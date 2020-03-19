from time import sleep
import subprocess
import os
import sys

from mail import mail
from configure import get_config
from logger import log

def icmp(quiet):
    
    try:
        poll = get_config('poll')
        hosts = get_config('host')
    except (IOError):
        print('\n\nAn existing poll and/or host configuration file could not be found at:\n' + os.getcwd() +
            '/config\n\n')
        sys.exit(0)    

    print('\n\n' +
            '#####################\n' +
            '#                   #\n' +
            '#   Pinging Hosts   #\n' + 
            '#                   #\n' +
            '#####################\n\n' +
            'All hosts will be pinged for 1 time every' , poll[0] , 'second(s).\n' +
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
                    msg = str('Camera ' +  str(x+1) + ' @ ' + str(hosts[x]) + ' has been offline for' + str(poll[1]) + ' rounds! Code: ' + str(r.returncode))
                    mail(msg)
                    log(msg)

            elif (r.returncode == 0):
                index[x] = 0

        sleep(poll[0])
