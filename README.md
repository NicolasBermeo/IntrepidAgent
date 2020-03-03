# pipoller
## A simple Python script to ping hosts

### What is pipoller?

**pipoller** is a Python script that will ping a user-specified set of hosts and report on those that are offline. Hosts may be set through a configuration file in json format. This script is complete with an interactive CLI to prompt users to make any changes desired to the configuration.

### How can I configure pipoller?

As of current, the following configuration options are available:
* Setting the polling mode to ICMP.
* Specifying a list or range of IP addresses.
  * Currently limited to addresses in the same /24 subnet.

The following configuration options are planned for future releases:
* Setting the polling mode to SNMPv1, SNMPv2c, & SNMPv3.
  * Configuring **pipoller** for these modes.
* 
