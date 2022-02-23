#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Common modules for parse script arguments"""

import argparse
import logging
import sys


def parse_sys_args(argv):
    """Parses commaond-line arguments"""
    parser = argparse.ArgumentParser(
        description="Gitlab backup tool in group level")
    parser.add_argument(
        "--local", action="store", dest="local",
        required=True, help="Local gitlab http url, "
                            "ex: https://local.gitlab.com")
    parser.add_argument(
        "--local-token", action="store", dest="local_token",
        required=True, help="Local gitlab private token.")
    parser.add_argument(
        "--local-group", action="store", dest="local_group",
        required=True, help="Local github group for reading.")
    parser.add_argument(
        "--remote", action="store", dest="remote",
        required=True, help="Remote gitlab http url, "
                            "ex: https://remote.gitlab.com")
    parser.add_argument(
        "--remote-token", action="store", dest="remote_token",
        required=True, help="Remote gitlab private token")
    parser.add_argument(
        "--remote-group", action="store", dest="remote_group",
        required=True, help="Target group of remote github for backup.")
    parser.add_argument(
        "--push-url", action="store", dest="push_url",
        required=True, help="Remote push url for backup target")
    parser.add_argument(
        "--force-push", action="store_true",
        dest="force_push", default=True,
        required=False, help="Force push to remote by default")
    parser.add_argument(
        "--ignore-branches", action="store", dest="ignore_branches",
        required=False, help="Not sync for ignore branches, "
                             "ex: cherry-pick,dev,temp")
    parser.add_argument(
        "--allow-branches", action="store", dest="allow_branches",
        required=False, help="Only sync for allow branches, "
                             "ex: master,main,qa. "
                             "if not given, sync all branches."
                             "If ignore branches is given, the"
                             "priority is higher than this argument")
    parser.add_argument(
        "-d", "--debug", action="store_true", dest="debug",
        default=False, help="Enable debug message.")
    parser.add_argument(
        "-v", "--verbose", action="store_true", dest="verbose",
        default=True, help="Show message in standard output.")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    else:
        return parser.parse_args(argv[1:])
