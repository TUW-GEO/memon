# Copyright (c) 2017,Vienna University of Technology,
# Department of Geodesy and Geoinformation
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#   * Neither the name of the Vienna University of Technology, Department of
#     Geodesy and Geoinformation nor the names of its contributors may be used
#     to endorse or promote products derived from this software without specific
#     prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL VIENNA UNIVERSITY OF TECHNOLOGY, DEPARTMENT OF
# GEODESY AND GEOINFORMATION BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
This module implements functions and classes to monitor the memory status.
"""

import psutil
import time
import threading


class MemoryMonitor(threading.Thread):

    def __init__(self, interval=0.1,
                 memory_limit=50):

        super(MemoryMonitor, self).__init__()

        self.__interval = interval
        self.__mem_limit = memory_limit
        self.is_recording = False
        self.history = []
        self.__monitor = threading.Event()
        self.__monitor.set()
        self.__has_shutdown = False
        self.max_mem = 0.
        self.total_mem = psutil.virtual_memory().total

    def run(self):
        """
        Run memory monitor.
        """
        while self.is_running():
            cur_mem = psutil.virtual_memory().percent

            if self.max_mem < cur_mem:
                self.max_mem = cur_mem

            if self.is_recording:
                self.history.append(cur_mem)

            time.sleep(self.__interval)

    @property
    def current_usage(self):
        """
        Return currently measured memory in percent.
        """
        return psutil.virtual_memory().percent

    def start_recording(self):
        """
        Start memory recording.
        """
        self.is_recording = True

    def stop_recording(self):
        """
        Stop memory recording.
        """
        self.is_recording = False

    def clear_recording_history(self):
        """
        Clear recording history.
        """
        self.history = []

    def reset_max_memory(self):
        """
        Reset maximum memory.
        """
        self.max_mem = psutil.virtual_memory().percent

    def memory_available(self):
        """
        Get memory availability.

        Returns
        -------
        status : bool
           If memory is available return is True, otherwise False.
        """
        mem = self.history
        # we calculate the delta to get the range of memory that the process is
        # using during regular allocation and freeing of memory
        delta_mem = max(mem) - min(mem)
        # this delta is then used together with the mean to check for the
        # memory limit. This is to make sure that historical information about
        # how much memory the process allocates does still fit under the memory
        # limit.
        exp_mem = sum(mem)/float(len(mem)) + delta_mem

        if exp_mem >= self.__mem_limit:
            return False
        else:
            return True

    def stop(self):
        """
        Clear memory monitoring.
        """
        self.__monitor.clear()

    def is_running(self):
        """
        Check if memory monitor is running.

        Returns
        -------
        status : bool
            Status of memory monitor.
        """
        return self.__monitor.isSet()

    def is_shutdown(self):
        """
        Check if memory monitor is shutdown.

        Returns
        -------
        status : bool
            Status of memory monitor.
        """
        return self.__has_shutdown

    def __enter__(self):
        """
        """
        return self

    def close(self):
        """
        Stop memory monitoring.
        """
        self.stop()

    def __exit__(self):
        """
        Stop memory monitoring.
        """
        self.close()

    def __del__(self):
        """
        Stop memory monitoring on object destruction.
        """
        self.close()
