#!/usr/bin/env python3

import os
import shutil
import sys
import psutil

def check_reboot():
    """Returns True if the computer has a pending reboot."""
    return os.path.exists("/run/reboot-required") 

def check_disk_full(disk, min_gb, min_percent):
    """Returns True if there isn't enough disk space, False otherwise."""
    du = shutil.disk_usage(disk) 
    percent_free = 100 * du.free / du.total 
    gigabytes_free = du.free / 2**30
    if gigabytes_free < min_gb or percent_free < min_percent:
        return True
    return False

def check_root_full():
    """ Return True if the foor partition is full, False otherwise """
    return check_disk_full(disk="/", min_gb=2, min_percent=10)

def check_cpu_constrained():
    """ Returns True if the CPU is having too much usage """
    return psutil.cpu_percent(1) > 75:

def main():
    checks = [
              (check_reboot, "Pending Reboot"),
              (check_root_full, "Root partition full"),
              (check_cpu_constrained, "CPU usage too high")]
    all_passed = True
    for check, msg in checks:
        if check():
            print(msg)
            all_passed = False
    if not all_passed:
        sys.exit(1)
        

    print("All checks passed")
    sys.exit(0)


main()
