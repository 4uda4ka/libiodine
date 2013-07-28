# File: util/_limit_class.py
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

# Class Limit Start #
class Limit:
    """
    specify one limitation, everything is optional:
    description: user readable string for run profile.
    value: the limitation value, comparable with the return value of current(pid).
    rlimit: hard limitation type passed to the kernel (Unix/Linux only).
    rlimit_value: hard limitation value passed to the kernel (Unix/Linux only).
    """
    
    description = ''
    value = None
    rlimit = None
    rlimit_value = None
    
    def current(pid):
        """
        get the current value of this limitation with pid.
        return value should be comparable with value
        """
        return None
# Class Limit End #

# Class Limit Status Start #
class LimitStatus:
    """
    specify the status of one limitation, everything is optional:
    description: user readable string for run profile, copyed form Limit.
    value: the limitation return value of current(pid).
    """
    
    description = ''
    value = None
# Class Limit Status End #

# Class Run Profile Start #
class RunProfile:
    """
    indicate the result of limit_run:
    ok: True/False indicate if the judge process can be continue.
    exitcode: exitcode
    error: reason when ok = False, copy from Limit or TIMEOUT/SYSERROR.
    limits: a list of LimitStatus indicate limitation status
    warnings: a list of str, indicate everything should be log
    """
    ok = False
    exitcode = 0
    error = ''

    def __init__(self):
        """
        init process for empty list
        """
        self.limits = []
        self.warnings = []

    def __str__(self):
        """
        show all data inside
        """
        return ('{ok:%d, exitcode:%d, error:\'%s\'' % (
            self.ok , self.exitcode, self.error)
                + ', limits:' + self.limits.__str__()
                + ', warnings:' + self.warnings.__str__() + '}')
    def __repr__(self):
        return self.__str__()
# Class Run Profile End #
