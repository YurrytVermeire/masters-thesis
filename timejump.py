#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import traceback
from threading import Thread

import win32api as win # type: ignore
import pywintypes # type: ignore
import datetime
import time

from lib.common.abstracts import Auxiliary

log = logging.getLogger(__name__)


def time_jump(min, timezonediff):
  """Adds minutes to the Windows system time.

  Args:
    min: The number of minutes to add or remove (if negative).
    timezonediff: The number of hours for the timezone difference to UTC
  """

  # Get current local time
  dt = datetime.datetime.now()

  # Add the minutes
  dt = dt + datetime.timedelta(minutes=min)
  dt = dt + datetime.timedelta(hours=timezonediff)

  # Convert datetime to win32 time tuple including miliseconds
  new_time = pywintypes.Time(dt.timetuple())

  # Set the new system time
  win.SetLocalTime(new_time)

class Timejump(Auxiliary, Thread):

    def __init__(self, options, config):
        Auxiliary.__init__(self, options, config)
        Thread.__init__(self)
        self.config = config
        self.enabled = self.config.timejumper
        self.do_run = self.enabled

    def stop(self):
        pass

    def run(self):
        try:
            # wait 1 minute till activation
            time.sleep(60)
            time_jump(59,2)
        except Exception:
            error_exc = traceback.format_exc()
            log.exception(error_exc)
