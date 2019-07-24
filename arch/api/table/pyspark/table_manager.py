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

import fnmatch
import os
import shutil
import uuid
from typing import Iterable

from pyspark import SparkContext, SparkConf

from arch.api import StoreType
from arch.api.table.eggrole.storage import EggRollStorage
from arch.api.table.pyspark import materialize
from arch.api.table.pyspark.rddtable import RDDTable
from arch.api.table.table_manager import TableManager as TableManger
from arch.api.utils import file_utils


class RDDTableManager(TableManger):
    """
    manage RDDTable, use EggRoleStorage as storage
    """

    def __init__(self, job_id=None):
        self.data_dir = os.path.join(file_utils.get_project_base_directory(), 'data')
        self.job_id = str(uuid.uuid1()) if job_id is None else "{}".format(job_id)
        self.meta_table = EggRollStorage('__META__', '__META__', 'fragments', 10)
        conf = SparkConf().setAppName(self.job_id)
        SparkContext.getOrCreate(conf)
        super().set_instance(self)

    """
    subclass-specialized methods
    """

    def _create_storage(self, name, namespace, partition=1,
                        create_if_missing=True, error_if_exist=False, persistent=True,
                        use_serialize=True):
        __type = StoreType.LMDB.value if persistent else StoreType.IN_MEMORY.value
        _table_key = ".".join([__type, namespace, name])
        self.meta_table.put_if_absent(_table_key, partition)
        partition = self.meta_table.get(_table_key)
        _d_table = EggRollStorage(__type, namespace, name, partition, use_serialize=use_serialize)
        return _d_table

    """
    implement abc methods
    """

    def _table(self,
               name,
               namespace,
               partition=1,
               create_if_missing=True,
               error_if_exist=False,
               persistent=True,
               use_serialize=True):
        _storage = self._create_storage(name, namespace, partition,
                                        create_if_missing, error_if_exist, persistent, use_serialize)
        return RDDTable(storage=_storage, partitions=_storage.partitions(), mode_instance=self)

    def _parallelize(self,
                     data: Iterable,
                     include_key=False,
                     name=None,
                     partition=1,
                     namespace=None,
                     create_if_missing=True,
                     error_if_exist=False,
                     persistent=False,
                     chunk_size=100000):

        _iter = data if include_key else enumerate(data)

        # if name is None:
        #     name = str(uuid.uuid1())
        # if namespace is None:
        #     namespace = self.job_id

        rdd = SparkContext.getOrCreate().parallelize(_iter, partition)
        rdd = materialize(rdd)
        rdd_inst = RDDTable(rdd=rdd, partitions=partition, mode_instance=self)

        return rdd_inst

    def _cleanup(self, name, namespace, persistent):
        if not namespace or not name:
            raise ValueError("neither name nor namespace can be blank")

        _type = StoreType.LMDB.value if persistent else StoreType.IN_MEMORY.value
        _base_dir = os.sep.join([self.data_dir, _type])
        if not os.path.isdir(_base_dir):
            raise EnvironmentError("illegal datadir set for eggroll")

        _namespace_dir = os.sep.join([_base_dir, namespace])
        if not os.path.isdir(_namespace_dir):
            raise EnvironmentError("namespace does not exist")

        _tables_to_delete = fnmatch.filter(os.listdir(_namespace_dir), name)
        for table in _tables_to_delete:
            shutil.rmtree(os.sep.join([_namespace_dir, table]))
