# remirepo/fedora spec file for cassandra-cpp-driver
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit   d5152deeeb188c1a1cb285233ffd98c6e9261e0c
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    datastax
%global gh_project  cpp-driver
%global libname     libcassandra
%global soname      2

Name:          cassandra-cpp-driver
Summary:       DataStax C/C++ Driver for Apache Cassandra
Version:       2.7.1
Release:       1%{?dist}
License:       ASL 2.0
Group:         System Environment/Libraries

URL:           http://datastax.github.io/cpp-driver/
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{version}.tar.gz
%if 0%{?rhel} >= 8
Patch0: ring_buffer_bio.hpp.el8.patch
%endif

BuildRequires: cmake >= 2.6.4
BuildRequires: libuv-devel
%if 0%{?rhel} < 8
BuildRequires: openssl-devel <= 1:1.0.2o
%else
BuildRequires: compat-openssl10 <= 1:1.0.2o
BuildRequires: compat-openssl10-debugsource <= 1:1.0.2o
%endif

%if 0%{?rhel} >= 8
%define CXXFLAGS -Wno-implicit-fallthrough -Wno-error=maybe-uninitialized -Wno-error=class-memaccess -Wno-error=unused-function  -Wno-error=deprecated-declarations -Wno-error=implicit-function-declaration
%endif

%description
%{summary}.

A modern, feature-rich, and highly tunable C/C++ client library for
Apache Cassandra (1.2+) and DataStax Enterprise (3.1+) using exclusively
Cassandra s native protocol and Cassandra Query Language v3.


%package devel
Summary:    Header files and development libraries for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}.


%prep
%setup -q -n %{gh_project}-%{version}
%if 0%{?rhel} >= 8
%patch0 -p0
%endif
find examples -name .gitignore -exec rm {} \; -print


%build
export CXXFLAGS="%{?CXXFLAGS} $RPM_OPT_FLAGS"
%cmake

make %{_smp_mflags}


%install
export CXXFLAGS="%{?CXXFLAGS} $RPM_OPT_FLAGS"
make install DESTDIR="%{buildroot}"

rm %{buildroot}%{_libdir}/%{libname}_static.a
rm %{buildroot}%{_libdir}//pkgconfig/cassandra_static.pc


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%{_libdir}/%{libname}.so.%{soname}*


%files devel
%doc *.md
%doc examples
%{_libdir}/%{libname}.so
%{_includedir}/cassandra.h
%{_libdir}/pkgconfig/cassandra.pc


%changelog
* Mon May 22 2017 Remi Collet <remi@remirepo.net> - 2.7.0-1
- update to 2.7.0
- open https://datastax-oss.atlassian.net/browse/CPP-470 - BC break

* Mon Mar 13 2017 Remi Collet <remi@fedoraproject.org> - 2.6.0-2
- add upstream patch for EL-6

* Fri Mar 10 2017 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- open https://datastax-oss.atlassian.net/browse/CPP-442
  Broken build on EL-6 64-bit

* Mon Mar  6 2017 Remi Collet <remi@fedoraproject.org> - 2.5.0-2
- use -Wno-implicit-fallthrough, workaround for GCC 7
- open https://datastax-oss.atlassian.net/browse/CPP-438
  Broken build with GCC 7 and OpenSSL 1.1

* Fri Oct 21 2016 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- update to 2.5.0

* Sat Sep  3 2016 Remi Collet <remi@fedoraproject.org> - 2.4.3-1
- update to 2.4.3

* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 2.4.2-1
- update to 2.4.2

* Fri Jun 10 2016 Remi Collet <remi@fedoraproject.org> - 2.4.1-1
- update to 2.4.1

* Tue Jun  7 2016 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- update to 2.4.0

* Fri Feb 12 2016 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- update to 2.2.2

* Thu Nov 26 2015 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- update to 2.2.1

* Thu Aug 13 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
<<<<<<< HEAD
- initial package
=======
- initial package
>>>>>>> ba0f526 (improvements for rocky9)
