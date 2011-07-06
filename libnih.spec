Name:           libnih
Version:        1.0.1
Release:        6%{?dist}
Summary:        Lightweight application development library

Group:          System Environment/Libraries
License:        GPLv2
URL:            https://launchpad.net/libnih
Source0:        http://launchpad.net/libnih/1.0/1.0.1/+download/libnih-1.0.1.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf >= 2.62
BuildRequires:  gettext >= 0.17
BuildRequires:  automake >= 1.11
BuildRequires:  libtool >= 2.2.4
BuildRequires:  dbus-devel >= 1.2.16
BuildRequires:  expat >= 2.0.0
BuildRequires:  expat-devel >= 2.0.0

# Filter GLIBC_PRIVATE Requires:
%define _filter_GLIBC_PRIVATE 1


%description
libnih is a small library for C application development containing functions
that, despite its name, are not implemented elsewhere in the standard library
set.

libnih is roughly equivalent to other C libraries such as glib, except that its
focus is on a small size and intended for applications that sit very low in the
software stack, especially outside of /usr.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
sed -i 's:$(prefix)/lib:$(prefix)/%{_lib}:g' nih{,-dbus}/Makefile.am
autoreconf -i --force
%configure --disable-static --disable-rpath --libdir=/%{_lib}
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig


%check
#some tests fail in koji while pass in mock and local build
#to run make check use "--with check"
%if %{?_with_check:1}%{!?_with_check:0}
  make check
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README
%doc AUTHORS
%doc ChangeLog
%doc COPYING
/%{_lib}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc HACKING
%doc TODO
%{_mandir}/man1/nih-dbus-tool.1.gz
%{_bindir}/nih-dbus-tool
%{_includedir}/*
/%{_lib}/*.so
%{_libdir}/pkgconfig/*
%{_prefix}/share/aclocal/libnih.m4


%changelog
* Fri Feb 26 2010 Petr Lautrbach <plautrba@redhat.com> 1.0.1-6
- Add "make check" with "--with check" option

* Fri Feb 19 2010 Casey Dahlin <cdahlin@redhat.com> - 1.0.1-5
- Remove libtool patch as it is no longer necessary

* Wed Feb 10 2010 Casey Dahlin <cdahlin@redhat.com> - 1.0.1-4
- Fix explicit path issue
- Fix unused shlib dependency issue

* Sun Feb 07 2010 Casey Dahlin <cdahlin@redhat.com> - 1.0.1-3
- Require pkgconfig for -devel
- Fill out buildrequires

* Sat Feb 06 2010 Casey Dahlin <cdahlin@redhat.com> - 1.0.1-2
- Move library to /lib

* Fri Feb 05 2010 Casey Dahlin <cdahlin@redhat.com> - 1.0.1-1
- Initial packaging
