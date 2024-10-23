version=$(shell lsb_release -r | cut -f2 -d":" | cut -f1 -d".")
print-%  : ; @echo $* = $($*)

RPM_DIR   := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
GIT_ROOT     := $(RPM_DIR:/upstream/rpm/=)
BUILD_BASE   ?= $(GIT_ROOT)/..

SPEC_DIR     := $(RPM_DIR)/specs
SPEC_TARGETS := $(notdir $(wildcard $(SPEC_DIR)/*))
UTILS_DIR    := $(RPM_DIR)/utils

OS_PLATFORM_ID ?= $(shell cat /etc/os-release | grep '^PLATFORM_ID=' | cut -d = -f 2 | sed  's/\"//g')

RPMBUILD_FLAGS ?=
BUILDDEP_FLAGS ?=
ifeq ($(OS_PLATFORM_ID), platform:el8)
	RPMBUILD_FLAGS += --define "__python %__python2"
	RPMBUILD_FLAGS += --define "__brp_mangle_shebangs %{nil}"
	RPMBUILD_FLAGS += --define "debug_package %{nil}"
	BUILDDEP_FLAGS += --define "__python %__python2"
endif


all: $(SPEC_TARGETS)

list:
	@echo $(sort $(SPEC_TARGETS))

prep:
	@echo "Build base is $(BUILD_BASE)"
	mkdir -p $(BUILD_BASE)/BUILD; \
	mkdir -p $(BUILD_BASE)/SRPMS; \
	mkdir -p $(BUILD_BASE)/RPMS;

clean_srpms:
	@test -d $(BUILD_BASE)/SRPMS && rm $(BUILD_BASE)/SRPMS/*.src.rpm

clean_rpms:
	@test -d $(BUILD_BASE)/RPMS && rm $(BUILD_BASE)/RPMS/*.rpm

clean: clean_srpms clean_rpms
	::

touch_all:
	find . -exec touch {} +

#boost-1.53.0: RPMBUILD_FLAGS += --without=openmpi --without=mpich

$(SPEC_TARGETS): prep
	@echo "contrail-third-party-packages: prepare sources for $@"
	spectool -g $(RPMBUILD_FLAGS) $(SPEC_DIR)/$@/$@.spec -C $(SPEC_DIR)/$@/
	echo "docker env: contrail-third-party-packages: make $@" ; \
	echo "DBG: $@: BUILDDEP_FLAGS=$(BUILDDEP_FLAGS) BUILD_BASE=$(BUILD_BASE)" ; \
	yum-builddep -y $(BUILDDEP_FLAGS) \
		--define "_topdir $(BUILD_BASE)" \
		--define "_sourcedir $(SPEC_DIR)/$@" \
		specs/$@/$@.spec ; \
	echo "DBG: $@: RPMBUILD_FLAGS=$(RPMBUILD_FLAGS)" ; \
	rpmbuild -bb $(RPMBUILD_FLAGS) \
		--define "_buildrootdir $$(mktemp -d)" \
		--define "_topdir $(BUILD_BASE)" \
		--define "_sourcedir $(SPEC_DIR)/$@" \
		specs/$@/$@.spec ; \
