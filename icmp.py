from time import sleep
import subprocess
import os
import sys
import json

from mail import mail
from configure import get_config
from logger import log #, mysql_log

# --- ICMP FUNCTION ---
'''
    The following function is used to poll a list of hosts via ICMP.

    icmp() polls hosts by first fetching all required configuration files, validating accuracy, and then
    continuing. Depending on if the host OS is Windows or Linux, the ping command will be ran differently.
    According to the pulled poll.json file, hosts from host.json will be polled every X seconds and will be
    marked as offline after Y failed responses. A message will be formed based on responses and forwarded to
    mail() and log() to email and log these status updates respectively. It takes in a boolean value (quiet),
    passed from main() based on an OPTION users may enter upon running main.py.
        It does not return any value and will run indefinitely unless an error occurs, in which case it will
        exit.	
'''
# ---------------------
def icmp(quiet):
    
    try:
        poll = get_config('poll')
        hosts = get_config('host')
    except IOError:
        print('\n\nAn existing poll and/or host configuration file could not be found at:\n' + os.getcwd() +
            '/config\n\n')
        sys.exit(1)
    except json.decoder.JSONDecodeError:
        print('\n\nAn invalid host configuration file has been found. Now exiting...\n\n')
        sys.exit(1)

    print('\n\n' +
            '#####################\n' +
            '#                   #\n' +
            '#   Polling Hosts   #\n' + 
            '#                   #\n' +
            '#####################\n\n' +
            'All hosts will be polled every' , poll[0] , 'second(s).\n' +
            'Hosts will be marked as offline after', poll[1], 'unanswered polls.\n' +
            'To exit at any time, press CTRL+C.\n\n')

    index = [0] * len(hosts)

    while (True):
        for x in range (0, len(hosts)):
            if (os.name == 'nt'):
                r = subprocess.run(['ping', '-n', '1', hosts[x]], stdout=subprocess.DEVNULL)                
            else:
                r = subprocess.run(['ping', '-c 1', '-w 3', hosts[x]], stdout=subprocess.DEVNULL)  

            if (r.returncode != 0):
                index[x] += 1
                
                if (index[x] == 1):
                    if (quiet == False):
                        print('Camera', x+1, ' @ ', hosts[x], ' is offline!  Code: ', r.returncode)
                elif (index[x] == poll[1]):
                    if (quiet == False):
                        print('Camera', x+1, ' @ ', hosts[x], ' has been offline for', poll[1], 'rounds! Email notification sent!  Code: ', r.returncode)
                    msg = str('Camera ' +  str(x+1) + ' @ ' + str(hosts[x]) + ' has been offline for ' + str(poll[1]) + ' rounds! Code: ' + str(r.returncode))
                    mail(msg)
                    log(msg)
                    #mysql_log(msg)

            elif (r.returncode == 0):
                index[x] = 0
                if (quiet == False):
                    print('Camera', x+1, ' @ ', hosts[x], ' has come back online!')
        try:
            sleep(poll[0])
        except ValueError:
            print('\n\nAn invalid poll configuration file has been found. Now exiting...\n\n')
            sys.exit(1)
