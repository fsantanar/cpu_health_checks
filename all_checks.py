#!/usr/bin/env python3



import os
import shutil
import sys
import psutil
import socket
import subprocess
import heapq
import ssl
import time
import urllib
import urllib.request
import time
from tqdm import tqdm


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def run_command(command):
    return subprocess.run(command, shell=True, capture_output=True, text=True)

def print_message(message):
    print(bcolors.OKGREEN + message + bcolors.ENDC)

def print_error(message):
    print(bcolors.FAIL + message + bcolors.ENDC)

def check_reboot():
    """Returns True if the computer has a pending reboot."""
    return os.path.exists('/run/reboot-required')

def check_disk_full(min_gb=2, min_percent=10):
    """Returns True if there isn't enough disk space, False otherwise."""
    du = shutil.disk_usage('/') 
    percent_free = 100 * du.free / du.total 
    gigabytes_free = du.free / 2**30
    message_head = (f'{gigabytes_free:.1f} Gb free ({percent_free:.2f}%) '
                    f'out of a total of {du.total/2**30:.1f} Gb')
    home_usage_output = run_command('du -sk $HOME')
    home_usage = int(home_usage_output.stdout.split('\t')[0]) / 2**20
    home_subfolders_output = run_command('ls -d $HOME/*/')
    subfolders_sizes = {}
    for subfolder in home_subfolders_output.stdout.split():
        usage_output = run_command('du -sk ' + subfolder)
        usage_gb = int(usage_output.stdout.split('\t')[0]) / 2 **20
        subfolders_sizes[subfolder] = usage_gb
    largest_subfolders = heapq.nlargest(3, subfolders_sizes.items(), key=lambda item: item[1])
    
    disk_full = False
    print_function = print_message
    if gigabytes_free < min_gb or percent_free < min_percent:
        disk_full = True
        message_head = 'Disk too close to full: Only '+message_head
        print_function = print_error

    print_function(message_head)
    print_function(f'Home folder is {home_usage:.2f} Gb')
    print_function('The largest home subfolders are:')
    for subfolder in largest_subfolders:
        print_function(f'{subfolder[0]} is {subfolder[1]:.2f} Gb')
                    
    return disk_full


def check_cpu_constrained():
    """ Returns True if the CPU is having too much usage """
    return psutil.cpu_percent(1) > 75

def check_no_network():
    """ Return True if it fails to resolve the given URL, and False otherwise"""
    try:
        socket.gethostbyname('www.google.com')
        return False
    except:
        return True

def check_download_speed():
    sizes = ['1MB', '10MB', '100MB', '1GB', '10GB']
    last_test = False
    message1 = 'Testing Download Speed: '
    message2a = 'Running preliminary quick tests'
    print(message1 + message2a, end='\r', flush=True)
    for ind_size in range(len(sizes)):
        size = sizes[ind_size]
        url = 'http://speedtest.tele2.net/' + size + '.zip'
        start_time = time.time()
        response = urllib.request.urlopen(url)
        file_size = int(response.headers['Content-Length'])
        downloaded_size = 0
        block_size = 8192  # Adjust the block size as per your preference

        if last_test:
            progress_bar = tqdm(total=file_size, unit='B', unit_scale=True, ncols=80)

        with open("/dev/null", 'wb') as file:
            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                downloaded_size += len(buffer)
                file.write(buffer)
                if last_test:
                    progress_bar.update(len(buffer))

        response.close()
        end_time = time.time()

        if last_test:
            progress_bar.close()

        download_time = end_time - start_time

        if size[-2:] == 'MB':
            megas = int(size[:-2])
        if size[-2:] == 'GB':
            megas = int(size[:-2]) * 2**10

        download_speed_mbps = megas / download_time
        time.sleep(1)  # To avoid overloading the server

        if last_test is True:
            print(f"Download Speed: {download_speed_mbps:.2f} Mbps")
            break

        if download_time > 3:
            last_test = True
            message2b = f'Running final download test on {sizes[ind_size+1]} size file'
            time.sleep(1.5) # So that the user can see the message change
            print(message1 + message2b)

def main():
    fails = 0
    checks = [check_reboot, check_disk_full, check_cpu_constrained,
              check_no_network, check_download_speed]
    all_passed = True
    for check in checks:
        if check():
            all_passed = False
            fails += 1

    print(' ')
    print('#'*28)
    if fails == 0:
        print('###  '+bcolors.OKGREEN + 'All checks passed' + bcolors.ENDC+'  ###')
    else:
        print('###  '+bcolors.FAIL + f'{fails:02}' + ' check(s) failed' + bcolors.ENDC+'  ###')
    print('#'*28)


if __name__=='__main__':
    main()



