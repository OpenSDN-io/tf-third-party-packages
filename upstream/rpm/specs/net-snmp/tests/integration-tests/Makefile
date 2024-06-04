# SPDX-License-Identifier: LGPL-2.1+
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Makefile of /CoreOS/net-snmp
#   Description: Test if net-snmp working ok
#   Author: Susant Sahani<susant@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
export TEST=/CoreOS/net-snmp
export TESTVERSION=1.0
BUILT_FILES=
FILES=$(METADATA) runtest.sh Makefile PURPOSE
.PHONY: all install download clean
run: $(FILES) build
	./runtest.sh
build: $(BUILT_FILES)
	test -x runtest.sh || chmod a+x runtest.sh
clean:
	rm -f *~ $(BUILT_FILES)
include /usr/share/rhts/lib/rhts-make.include
$(METADATA): Makefile
	@echo "Owner:           Susant Sahani<susant@redhat.com>" > $(METADATA)
	@echo "Name:            $(TEST)" >> $(METADATA)
	@echo "TestVersion:     $(TESTVERSION)" >> $(METADATA)
	@echo "Path:            $(TEST_DIR)" >> $(METADATA)
	@echo "Description:     Test snmpd" >> $(METADATA)
	@echo "Type:            Sanity" >> $(METADATA)
	@echo "TestTime:        5m" >> $(METADATA)
	@echo "RunFor:          net-snmp" >> $(METADATA)
	@echo "Requires:        net=snmp" >> $(METADATA)
	@echo "Priority:        Normal" >> $(METADATA)
	@echo "License:         GPLv2" >> $(METADATA)
	@echo "Confidential:    no" >> $(METADATA)
	@echo "Destructive:     no" >> $(METADATA)
	@echo "Releases:        -Fedora 28" >> $(METADATA)
	rhts-lint $(METADATA)
