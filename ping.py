from time import sleep
import subprocess
import json
import sys
import os

import smtplib, ssl

#Create or open list of hosts
#Pass to ping function
#Ping all hosts, wait 30s, loop
#Email if host is down for 2 pings in a row

##Config For:
###Hosts
###Emails (sender and receiver)
###Polling method and setup

'''
#########################
#                       #
#   Ping Return Codes   #
#                       #
#########################

0   :   success
1   :   unreachable
2   :   address error
'''

def mail(msg):

    #Loop to iterate through a list of set email addresses

    port = 465
    password = ('pipollermail123')

    context = ssl.create_default_context()
    msg = """\
        Subject: Camera Down\n\n""" + msg

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login('pipoller.alert@gmail.com', password)
        server.sendmail('pipoller.alert@gmail.com', 'nicolas.bermeo@ontariotechu.net', msg)

def ping(hosts):
    
    print('\n\n' +
            '#####################\n' +
            '#                   #\n' +
            '#   Pinging Hosts   #\n' + 
            '#                   #\n' +
            '#####################\n\n' +
            'All hosts will be pinged for (1) time every (30) seconds.\n' +
            'To exit at any time, press CTRL+C.\n\n')

    #responses = []
    index = [0] * len(hosts)

    while (1==1):
        for x in range (0, len(hosts)):
            if (os.name == 'nt'): #Windows, not functional
                r = subprocess.run(['ping', '-n', '1', hosts[x]], stdout=subprocess.DEVNULL)                
            else:
                r = subprocess.run(['ping', '-c 1', '-w 3', hosts[x]], stdout=subprocess.DEVNULL)  

            if (r.returncode != 0):
                index[x] += 1
                
                if (index[x] == 1):
                    #responses.append('Camera', x, ' @ ', hosts[x], ' is offline!  Code: ', r.returncode)    
                    print('Camera', x, ' @ ', hosts[x], ' is offline!  Code: ', r.returncode)
                elif (index[x] == 2):
                    print('Camera', x, ' @ ', hosts[x], ' has been offline for (2) rounds! Email notification sent!  Code: ', r.returncode)
                    msg = str('Camera ' +  str(x) + ' @ ' + hosts[x] + ' has been offline for (2) rounds! Code: ' + str(r.returncode))
                    print(msg)
                    mail(msg)

            elif (r.returncode == 0):
                index[x] = 0
        sleep(5)

def gen_config(hosts):
    with open('./hosts.json', 'w+') as outfile:
        json.dump(hosts, outfile)

def load_config():
    with open('./hosts.json') as infile:
        hosts = json.load(infile)
    return(hosts)

def no_config():
    gc_in = '0'
    while (gc_in != '2'):
        gc_in = input('\n\n' +
            '##################################\n' +
            '#                                #\n' +
            '#   Missing Configuration File   #\n' + 
            '#                                #\n' +
            '##################################\n\n' +
            'An existing configuration file could not be found at ' + os.getcwd() +
            '\n\nPlease select one of the following options:\n\n' +
            '1: Create a new configuration file\n' +
            '2: Exit\n')

        if (gc_in == '1'):
            print('Generating configuration file...')
            gen_config(create_config())
            break
        elif (gc_in == '2'):
            print('Exiting...')
            sys.exit()
        else:
            print('Invalid input.')

def found_config():
    fc_in = '0'
    while (fc_in != '3'):
        fc_in = input('\n\n' +
            '################################\n' +
            '#                              #\n' +
            '#   Found Configuration File   #\n' + 
            '#                              #\n' +
            '################################\n\n' +             
            'An existing configuration was found at ' + os.getcwd() +
            '\n\nWould you like to continue using this file?\n' +
            '1: Yes, continue using this file\n' +
            '2: No, create a new file\n' +
            '3: Exit\n')

        if (fc_in == '1'):
            print('Continuing...')
            return(load_config())
        elif (fc_in == '2'):
            gen_config(create_config())
            return(load_config())
        elif (fc_in == '3'):
            print('Exiting...')
            sys.exit()
        else:
            print('Invalid input.')

def create_config():
    cc_in = 0

    while (cc_in != 4):
        cc_in = input('\n\n' +
                '#################################\n' +
                '#                               #\n' +
                '#   Create Configuration File   #\n' + 
                '#                               #\n' +
                '#################################\n\n' + 
                'Please select one of the following polling methods:\n\n' +
                '1: SNMPv1\n' +
                '2: SNMPv2c\n' +
                '3: SNMPv3\n' +
                '4: ICMP\n')
    
        if (cc_in != '4'):
            #ver = '???'
            print('Invalid input. Only ICMP is currently available.')
        else:
            #ver = 'ICMP'
            cc_in = input('\n\nPlease enter either a list or range of IP addresses.\n' +
                        'For a list, separate using commas. For a range, use dashes.\n' +
                        'Please note that a range of addresses must be in the same /24 subnet.\n\n')
            cc_in = cc_in.replace(' ', '')
                        

            if (',' in cc_in and '-' not in cc_in):
                cc_in = cc_in.replace(',', ' ')
                addrs = cc_in.split(' ')
                hosts = []
                for x in range(0, int(len(addrs))):
                    hosts.append(addrs[x])                  
                break
            elif ('-' in cc_in and ',' not in cc_in):
                cc_in = cc_in.replace('-', ' ')
                addrs = cc_in.split(' ')
                addr1 = addrs[0].split('.')
                addr2 = addrs[1].split('.')
                diff = int(addr2[3]) - int(addr1[3])
                #print(diff)   
                hosts = []            
                for x in range(0, (diff + 1)):
                    hosts.append(addr1[0] + '.' + addr1[1] + '.' + addr1[2] + '.' + str(int(addr1[3]) + x))
                    #print(x , ' ' , hosts[x])
                break
            else:
                print('Invalid input.')    
    return(hosts)

def main():
    if (os.path.isfile('./hosts.json') == False):
        no_config()        

    hosts = found_config()
    ping(hosts)

if __name__ == "__main__":
    main()