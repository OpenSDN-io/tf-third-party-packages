#!/bin/bash
# SPDX-License-Identifier: LGPL-2.1+
# ~~~
#   runtest.sh of net-snmp
#   Description:  net-snmp tests
#
#   Author: Susant Sahani <susant@redhat.com>
#   Copyright (c) 2018 Red Hat, Inc.
# ~~~

# Include Beaker environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGE_NET_SNMP="net-snmp"
PACKAGE_NET_SNMP_UTILS="net-snmp-utils"

NET_SNMP_CONF_FILE="/etc/snmp/snmpd.conf"

rlJournalStart
    rlPhaseStartSetup
        rlAssertRpm $PACKAGE_NET_SNMP
        rlAssertRpm $PACKAGE_NET_SNMP_UTILS

        rlRun "systemctl stop firewalld" 0,5
        rlRun "setenforce 0" 0,1

        rlRun "[ -e /sys/class/net/veth-test ] && ip link del veth-test" 0,1
        rlRun "cp net-snmp-tests.py /usr/bin/"

        rlFileBackup "$NET_SNMP_CONF_FILE"
        rlRun "cp snmpd.conf $NET_SNMP_CONF_FILE"

    rlPhaseEnd

    rlPhaseStartTest
        rlLog "Starting net-snmp tests ..."
        rlRun "/usr/bin/python3 /usr/bin/net-snmp-tests.py"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "rm /usr/bin/net-snmp-tests.py  $NET_SNMP_CONFIG_FILE"
        rlRun "systemctl daemon-reload"
        rlRun "[ -e /sys/class/net/veth-test ] && ip link del veth-test" 0,1
        rlFileRestore
        rlRun "setenforce 1" 0,1
        rlLog "net-snmp tests done"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd

rlGetTestState
