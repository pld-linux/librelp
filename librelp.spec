#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	The Reliable Event Logging Protocol library
Summary(pl.UTF-8):	Biblioteka Reliable Event Logging Protocol
Name:		librelp
Version:	1.8.0
Release:	1
License:	GPL v3+ or commercial
Group:		Libraries
Source0:	https://download.rsyslog.com/librelp/%{name}-%{version}.tar.gz
# Source0-md5:	dc605ac0e1efa5aac8fd7f9561317cef
URL:		https://www.rsyslog.com/librelp/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	gnutls-devel >= 2.0.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires:	gnutls-libs >= 2.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Librelp is an easy to use library for the RELP protocol. RELP (stands
for Reliable Event Logging Protocol) is a general-purpose, extensible
logging protocol.

%description -l pl.UTF-8
Librelp to łatwa w użyciu biblioteka do protokołu RELP. RELP (Reliable
Event Logging Protocol - protokół wiarygodnego logowania zdarzeń).

%package devel
Summary:	Development files for librelp library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki librelp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files needed to develop applications
using librelp.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia aplikacji z
użyciem biblioteki librelp.

%package static
Summary:	Static librelp library
Summary(pl.UTF-8):	Statyczna biblioteka librelp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static librelp library.

%description static -l pl.UTF-8
Statyczna biblioteka librelp.

%prep
%setup -q

# strip common GPL text
%{__sed} -i -e '/^---------/,$ d' COPYING

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--disable-tls-openssl

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog doc/*.html
%attr(755,root,root) %{_libdir}/librelp.so.*.*.*
%attr(755,root,root) %{_libdir}/librelp.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librelp.so
%{_includedir}/librelp.h
%{_pkgconfigdir}/relp.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/librelp.a
%endif
