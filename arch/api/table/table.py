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

import abc
from typing import Iterable

import six

from arch.api import RuntimeInstance


# noinspection PyPep8Naming
@six.add_metaclass(abc.ABCMeta)
class Storage(object):
    """
    Storage apis
    """

    @abc.abstractmethod
    def save_as(self, name, namespace, partition=None, use_serialize=True):
        pass

    @abc.abstractmethod
    def put(self, k, v, use_serialize=True):
        pass

    @abc.abstractmethod
    def put_all(self, kv_list: Iterable, use_serialize=True, chunk_size=100000):
        pass

    @abc.abstractmethod
    def get(self, k, use_serialize=True):
        pass

    @abc.abstractmethod
    def collect(self, min_chunk_size=0, use_serialize=True):
        pass

    @abc.abstractmethod
    def delete(self, k, use_serialize=True):
        pass

    @abc.abstractmethod
    def destroy(self):
        pass

    @abc.abstractmethod
    def count(self):
        pass

    @abc.abstractmethod
    def put_if_absent(self, k, v, use_serialize=True):
        pass

    @abc.abstractmethod
    def take(self, n=1, keysOnly=False, use_serialize=True):
        pass

    @abc.abstractmethod
    def first(self, keysOnly=False, use_serialize=True):
        pass

    @abc.abstractmethod
    def partitions(self) -> int:
        pass


# noinspection PyPep8Naming
class Computing(object):
    """
    computing apis
    """

    @abc.abstractmethod
    def map(self, func):
        pass

    @abc.abstractmethod
    def mapValues(self, func):
        pass

    @abc.abstractmethod
    def mapPartitions(self, func):
        pass

    @abc.abstractmethod
    def reduce(self, func):
        pass

    @abc.abstractmethod
    def join(self, other, func):
        pass

    @abc.abstractmethod
    def glom(self):
        pass

    @abc.abstractmethod
    def sample(self, fraction, seed=None):
        pass

    @abc.abstractmethod
    def subtractByKey(self, other):
        pass

    @abc.abstractmethod
    def filter(self, func):
        pass

    @abc.abstractmethod
    def union(self, other, func=lambda v1, v2: v1):
        pass

    @abc.abstractmethod
    def flatMap(self, func):
        pass


# noinspection PyPep8Naming
class Table(object):

    def __init__(self, storage: Storage = None, computing: Computing = None):
        self.STORAGE = storage
        self.COMPUTING = computing

    def save_as(self, name, namespace, partition=None, use_serialize=True):
        return self.STORAGE.save_as(name, namespace, partition, use_serialize)

    def put(self, k, v, use_serialize=True):
        return self.STORAGE.put(k, v, use_serialize)

    def put_all(self, kv_list: Iterable, use_serialize=True, chunk_size=100000):
        return self.STORAGE.put_all(kv_list, use_serialize, chunk_size)

    def get(self, k, use_serialize=True):
        return self.STORAGE.get(k, use_serialize)

    def collect(self, min_chunk_size=0, use_serialize=True):
        return self.STORAGE.collect(min_chunk_size, use_serialize)

    def delete(self, k, use_serialize=True):
        return self.STORAGE.delete(k, use_serialize)

    def destroy(self):
        return self.STORAGE.destroy()

    def count(self):
        return self.STORAGE.count()

    def put_if_absent(self, k, v, use_serialize=True):
        return self.STORAGE.put_if_absent(k, v, use_serialize)

    def take(self, n=1, keysOnly=False, use_serialize=True):
        return self.STORAGE.take(n, keysOnly, use_serialize)

    def first(self, keysOnly=False, use_serialize=True):
        return self.STORAGE.first(keysOnly, use_serialize)

    def partitions(self):
        return self.STORAGE.partitions()

    """
    computing apis
    """

    def map(self, func):
        return self.COMPUTING.map(func)

    def mapValues(self, func):
        return self.COMPUTING.mapValues(func)

    def mapPartitions(self, func):
        return self.COMPUTING.mapPartitions(func)

    def reduce(self, func):
        return self.reduce(func)

    def join(self, other, func):
        return self.COMPUTING.join(other, func)

    def glom(self):
        return self.COMPUTING.glom()

    def sample(self, fraction, seed=None):
        return self.COMPUTING.sample(fraction, seed)

    def subtractByKey(self, other):
        return self.COMPUTING.subtractByKey(other)

    def filter(self, func):
        return self.COMPUTING.filter(func)

    def union(self, other, func=lambda v1, v2: v1):
        return self.COMPUTING.union(other, func)

    def flatMap(self, func):
        return self.COMPUTING.flatMap(func)


def table(name,
          namespace,
          partition=1,
          persistent=True,
          create_if_missing=True,
          error_if_exist=False,
          use_serialize=True) -> Table:
    return RuntimeInstance.TABLE_MANAGER.\
        table(name=name, namespace=namespace, partition=partition, persistent=persistent,
              create_if_missing=create_if_missing, error_if_exist=error_if_exist, use_serialize=use_serialize)


def parallelize(data: Iterable, include_key=False, name=None, partition=1, namespace=None, persistent=False,
                create_if_missing=True, error_if_exist=False, chunk_size=100000):
    return RuntimeInstance.TABLE_MANAGER.\
        parallelize(data=data, include_key=include_key, name=name, partition=partition, namespace=namespace,
                    create_if_missing=create_if_missing, error_if_exist=error_if_exist,
                    persistent=persistent, chunk_size=chunk_size)


def cleanup(name, namespace, persistent=False):
    return RuntimeInstance.TABLE_MANAGER.\
        cleanup(name=name, namespace=namespace, persistent=persistent)


def get_job_id():
    return RuntimeInstance.TABLE_MANAGER.job_id
