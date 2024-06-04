#!/usr/bin/env python3
# SPDX-License-Identifier: LGPL-2.1+
# ~~~
#   Description: Tests for snmpd
#
#   Author: Susant Sahani <susant@redhat.com>
#   Copyright (c) 2018 Red Hat, Inc.
# ~~~

import errno
import os
import sys
import time
import unittest
import subprocess
import signal
import shutil
import psutil
import socket
import platform
import re
from pyroute2 import IPRoute
from psutil import virtual_memory
from collections import OrderedDict

HOST='192.168.111.50'

def setUpModule():
    """Initialize the environment, and perform sanity checks on it."""

    if shutil.which('snmpd') is None:
        raise OSError(errno.ENOENT, 'snmpd not found')

    if shutil.which('snmpwalk') is None:
        raise OSError(errno.ENOENT, 'snmpwalk not found')

def tearDownModule():
        pass

class GenericUtilities():
    """Provide a set of utility functions start stop daemons. write config files etc """

    def StartSnmpd(self):
        """Start snmpd"""
        subprocess.check_output(['systemctl', 'start', 'snmpd'])

    def StopSnmpd(self):
        """Stop snmpd"""
        subprocess.check_output(['systemctl', 'stop', 'snmpd'])

    def SetupVethInterface(self):
        """Setup veth interface"""

        ip = IPRoute()

        ip.link('add', ifname='veth-test', peer='veth-peer', kind='veth')
        idx_veth_test = ip.link_lookup(ifname='veth-test')[0]
        idx_veth_peer = ip.link_lookup(ifname='veth-peer')[0]

        ip.link('set', index=idx_veth_test, address='12:11:12:13:14:18')
        ip.link('set', index=idx_veth_peer, address='22:21:22:23:24:29')
        ip.link('set', index=idx_veth_test, state='up')
        ip.link('set', index=idx_veth_peer, state='up')
        ip.addr('add', index=idx_veth_test, address='192.168.111.50')
        ip.addr('add', index=idx_veth_peer, address='192.168.111.51')

        ip.close()

    def TearDownVethInterface(self):
        ip = IPRoute()

        ip.link('del', index=ip.link_lookup(ifname='veth-test')[0])
        ip.close()

