#!/usr/bin/python

"""
This example shows how to add an interface (for example a real
hardware interface) to a network after the network is created.
"""

import re

from mininet.cli import CLI
from mininet.log import setLogLevel, info, error
from mininet.net import Mininet
from mininet.link import Intf
from mininet.topolib import TreeTopo
from mininet.util import quietRun
from mininet.node import RemoteController, OVSKernelSwitch

def checkIntf( intf ):
    "Make sure intf exists and is not configured."
    if ( ' %s:' % intf ) not in quietRun( 'ip link show' ):
        error( 'Error:', intf, 'does not exist!\n' )
        exit( 1 )
    ips = re.findall( r'\d+\.\d+\.\d+\.\d+', quietRun( 'ifconfig ' + intf ) )
    if ips:
        error( 'Error:', intf, 'has an IP address,'
               'and is probably in use!\n' )
        exit( 1 )

if __name__ == '__main__':
    setLogLevel( 'info' )

    intfName = 'eth1'
    info( '*** Checking', intfName, '\n' )
    checkIntf( intfName )

    info( '*** Creating network\n' )
    net = Mininet()

#   change the dpid when being used on different virtual machines to make sure there is no conflict
    s1 = net.addSwitch('s1', dpid='00:00:00:00:00:02')
    net.addController('c1', controller=RemoteController, ip='10.0.66.1', port=6633)

#   change the host name and ip when being used on different virtual machines
    h1 = net.addHost('h1', ip='10.0.23.21/24')
    h2 = net.addHost('h2', ip='10.0.23.22/24')
    h3 = net.addHost('h3', ip='10.0.23.23/24')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)

    info( '*** Adding hardware interface', intfName, 'to switch',
          s1.name, '\n' )
    _intf = Intf( intfName, node=s1)

    info( '*** Note: you may need to reconfigure the interfaces for '
          'the Mininet hosts:\n', net.hosts, '\n' )

    net.start()
    CLI( net )
    net.stop()
