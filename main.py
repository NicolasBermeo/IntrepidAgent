import sys
import getopt
import os

from configure import init_config
from icmp import icmp

'''
##########################
#                        #
#   Accepted Arguments   #
#                        #
##########################
q   :   quiet
c   :   configure
h   :   help
v   :   version
'''

def main(argv):   
    
    try:
        opts, args = getopt.getopt(argv, 'hvqc', ['help','version','quiet','configure'])
    except getopt.GetoptError:
        print('Usage: main.py [OPTION] (see --help for more information.)\n')
        sys.exit(2)

    quiet = False

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('Usage: main.py [OPTION]\n' +
                'Monitor, record and report on network device statuses.\n\n' +
                'With no OPTION specified, run as verbose in terminal.\n\n' +
                ' -q, --quiet           suppress automatic printing of status information\n' +
                ' -c, --configure       enter CLI configuration mode\n' +
                ' -v, --version         output version information and exit\n' +
                ' -h, --help            display this help and exit\n\n' +
                'To run as a background process on Linux, use \'main.py &\'\n')
            sys.exit(0)
        elif opt in ('-v', '--version'):
            print('Version: 1.0.0\n')
            sys.exit(0)
        elif opt in ('-q', '--quiet'):
            print('Launching quietly in terminal...\n')
            quiet = True
            icmp(quiet)
            sys.exit(0)
        elif opt in ('-c', '--configure'):
            print('Launching CLI configuration mode...\n')
            init_config()
            sys.exit(0)
    
    print('Starting without an option...')
    icmp(quiet)


if __name__ == "__main__":
    main(sys.argv[1:])
