%define version 1.6.1
%define release 0contrail0
Name:    librdkafka
Version: 1.6.1
Release: 0contrail0%{?dist}
%define soname 1

Summary: The Apache Kafka C library
Group:   Development/Libraries/C and C++
License: BSD-2-Clause
URL:     https://github.com/confluentinc/librdkafka
Source:	 https://github.com/edenhill/librdkafka/archive/v%{version}.tar.gz

BuildRequires: zlib-devel libstdc++-devel gcc >= 4.1 gcc-c++ cyrus-sasl-devel libzstd-devel rapidjson-devel
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%define _source_payload w9.gzdio
%define _binary_payload w9.gzdio

%description
librdkafka is the C/C++ client library implementation of the Apache Kafka protocol, containing both Producer and Consumer support.


%package -n %{name}%{soname}
Summary: The Apache Kafka C library
Group:   Development/Libraries/C and C++
Requires: zlib libstdc++ cyrus-sasl
# openssl libraries were extract to openssl-libs in RHEL7
Requires: openssl-libs >= 1.0.2
BuildRequires: python3
BuildRequires: openssl-devel >= 1.0.2


%description -n %{name}%{soname}
librdkafka is the C/C++ client library implementation of the Apache Kafka protocol, containing both Producer and Consumer support.


%package -n %{name}-devel
Summary: The Apache Kafka C library (Development Environment)
Group:   Development/Libraries/C and C++
Requires: %{name}%{soname} = %{version}

%description -n %{name}-devel
librdkafka is the C/C++ client library implementation of the Apache Kafka protocol, containing both Producer and Consumer support.

This package contains headers and libraries required to build applications
using librdkafka.

%global debug_package %{nil}
%prep
%setup -q -n %{name}-%{version}

# --install-deps will install missing dependencies that are not available
# through BuildRequires, such as libzstd, which will be linked statically.
%configure --install-deps --disable-lz4-ext --disable-c11threads --disable-zstd

%build
cat config.log
make HAVE_STRLCPY=0
examples/rdkafka_example -X builtin.features

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} make install

%clean
rm -rf %{buildroot}

%post   -n %{name}%{soname} -p /sbin/ldconfig
%postun -n %{name}%{soname} -p /sbin/ldconfig

%files -n %{name}%{soname}
%defattr(444,root,root)
%{_libdir}/librdkafka.so.%{soname}
%{_libdir}/librdkafka++.so.%{soname}
%defattr(-,root,root)
%doc %{_docdir}/librdkafka/README.md
%doc %{_docdir}/librdkafka/LICENSE
%doc %{_docdir}/librdkafka/CONFIGURATION.md
%doc %{_docdir}/librdkafka/INTRODUCTION.md
%doc %{_docdir}/librdkafka/STATISTICS.md
%doc %{_docdir}/librdkafka/CHANGELOG.md
%doc %{_docdir}/librdkafka/LICENSES.txt

%defattr(-,root,root)
#/usr/local/bin/rdkafka_example
#%/usr/local/bin/rdkafka_performance


%files -n %{name}-devel
%defattr(-,root,root)
%{_includedir}/librdkafka
%defattr(444,root,root)
%{_libdir}/librdkafka.a
%{_libdir}/librdkafka.so
%{_libdir}/librdkafka++.a
%{_libdir}/librdkafka++.so
%{_libdir}/pkgconfig/rdkafka++.pc
%{_libdir}/pkgconfig/rdkafka.pc
%{_libdir}/pkgconfig/rdkafka-static.pc
%{_libdir}/pkgconfig/rdkafka++-static.pc

%changelog
* Thu Apr 09 2015 Eduard Iskandarov <e.iskandarov@corp.mail.ru> 0.8.6-0
- 0.8.6 simplify build process

* Fri Oct 24 2014 Magnus Edenhill <rdkafka@edenhill.se> 0.8.5-0
- 0.8.5 release

* Mon Aug 18 2014 Magnus Edenhill <rdkafka@edenhill.se> 0.8.4-0
- 0.8.4 release

* Mon Mar 17 2014 Magnus Edenhill <vk@edenhill.se> 0.8.3-0
- Initial RPM package
