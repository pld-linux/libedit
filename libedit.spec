%define	snap	20041207
Summary:	Editline Library
Name:		libedit
Version:	2.9
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://www.thrysoee.dk/editline/%{name}-%{snap}-%{version}.tar.gz
# Source0-md5:	93bac6ac3451bd1f2066614992154e02
URL:		http://www.thrysoee.dk/editline/
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Port of the NetBSD Editline library (libedit). This Berkeley-style
licensed command line editor library provides generic line editing,
history, and tokenization functions, similar to those found in GNU
Readline.

%package devel
Summary:	Header files and develpment documentation for libedit
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Port of the NetBSD Editline library (libedit). This Berkeley-style
licensed command line editor library provides generic line editing,
history, and tokenization functions, similar to those found in GNU
Readline.

%package static
Summary:	Static libedit library
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Port of the NetBSD Editline library (libedit). This Berkeley-style
licensed command line editor library provides generic line editing,
history, and tokenization functions, similar to those found in GNU
Readline.

%prep
%setup -q -n %{name}-%{snap}-%{version}

%build
LANG=C; export LANG
LC_ALL=C; export LC_ALL
CPPFLAGS="-I%{_includedir}/ncurses"
%configure
%{__make} -C src vi.h emacs.h common.h
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog THANKS
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_mandir}/man5/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*
%{_mandir}/man3/*
# conflict with heimdal, does heimdal use some internal libedit?
%exclude %{_mandir}/man3/editline*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
