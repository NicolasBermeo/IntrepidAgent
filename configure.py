import sys
import os
import json
import string
import socket
import re

# --- COMMON CONFIGURATION FUNCTIONS ---
'''
    The following functions are common between all specific configuration functions.

    init_config() is used to prompt users for what they'd like to configure and calls 
    other functions from there.
        It does not return anything and instead loops infinitely until option 5 (exit) is selected.

    config_base() is used to prompt users to select if they would like to overwrite or append to 
    configuration files. It takes a string value (c_type)that specifies the configuration type used.
        It returns the boolean variables append and back that are used to either append to the config 
        file or return to the init_config() function, based on user input.
    
    set_config() is used to apply modifications to configuration files. It will verify that a list
    element is not already present before writing it to the file. These files are in json format.
    It takes a list of elements, a boolean value (append) that specifies how to write to the file, 
    and a string value (c_type) that specifies the configuration type used.
        It does not return any value.
    
    get_config() reads the json configuration files and writes it to a list. It takes a string value
    (c_type) that specifies the configuration type used.
        It returns the list containing elements from the configuration file selected.

'''
# --------------------------------------
def init_config():
    ic_in = 0

    while (True):
        ic_in = input('\n\n' +
            '##########################\n' +
            '#                        #\n' +
            '#   Configuration Mode   #\n' + 
            '#                        #\n' +
            '##########################\n\n' +
            'Welcome to the interactive CLI configuration mode!\n' +
            'To begin, please select one of the following options:\n\n' +
            ' 1: Configure host addresses\n' +
            ' 2: Configure email addresses\n' +
            ' 3: Configure ICMP polling\n' +
            ' 4: Configure Email Authentication\n' +
            ' 5: Configure all\n' +
            ' 6: Exit\n\n')
        
        if (ic_in == '1'):            
            host_config()
        elif (ic_in == '2'):            
            mail_config()
        elif (ic_in == '3'):            
            poll_config()
        elif (ic_in == '4'):            
            auth_config()
        elif (ic_in == '5'):      
            host_config()
            mail_config()
            poll_config()
            auth_config()
        elif (ic_in == '6'):
            print('Exiting...')
            sys.exit(0)

def config_base(c_type):    
    cb_in = 0
    append = False
    back = False

    prompt = str('\n\n' +
                '##########################\n' +
                '#                        #\n' +
                '#   ' + string.capwords(c_type) + ' Configuration   #\n' + 
                '#                        #\n' +
                '##########################\n\n' + 
                'Please select one of the following options:\n' +
                ' 1: Create a new configuration file\n' +
                ' 2: Append to an existing configuration file\n' +
                ' 3: Back\n' +
                ' 4: Exit\n\n')

    path = str('./config/' + c_type + '.json')

    while (True):
        cb_in = input(prompt)

        if (cb_in == '1'):
            print('Create new ', c_type, ' config.')

            if (os.path.isfile(path) == True):                
                cb_in = input('\n\nAn existing ' + c_type + ' configuration file has been found at:\n' + os.getcwd() +
                    '\config\n\nWould you like to overwrite this?\n' +
                    ' 1: Yes\n' +
                    ' 2: No\n\n')
                if (cb_in == '1'):
                    break
                elif (cb_in == '2'):
                    back = True
                    return(append, back)
            break
        elif (cb_in == '2'):
            print('Append another host(s) to config.')

            if (os.path.isfile(path) == False):                
                print('\n\nAn existing ' + c_type + ' configuration file could not be found at:\n' + os.getcwd() +
                    '/config\n\n')
                back = True
                return(append, back)

            append = True
            break
        elif (cb_in == '3'):
            print('Call last function')
            back = True
            return(append, back)
        elif (cb_in == '4'):
            print('Exiting...')
            sys.exit(0)

    return(append, back)

def set_config(elements, append, c_type):

    path = str('./config/' + c_type + '.json')
    if (append == True):
        tmp_list = get_config(c_type)

        for x in range (0, int(len(elements))):           
            if (elements[x] not in tmp_list):
                tmp_list.append(elements[x])

        elements = tmp_list

    with open(path, 'w+') as outfile:
        json.dump(elements, outfile)

def get_config(c_type):
    path = str('./config/' + c_type + '.json')

    with open(path) as infile:
        elements = json.load(infile)
    return(elements)
# --------------------------------------



