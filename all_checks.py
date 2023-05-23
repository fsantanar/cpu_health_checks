import os
import shutil
import sys 
def check_reboot(): """Returns True if the computer has a pending reboot."""
    return os.path.exists("/run/reboot-required") 

def check_disk_full(disk, min absolute, min percent):
    """Returns True if there isn't enough disk space, False otherwise."""
    du = shutil.disk usage(disk) 
    percent free = 100 * du.free / du.total 
    gigabytes free = du.free / 2**30
    if gigabytes_free < min_absolute or percent_free < min_percent:
        return True
    return False 1 

def main():
    if check_reboot():
        print("Pending Reboot.")
        sys.exit(1)
    if check_disk_full("/",2,10):
        print("Disk too close to full")
        sys.exit(1)
    print("All checks passed")
