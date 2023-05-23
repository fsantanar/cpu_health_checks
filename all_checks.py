import os
import shutil
import sys 

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

def main():
    if check_reboot():
        print("Pending Reboot.")
        sys.exit(1)
    if check_disk_full(disk="/", min_gb=2, min_percent=10):
        print("Disk too close to full")
        sys.exit(1)
    print("All checks passed")
    sys.exit(0)


main()
