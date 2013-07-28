# File: util/_limit_limitation.py
# Author: Jason Lau

# Copyright 2013 Jason Lau <i@dotkrnl.com>
# Bug report email <i@dotkrnl.com>
# This file is part of iodine.

# iodine is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# iodine is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with iodine. if not, see <http://www.gnu.org/licenses/>.

import resource
from .limit import Limit

class TimeLimit(Limit):
    """
    specify cpu(user + sys) time limitation,
    TimeLimit(time), time should be specify in second.
    """
    
    def __init__(self, time):
        super().__init__()
        time = float(time) # test number
        self.description = 'cpu time'
        self.value = time
        self.rlimit = resource.RLIMIT_CPU
        self.rlimit_value = int(time) + 1

    def current(self, rusage, exitcode):
        return rusage.ru_utime + rusage.ru_stime
