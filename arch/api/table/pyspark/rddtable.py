#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import uuid

from pyspark import SparkContext

from arch.api.table.pyspark import materialize, STORAGE_LEVEL
from arch.api.table.table import Table


class RDDTable(Table):

    def __init__(self, rdd=None, storage=None, partitions=1, schema=None, mode_instance=None):

        if rdd is None and storage is None:
            raise AssertionError("params rdd and storage are both None")
        super().__init__(storage, None)
        self._rdd = rdd
        self._partitions = partitions
        self.schema = schema or {}
        self.mode_instance = mode_instance
        self.storage = storage

    @property
    def rdd(self):
        if self._rdd is None:
            if self.storage is None:
                raise AssertionError("try create rdd from None storage")
            elif self.storage.count() <= 0:
                raise AssertionError("can't create rdd from empty storage")
            else:
                storage_iterator = self.storage.collect(use_serialize=True)
                num_partition = self.storage.partitions()
                self._rdd = SparkContext.getOrCreate() \
                    .parallelize(storage_iterator, num_partition) \
                    .persist(STORAGE_LEVEL)
        return self._rdd

    # self._rdd should not be pickled since all transformer/action should be invoked in driver.
    def __getstate__(self):
        state = dict(self.__dict__)
        if "_rdd" in state:
            del state["_rdd"]
        return state

    @property
    def partitions(self):
        return self._partitions

    def map(self, func):
        rtn_rdd = self.rdd.map(
            lambda x: func(x[0], x[1]),
            preservesPartitioning=True)
        rtn_rdd = materialize(rtn_rdd)
        return RDDTable(rdd=rtn_rdd, partitions=self._partitions, mode_instance=self.mode_instance)

    def mapValues(self, func):
        rtn_rdd = self.rdd.mapValues(func)
        rtn_rdd = materialize(rtn_rdd)
        return RDDTable(rdd=rtn_rdd, partitions=self._partitions, mode_instance=self.mode_instance)

    def mapPartitions(self, func):
        rtn_rdd = self.rdd.mapPartitions(
            lambda x: [[str(uuid.uuid1()), func(x)]],
            preservesPartitioning=True)
        rtn_rdd = materialize(rtn_rdd)
        #         rtn_rdd = rtn_rdd.zipWithUniqueId()
        #         rtn_rdd = rtn_rdd.map(lambda x: (x[1], x[0])).persist(StorageLevel.MEMORY_AND_DISK)
        return RDDTable(rdd=rtn_rdd, partitions=self._partitions, mode_instance=self.mode_instance)

    def reduce(self, func):
        return self.rdd.values().reduce(func)

    def join(self, other, func=None):
        _partitions = max(self._partitions, other.partitions)
        rtn_rdd = self.rdd.join(other.rdd, numPartitions=_partitions)
        if func is not None:
            rtn_rdd = rtn_rdd.mapValues(lambda x: func(x[0], x[1]))
        rtn_rdd = materialize(rtn_rdd)
        return RDDTable(rdd=rtn_rdd, partitions=_partitions, mode_instance=self.mode_instance)

    def glom(self):
        rtn_rdd = self.rdd.glom()
        rtn_rdd = materialize(rtn_rdd)
        return RDDTable(rdd=rtn_rdd, partitions=rtn_rdd.getNumPartitions(), mode_instance=self.mode_instance)

    def sample(self, fraction, seed=None):
        rtn_rdd = self.rdd.sample(withReplacement=False, fraction=fraction, seed=seed)
        rtn_rdd = materialize(rtn_rdd)
        return RDDTable(rdd=rtn_rdd, partitions=rtn_rdd.getNumPartitions(), mode_instance=self.mode_instance)

    def subtractByKey(self, other):
        raise NotImplementedError("subtractByKey is not implemented")

    def filter(self, func):
        rtn_rdd = self.rdd.filter(func)
        rtn_rdd = materialize(rtn_rdd)
        return RDDTable(rdd=rtn_rdd, partitions=rtn_rdd.getNumPartitions(), mode_instance=self.mode_instance)

    def union(self, other, func=lambda v1, v2: v1):
        raise NotImplementedError("union is not implemented")

    def flatMap(self, func):
        raise NotImplementedError("flatMap is not implemented")

    """
    overwrite several storage api
    """

    def count(self):
        num = self.rdd.count()
        return num

    def collect(self, min_chunk_size=0, use_serialize=True):
        rtn_iterator = iter(self.rdd.collect())
        return rtn_iterator

    def save_as(self, name, namespace, partition=None, use_serialize=True, persistent=True):
        if partition is None:
            partition = self._partitions

        partition = min(partition, 50)
        dup = self.mode_instance.dtable(name, namespace, partition,
                                        persistent=persistent, use_serialize=use_serialize)

        res = self.rdd.mapPartitions(lambda x: (dup.put_all(x),))
        res.count()

        return dup
