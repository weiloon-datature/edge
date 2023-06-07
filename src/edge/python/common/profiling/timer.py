#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   timer.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   This module contains the timer function decorator.
"""

import time

from common.constants import Timers
from common.logger import ProfileLogger


def timing(timer: Timers):
    """Measure the execution time of the function object passed."""

    def timer_wrapper(func):
        """Wrap the function object passed and outputs the execution time
        (in milliseconds) of the function object to the debug log.

        Args:
            func: Function object to be wrapped.
        """
        if timer == Timers.PERF_COUNTER:
            execute_timer = time.perf_counter_ns
        elif timer == Timers.PROCESS_TIMER:
            execute_timer = time.process_time_ns
        elif timer == Timers.THREAD_TIMER:
            execute_timer = time.thread_time_ns
        else:
            ProfileLogger.error(
                f"{func.__qualname__!r}: Timer type not supported")

        def timer_func(*args, **kwargs):
            """Execute the function object passed and calculates
            the execution time (in milliseconds) of the function object.

            Returns:
                The result of the function object passed.
            """
            timer1 = execute_timer()
            result = func(*args, **kwargs)
            timer2 = execute_timer()
            execution_time = (timer2 - timer1) / 1000000
            func_name = f"'{args[0].__class__.__name__}.{func.__name__}'"
            ProfileLogger.debug(f"{func_name} {execution_time:>15.6f} ms")
            return result

        return timer_func

    return timer_wrapper