class SnmpdTests(unittest.TestCase, GenericUtilities):

    def setUp(self):
        self.SetupVethInterface()
        time.sleep(1)
        self.StartSnmpd()

    def tearDown(self):
        self.StopSnmpd()
        self.TearDownVethInterface()

    def test_UCD_SNMP_MIB_memory(self):
        ''' UCD-SNMP-MIB::memory '''

        subprocess.check_output(['snmpwalk', '-v2c', '-c' , 'public',  HOST,  'UCD-SNMP-MIB::memory'])

        meminfo=OrderedDict()
        with open('/proc/meminfo') as f:
            for line in f:
                meminfo[line.split(':')[0]] = line.split(':')[1].strip()

        output=subprocess.check_output(['snmpwalk', '-v2c', '-c' , 'public',  HOST,  'UCD-SNMP-MIB::memTotalReal.0']).rstrip().decode('utf-8')
        self.assertRegex(output, meminfo['MemTotal'])

    def test_SNMP_hrSWRunPath(self):
        """ process id """
        output=subprocess.check_output(['snmpwalk', '-v2c', '-c' , 'public',  HOST,  'HOST-RESOURCES-MIB::hrSWRunPath.1']).rstrip().decode('utf-8')
        self.assertRegex(output, 'systemd')

    def test_SNMP_IF_MIB_network_interface(self):
        """ verify network interface (1.3.6.1.2.1.2.2.1) SNMP variables """

        ip = IPRoute()

        subprocess.check_output(['snmpwalk', '-v2c', '-c', 'public', HOST, '1.3.6.1.2.1.2.2.1'])

        # 1.3.6.1.2.1.2.2.1.1 IF-MIB::ifIndex
        output=subprocess.check_output(['snmpwalk', '-v2c', '-c', 'public', HOST, '1.3.6.1.2.1.2.2.1.1']).rstrip().decode('utf-8')
        self.assertRegex(output, 'IF-MIB::ifIndex.1 = INTEGER: 1')

        # 1.3.6.1.2.1.2.2.1.1 IF-MIB::ifDescr
        output=subprocess.check_output(['snmpwalk', '-v2c', '-c', 'public', HOST, '1.3.6.1.2.1.2.2.1.2']).rstrip().decode('utf-8')
        for link in ip.get_links():
            self.assertRegex(output, link.get_attr('IFLA_IFNAME'))

        # IP-MIB::ipAdEntAddr 1.3.6.1.2.1.4.20.1.1
        output=subprocess.check_output(['snmpwalk', '-v2c', '-c', 'public', HOST, '1.3.6.1.2.1.4.20.1.1']).rstrip().decode('utf-8')
        for addr in ip.get_addr():
            if addr.get_attr('IFA_ADDRESS'):
                if addr.get_attr('IFA_ADDRESS') != '::1' and addr.get_attr('Ifamily') == 2:
                    self.assertRegex(output, addr.get_attr('IFA_ADDRESS'))

        # IF-MIB::ifPhysAddress. 1.3.6.1.2.1.2.2.1.6
        output=subprocess.check_output(['snmpwalk', '-v2c', '-c', 'public', HOST, '1.3.6.1.2.1.2.2.1.6']).rstrip().decode('utf-8')
        for link in ip.get_links():
            if link.get_attr('IFLA_ADDRESS') and link.get_attr('IFLA_ADDRESS') != '00:00:00:00:00:00':
                snmp_mac = re.sub(r'\b0+(\d)', r'\1', link.get_attr('IFLA_ADDRESS')).lstrip('0')
                self.assertRegex(output, snmp_mac)

        ip.close()

    def test_SNMP_MIB_2_System(self):
        """ verify RFC 1213 System (1.3.6.1.2.1.1) SNMP variables"""

        subprocess.check_output(['snmpwalk', '-v2c', '-c', 'public', HOST, '1.3.6.1.2.1.1']).rstrip().decode('utf-8')

        # 1.3.6.1.2.1.1.1 - sysDescr
        output=subprocess.check_output(['snmpwalk', '-v2c', '-c', 'public', HOST, '1.3.6.1.2.1.1.1']).rstrip().decode('utf-8')
        self.assertRegex(output, platform.machine())
        self.assertRegex(output, platform.node())
        self.assertRegex(output, platform.processor())
        self.assertRegex(output, platform.release())
        self.assertRegex(output, platform.version())

        # 1.3.6.1.2.1.1.2 - sysObjectID
        subprocess.check_output(['snmpwalk', '-v2c', '-c', 'public', HOST, '1.3.6.1.2.1.1.2'])

        # 1.3.6.1.2.1.1.3 - sysUpTime
        subprocess.check_output(['snmpwalk', '-v2c', '-c', 'public', HOST, '1.3.6.1.2.1.1.3'])

        # 1.3.6.1.2.1.1.4 - sysContact
        output=subprocess.check_output(['snmpwalk', '-v2c', '-c', 'public', HOST, '1.3.6.1.2.1.1.4']).rstrip().decode('utf-8')
        self.assertRegex(output, 'fedora-ci <fedoraci@fedoraproject.org>')

        # 1.3.6.1.2.1.1.5 - sysName
        output=subprocess.check_output(['snmpwalk', '-v2c', '-c', 'public', HOST, '1.3.6.1.2.1.1.5']).rstrip().decode('utf-8')
        self.assertRegex(output, socket.gethostname())

        # 1.3.6.1.2.1.1.6 - sysLocation
        output=subprocess.check_output(['snmpwalk', '-v2c', '-c', 'public', HOST, '1.3.6.1.2.1.1.6']).rstrip().decode('utf-8')
        self.assertRegex(output, 'Pune, IN')

    def test_basic_snmpwalk(self):
        """ verify snmpwalk getting success snmpwalk -v2c -c public localhost """

        subprocess.check_output(['snmpwalk', '-v2c', '-c', 'public', HOST])


if __name__ == '__main__':
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout,
                                                     verbosity=3))
