
import os
import pickle as c_pickle
from arch.api.utils import cache_utils, file_utils
from arch.api.utils.core import string_to_bytes, bytes_to_string
from heapq import heapify, heappop, heapreplace
from typing import Iterable
import lmdb
from cachetools import cached
import hashlib
from arch.api.table.table import Storage


class EggRollStorage(Storage):
    def __init__(self, _type, namespace, name, partitions, use_serialize=True):
        pass

    def __str__(self):
        return "type: {}, namespace: {}, name: {}, partitions: {}".format(self._type, self._namespace, self._name,
                                                                          self._partitions)

    def put(self, k, v, use_serialize=True):
        pass

    def put_all(self, kv_list: Iterable, use_serialize=True, chunk_size=100000):
        pass

    def put_if_absent(self, k, v, use_serialize=True):
        pass


    def get(self, k, use_serialize=True):
        pass

    def collect(self, min_chunk_size=0, use_serialize=True):
        pass

    def first(self, keysOnly=False, use_serialize=True):
        pass

    def take(self, n=1, keysOnly=False, use_serialize=True):
        pass

    def save_as(self, name, namespace, partition=None, use_serialize=True):
        pass

    def count(self):
        pass

    def delete(self, k, use_serialize=True):
        pass

    def destroy(self):
        pass

    def partitions(self) -> int:
        pass
