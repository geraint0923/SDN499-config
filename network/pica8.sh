#!/bin/bash
# boot
# use one of the following method to turn the switch into OpenFlow mode
# 1. use command line tool to configure the mode
# sudo picos_boot
# 2
# 129.105.44.58/24
# 129.105.44.193
# service picos restart
#
# 2. modify the configuration file to change the mode
# vim /etc/picos/picos_start.conf
# picos_start=ovs


############ configure ##########
# add physical ports to the Open Virtual Switch on Pica8
ovs-vsctl add-br br0 -- set bridge br0 datapath_type=pica8
ovs-vsctl add-port br0 te-1/1/1 vlan_mode=trunk tag=1 -- set interface te-1/1/1 type=pica8
ovs-vsctl add-port br0 te-1/1/2 vlan_mode=trunk tag=1 -- set interface te-1/1/2 type=pica8
ovs-vsctl add-port br0 te-1/1/3 vlan_mode=trunk tag=1 -- set interface te-1/1/3 type=pica8

ovs-vsctl add-port br0 ge-1/1/1 -- set interface ge-1/1/1 type=pica8
ovs-vsctl add-port br0 ge-1/1/2 -- set interface ge-1/1/2 type=pica8
ovs-vsctl add-port br0 ge-1/1/3 -- set interface ge-1/1/3 type=pica8

# set the IP and port of the remote controller
ovs-vsctl set-controller br0 tcp:129.105.44.99:6633
