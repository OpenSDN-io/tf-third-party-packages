%if 0%{!?amzn}
%define distnum %(/usr/lib/rpm/redhat/dist.sh --distnum)
%endif

%global gh_owner    datastax
%global gh_project  cpp-driver

Name:    cassandra-cpp-driver
Epoch:   1
Version: 2.17.1
Release: 1%{?dist}
Summary: DataStax C/C++ Driver for Apache Cassandra and DataStax Products

Group: Development/Tools
License: Apache 2.0
URL:           http://datastax.github.io/cpp-driver/
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{version}.tar.gz
Source1: cassandra.pc.in
Source2: cassandra_static.pc.in

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%if 0%{?distnum} >= 8
%define cmakecmd cmake
BuildRequires: cmake >= 3.5.0
%else
BuildRequires: cmake3 >= 3.5.0
%define cmakecmd cmake3
%endif

BuildRequires: libuv-devel >= 1.42.0
BuildRequires: openssl-devel >= 0.9.8e

%description
A modern, feature-rich, and highly tunable C/C++ client library for Apache
Cassandra and DataStax Products using Cassandra's native protocol and Cassandra
Query Language along with extensions for DataStax Products.

%package devel
Summary: Development libraries for ${name}
Group: Development/Tools
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: libuv >= 1.42.0
Requires: openssl >= 0.9.8e
Requires: krb5-libs
Requires: pkgconfig

%description devel
Development libraries for %{name}

%prep
%setup -qn %{gh_project}-%{version}

%build
export CFLAGS='%{optflags}'
export CXXFLAGS='%{optflags}'
%{cmakecmd} -DCMAKE_BUILD_TYPE=RELEASE -DCASS_BUILD_STATIC=ON -DCASS_INSTALL_PKG_CONFIG=OFF -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_libdir} .
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}/%{_libdir}/pkgconfig
sed -e "s#@prefix@#%{_prefix}#g" \
    -e "s#@exec_prefix@#%{_exec_prefix}#g" \
    -e "s#@libdir@#%{_libdir}#g" \
    -e "s#@includedir@#%{_includedir}#g" \
    -e "s#@version@#%{version}#g" \
    %SOURCE1 > %{buildroot}/%{_libdir}/pkgconfig/cassandra.pc
sed -e "s#@prefix@#%{_prefix}#g" \
    -e "s#@exec_prefix@#%{_exec_prefix}#g" \
    -e "s#@libdir@#%{_libdir}#g" \
    -e "s#@includedir@#%{_includedir}#g" \
    -e "s#@version@#%{version}#g" \
    %SOURCE2 > %{buildroot}/%{_libdir}/pkgconfig/cassandra_static.pc

%clean
rm -rf %{buildroot}

%check
# make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README.md LICENSE.txt
%{_libdir}/*.so
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%doc README.md LICENSE.txt
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Mar 13 2017 Michael Penick <michael.penick@datastax.com> - 2.6.0-1
- release
