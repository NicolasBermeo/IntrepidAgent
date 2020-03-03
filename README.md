# pipoller
## A simple Python script to ping hosts

### What is pipoller?

**pipoller** is a Python script that will ping a user-specified set of hosts and report on those that are offline. Hosts may be set through a configuration file in json format. This script is complete with an interactive CLI to prompt users to make any changes desired to the configuration.

### How can I configure pipoller?

The interactive CLI will prompt users to create a configuration file if none exists. If one does exist, users may choose to continue with the existing file in their working directory *or* create a new one to overwrite it. 

Users will be walked through a configuration process by first specifying a polling mode. Additional configuration may be prompted for in order to communicate using the specified mode. This may include a community string for SNMPv2c or an authentication key for SNMPv3. 

Finally, users will be asked to input either a list *or* range of host addresses. The configuration file will be complete after this point.

#
As of current, the following configuration options are available:
* Setting the polling mode to ICMP.
* Specifying a list or range of IP addresses.
  * Currently limited to addresses in the same /24 subnet via range.

The following configuration options are planned for future releases:
* Setting the polling mode to SNMPv1, SNMPv2c, & SNMPv3.
  * Configuring **pipoller** for these modes.
* Setting a range of addresses in varying subnets.
* Setting the wait time in between polls.
* Setting the number of offline responses before notifying an offline host.
#

### What exactly does pipoller do?

**pipoller** will use the established hosts list to continuously poll them, monitoring and recording offline activity. Currently, this process occurs every *30 seconds* and after *2 rounds* of offline responses, an email notification will be sent out to a user-specified list of addresses. 


