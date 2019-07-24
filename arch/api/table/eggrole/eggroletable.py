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

from arch.api.table.table import Table
from arch.api.table.eggrole.storage import EggRollStorage


class EggRoleTable(Table):

    def __init__(self, storage=EggRollStorage):
        super().__init__(storage=storage)

    def map(self, func):
        pass

    def mapValues(self, func):
        pass

    def mapPartitions(self, func):
        pass

    def reduce(self, func):
        pass

    def join(self, other, func=None):
        pass

    def glom(self):
        pass

    def sample(self, fraction, seed=None):
        pass

    def subtractByKey(self, other):
        pass

    def filter(self, func):
        pass

    def union(self, other, func=lambda v1, v2: v1):
        pass

    def flatMap(self, func):
        pass
