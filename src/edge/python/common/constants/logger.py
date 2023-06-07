#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   logger.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Logging constants.
"""

import logging

from colorama import Fore, Style

COLORED_FORMAT = {
    logging.DEBUG:
    (f"{Fore.WHITE + Style.DIM}[%(asctime)s,%(msecs)010.6f"
     f" {Fore.BLUE} %(levelname)s %(filename)s:%(lineno)d"
     f" %(funcName)s] {Fore.MAGENTA} %(message)s{Style.RESET_ALL}"),
    logging.INFO: (f"{Fore.WHITE + Style.DIM}[%(asctime)s,%(msecs)010.6f"
                   f" {Style.RESET_ALL}{Fore.CYAN} %(levelname)s"
                   " %(filename)s:%(lineno)d %(funcName)s]"
                   f" {Fore.MAGENTA} %(message)s{Style.RESET_ALL}"),
    logging.WARNING:
    (f"{Fore.WHITE + Style.DIM}[%(asctime)s,%(msecs)010.6f"
     f" {Style.RESET_ALL}{Fore.YELLOW} %(levelname)s"
     " %(filename)s:%(lineno)d %(funcName)s]"
     f" {Fore.YELLOW + Style.BRIGHT} %(message)s{Style.RESET_ALL}"),
    logging.ERROR: (f"{Fore.WHITE + Style.DIM}[%(asctime)s,%(msecs)010.6f"
                    f" {Style.RESET_ALL}{Fore.RED} %(levelname)s"
                    " %(filename)s:%(lineno)d %(funcName)s]"
                    f" {Style.BRIGHT} %(message)s{Style.RESET_ALL}"),
    logging.CRITICAL: (f"{Fore.WHITE + Style.DIM}[%(asctime)s,%(msecs)010.6f"
                       f"{Style.RESET_ALL}{Fore.RED} %(levelname)s"
                       " %(filename)s:%(lineno)d %(funcName)s]"
                       f" {Style.BRIGHT} %(message)s{Style.RESET_ALL}"),
}
