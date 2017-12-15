"""
This script allows a user to give a condition (a shell command) that is
repeated until a successful return code is retrieved.

For example we get the output of the list docker containers command and
grep for running success to make sure the correct container is up.

Or we send requests to the mysql docker containers asking if they are
available for connection.

Accepts an 'on_success' command parameter. This is executed in the case
that the condition has successfully returned. We exit with the return
code of the on_success command.
"""

import sys
import time
import subprocess
import argparse


def return_code_to_success(return_code):
    if return_code == 0:
        return True
    else:
        return False


def run_command(condition):
    return_code = subprocess.call(condition, shell=True)
    return return_code


def main(args):
    # Default values
    wait_interval = 1
    timeout = 10
    success = False

    # Get any overrides
    condition = args.condition
    if args.wait_interval is not None:
        wait_interval = int(args.wait_interval)
    if args.timeout is not None:
        timeout = int(args.timeout)

    # Start main loop
    loop_time = 0
    while True:
        return_code = run_command(condition)
        success = return_code_to_success(return_code)

        if success is True:
            print("SUCCESS after {0} seconds and {1} retries.".format(loop_time, int(loop_time/wait_interval)))
            if args.on_success is not None:
                return_code = run_command(args.on_success)
                sys.exit(return_code)
            sys.exit(0)
        if loop_time >= timeout:
            print("FAILURE: timeout after {0} seconds and {1} retries.".format(loop_time, int(loop_time/wait_interval)))
            sys.exit(1)

        loop_time = loop_time + wait_interval
        time.sleep(wait_interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("condition", help="A short shell command to condition the wait on")
    parser.add_argument("--wait_interval", help="INTEGER, SECONDS, time between tries to execute the condition command")
    parser.add_argument("--timeout", help="INTEGER, SECONDS, time you are willing to \
                                           wait for the condition to be successful")
    parser.add_argument("--on_success", help="SCRIPT, a command to be ran if the condition is successfully \
                                              executed.")

    args = parser.parse_args()
    main(args)