# --- HOST CONFIGURATION FUNCTIONS ---
'''
    This function is used to configure host.json.

    host_config() prompts the user for addresses they would like to add to the file, calling config_base() to
    retrieve the append and back boolean variables used to navigate the function and manage writing to the file.
        It passes a list containing all user-specified hosts to set_config(), but only if they are all legal 
        and no errors have occured due to invalid input. Errors cause the function to return back to init_config() 
        so they user may try again.
'''
# ------------------------------------
def host_config():

    append, back = config_base('host')
    if (back == True):
        return

    addr_in = input('Please enter a single, list or range of IPv4 addresses.\n' +
    'For a list, separate using commas. For a range, use dashes.\n' +
    'Please note that a range of addresses must be in the same /24 subnet.\n\n')
                
    addr_in = addr_in.replace(' ', '')
    hosts = []           

    if (',' in addr_in and '-' not in addr_in):
        #addr_in = addr_in.replace(',', ' ')
        addrs = addr_in.split(',')
        for x in range(0, int(len(addrs))):
            try:
                socket.inet_aton(addrs[x])
                hosts.append(addrs[x])
            except (socket.error, OSError, ValueError):
                print('Invalid address at position ' , x+1)
                return
        
    elif ('-' in addr_in and ',' not in addr_in):
        #addr_in = addr_in.replace('-', ' ')
        addrs = addr_in.split('-')
        addr1 = addrs[0].split('.')
        addr2 = addrs[1].split('.')

        try:
            diff = int(addr2[3]) - int(addr1[3])
        except (OSError, ValueError, IndexError):
            print('Invalid input.')
            return
            
                    
        for x in range(0, (diff + 1)):
            try:
                socket.inet_aton(addr1[0] + '.' + addr1[1] + '.' + addr1[2] + '.' + str(int(addr1[3]) + x))
                hosts.append(addr1[0] + '.' + addr1[1] + '.' + addr1[2] + '.' + str(int(addr1[3]) + x))
            except (socket.error, OSError, ValueError):
                print('Invalid address at index ' , x+1)
                return            
    else:
        try:
            socket.inet_aton(addr_in)
            hosts = [addr_in]
        except (socket.error, OSError, ValueError):
            print('Invalid input.')
            return

    set_config(hosts, append, 'host')
    
    return
# ------------------------------------



# --- EMAIL CONFIGURATION FUNCTIONS ---
'''
    These functions are used to configure mail.json and auth.json.    

    mail_config() prompts the user for addresses they would like to add to the file, calling config_base() to
    retrieve the append and back boolean variables used to navigate the function and manage writing to the file.
        It passes a list containing all user-specified email addresses to set_config(), but only if they are all 
        legal and no errors have occured due to invalid input. Errors cause the function to return back to 
        init_config() so they user may try again.
    
    auth_config() prompts the user for the email address and password to be used when sending status updates
    via email. config_base() is called to retrieve the append and back boolean variables used to navigate
    the function and manage writing to the file.
        It passes a list containing the email address and password to set_config() to update the associated
        file.
'''
# -------------------------------------
def mail_config():

    append, back = config_base('mail')
    if (back == True):
        return

    mail_in = input('Please enter a list of e-mail addresses.\n' +
			'Separate list entries with commas.\n\n')

    mail_in = mail_in.replace(' ', '')
    mail_in = mail_in.lower()

    emails = []

    regex = re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')

    if (',' in mail_in):
        #mail_in = mail_in.replace(',', ' ')
        addrs = mail_in.split(',')
        for x in range(0, int(len(addrs))):
            try:
                if(regex.fullmatch(addrs[x])):
                    emails.append(addrs[x])
            except IndexError:
                print('Invalid address at index ' , x+1)
                return
    else:
        try:
            if(regex.fullmatch(mail_in)):
                emails.append(mail_in)
            else:
                print('Invalid input.')
        except IndexError:
            print('Invalid input.')
            return        
    
    set_config(emails, append, 'mail')

    return

def auth_config():
    append, back = config_base('auth')

    if (back == True):
        return
    if (append == True):
        print('Cannot append to an auth configuration file. Please select another option.')
        return

    auth_in = input('Please enter the email address used to send status updates:\n\n')
    regex = re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')

    auth = []

    try:
        if(regex.fullmatch(auth_in)):
            auth.append(auth_in)
        else:
            print('Invalid input.')
    except IndexError:
        print('Invalid input.')
        return
    
    auth_in = input('Please enter the password used for the specified email address:\n\n')
    auth.append(auth_in)

    set_config(auth, append, 'auth')

    return
# -------------------------------------



# --- POLL CONFIGURATION FUNCTIONS ---
'''
    This function is used to configure poll.json.    

    poll_config() prompts the user for an integer value describing the time (in seconds) to wait between
    host polls. config_base() is called to retrieve the append and back boolean variables used to navigate
    the function and manage writing to the file.
        It passes a list containing the integer value to set_config(), but only if the input is a valid
        integer greater than or equal to 0. Errors cause the function to return back to init_config() so
        the user may try again.
'''
# ------------------------------------
def poll_config():

    append, back = config_base('poll')
    poll = []

    if (back == True):
        return
    if (append == True):
        print('Cannot append to a poll configuration file. Please select another option.')
        return
        
    try:        
        poll_in = int(input('Please specify the wait time (in seconds) between host polls:\n\n'))
        if (poll_in < 0):
            print('Invalid input. Values must be greater than or equal to 0.')
            return
        poll.append(poll_in)

        poll_in = int(input('Please specify the number of polls (integer value) before a host is ' +
        'marked as down:\n\n'))
        if (poll_in < 0):
            print('Invalid input. Values must be greater than or equal to 0.')
            return
        poll.append(poll_in)
    except (TypeError, ValueError):
        print('Invalid input. Values must be integers.')
        return    
    
    set_config(poll, append, 'poll')

    return
# ------------------------------------
