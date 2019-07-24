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
import os
import threading
import uuid
from typing import Iterable

import six

from arch.api import WorkMode
from arch.api.table.table import Table


def init(job_id=None, mode: WorkMode = WorkMode.STANDALONE):
    pass


@six.add_metaclass(abc.ABCMeta)
class TableManager(object):
    _instance_lock = threading.Lock()

    @abc.abstractmethod
    def _table(self,
               name,
               namespace,
               partition=1,
               create_if_missing=True,
               error_if_exist=False,
               persistent=True,
               use_serialize=True) -> Table:
        pass

    @abc.abstractmethod
    def _parallelize(self,
                     data: Iterable,
                     include_key=False,
                     name=None,
                     partition=1,
                     namespace=None,
                     create_if_missing=True,
                     error_if_exist=False,
                     persistent=False,
                     chunk_size=100000) -> Table:
        pass

    @abc.abstractmethod
    def _cleanup(self, name, namespace, persistent):
        pass

    @abc.abstractmethod
    def _create_storage(self, name, namespace, partition=1,
                        create_if_missing=True, error_if_exist=False, persistent=True,
                        use_serialize=True):
        pass

    @staticmethod
    def set_instance(inst):
        if not hasattr(TableManager, "_instance"):
            with TableManager._instance_lock:
                if not hasattr(TableManager, "__instance"):
                    TableManager.__instance = inst
        else:
            pass  # todo: add logs

    @staticmethod
    def get_instance() -> 'TableManager':
        if not hasattr(TableManager, "__instance"):
            raise EnvironmentError("table manager should initialize before use")
        return TableManager.__instance

    @staticmethod
    def table(name,
              namespace,
              partition=1,
              create_if_missing=True,
              error_if_exist=False,
              persistent=True,
              use_serialize=True) -> Table:

        return TableManager.get_instance()\
            ._table(name=name, namespace=namespace, partition=partition,
                    create_if_missing=create_if_missing, error_if_exist=error_if_exist,
                    persistent=persistent, use_serialize=use_serialize)

    @staticmethod
    def parallelize(data: Iterable,
                    include_key=False,
                    name=None,
                    partition=1,
                    namespace=None,
                    create_if_missing=True,
                    error_if_exist=False,
                    persistent=False,
                    chunk_size=100000) -> Table:
        return TableManager.get_instance()\
            ._parallelize(data=data, include_key=include_key, name=name, partition=partition, namespace=namespace,
                          create_if_missing=create_if_missing, error_if_exist=error_if_exist,
                          persistent=persistent, chunk_size=chunk_size)

    @staticmethod
    def cleanup(name, namespace, persistent):
        return TableManager.get_instance()\
            ._cleanup(name=name, namespace=namespace, persistent=persistent)
