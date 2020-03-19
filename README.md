# IntrepidAgent
## Monitor, record and report on network device statuses.

### What is IntrepidAgent?

**IntrepidAgent** is a Python script that will ping a user-specified set of hosts and report on those that are offline. Hosts may be set through a configuration file in json format. This script is complete with an interactive CLI to prompt users to make any changes desired to the configuration.

### Using IntrepidAgent

    Usage: main.py [OPTION]
    Monitor, record and report on network device statuses.

    With no OPTION specified, run as verbose in terminal.

     -q, --quiet           suppress automatic printing of status information
     -c, --configure       enter CLI configuration mode
     -v, --version         output version information and exit
     -h, --help            display this help and exit

    To run as a background process on Linux, use 'main.py &'

### Configuring IntrepidAgent

The interactive CLI will prompt users to create configuration files if none exist. If all configuration and log files exist in the current working directory, users may choose to append to these files or overwrite them. Users will be guided through a configuration process by first specifying which file they would like to configure. Configuration options for ICMP, email addresses and polling options are implemented in this solution. Files may be configured individually or all at once. 

#
As of current, the following configuration options are available:
* Poll hosts through ICMP
* Specifying an individual, list or range of IPv4 addresses.
  * Limited to addresses in the same /24 subnet via range.
* Specifying an individual or list of email addresses.
* Specifying the wait time between polls and the amount of polls held before a host is marked as offline.
#

## Q & A
### What exactly does IntrepidAgent do?

**IntrepidAgent** polls hosts using ICMP to determine their online status. Polls are sent out at a user-specified interval and after hosts are offline for a user-specified amount of polls, they will be marked as offline. This event will be logged and an email notification will be sent out to all specified recipients.

### Can I automate IntrepidAgent to run without user intervention?

Yes, the script may be ran quietly or as a background process. No user intervention is required as long as all required files exist in the working directory.
