import os
from datetime import datetime

#def log(msg):
#    logging.basicConfig(filename='./logs/status.log', 
#        format='%(asctime)s - %(message)s', datefmt='%b-%d-%y %H:%M:%S')
#    logging.warning(msg)


def log(msg):

    now = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    msg = str(msg)

    with open('./logs/status.log', 'a') as logfile:
        msg = f'[{now}] {msg}\n'
        logfile.write(msg)
        logfile.close()
        
        return
