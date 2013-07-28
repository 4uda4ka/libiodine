# File: util/_limit_limit_run.py
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

# Important: Python 3.3+ is required

import os, sys, resource
import shlex, subprocess
import pwd, logging

from .limit import RunProfile, LimitStatus, SYSERROR, TIMEOUT, RUNTIME, ERRCUT
from threading import Timer

# Get logger
# TODO: change logging method
log = logging

# Get Uid Info Begin
try:
    if os.geteuid() != pwd.getpwnam('root').pw_uid:
        log.warning(__file__ + ': root permission is required.')
    nobody = pwd.getpwnam('nobody')
    nuid = nobody.pw_uid
    ngid = nobody.pw_gid
except:
    log.warning(__file__ + ': Failed to get current & nobody\'s uid & gid')
# Get Uid Info End

# Main Function limit_run Begin #
def limit_run(command_line, instream = None, outstream = None,
              errstream = None, limits = [], timeout = None,
              chroot = None):
    """
    try to run command_line with 'nobody' permission in chroot directory
    within the limitations specify by limits argument. limits is a list of Limit.
    return RunProfile
    """
    profile = RunProfile()
    if sys.platform.startswith('win32'):
        # sorry to windows user.
        profile.ok = False
        profile.error = SYSERROR
        return profile

    def preexec():
        # chroot to safe place if needed
        try:
            if chroot:
                os.chroot(chroot)
        except Exception as err:
            log.warning(str(err) + ': unable to chroot')
        # setup resource kernel limitation
        for limit in limits:
            if limit.rlimit != None:
                resource.setrlimit(
                    limit.rlimit, # hard limit & soft limit
                    (limit.rlimit_value, limit.rlimit_value)
                )
        # setuid for nobody
        try:
            os.setresgid(ngid, ngid, ngid)
            os.setresuid(nuid, nuid, nuid)
        except Exception as err:
            log.warning(str(err) + ': unable to setuid')

    args = shlex.split(command_line)
    try:
        proc = subprocess.Popen(args, stdin = instream, stdout = outstream,
                                stderr = errstream, preexec_fn = preexec,
                                close_fds = True)
        
        def killer():
            print('KILLED')
            proc.kill()
            profile.ok = False
            profile.error = TIMEOUT
        if timeout != None:
            t = Timer(timeout, killer)
            t.start()
        pid, exitcode, rusage = os.wait4(proc.pid, 0)
        if timeout != None:
            t.cancel()
        
        if profile.ok:
            return _gen_profile(profile, rusage, limits, exitcode)
        else: return profile

    except Exception as err:
        # system error
        try: proc.kill()
        except: pass
        profile.ok = False
        profile.error = SYSERROR
        profile.warnings += [str(err)]
        return profile

# Main Funtion limit_run End

# Utility Function Begin
def _gen_profile(profile, rusage, limits, exitcode = 0):
    profile.ok = True
    profile.exitcode = exitcode
    if exitcode >= ERRCUT:
        # indicate an runtime error
        profile.ok = False
        profile.error = RUNTIME
    for limit in limits:
        if limit.value == None:
            # just a kernel resource restricion
            continue
        # else should return with profile
        ls = LimitStatus()
        ls.description = limit.description
        ls.value = limit.current(rusage, exitcode)
        profile.limits += [ls]
        if ls.value > limit.value:
            # limitation exceeded
            profile.ok = False
            profile.error = limit.description
    return profile
# Utility Function End
