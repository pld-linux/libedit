# TODO: resolve conflict with heimdal (use shared editline in heimdal?)
# remove (static-only) libeditline (+devel) from heimdal
%define	snap	20041207
Summary:	Editline Library
Summary(pl):	Biblioteka Editline (edytor linii polece�)
Name:		libedit
Version:	2.9
Release:	1
Epoch:		0
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

%description -l pl
Port biblioteki Editline z NetBSD (libedit). Jest to biblioteka
edytora linii polece� na licencji w stylu BSD udost�pniaj�ca
funkcjonalno�� og�lnego modyfikowania linii, historii oraz tokenizacji
podobn� do obecnych w GNU Readline.

%package devel
Summary:	Header files and development documentation for libedit
Summary(pl):	Pliki nag��wkowe i dokumentacja programisty do libedit
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and development documentation for libedit.

%description devel -l pl
Pliki nag��wkowe i dokumentacja programisty do libedit.

%package static
Summary:	Static libedit library
Summary(pl):	Statyczna biblioteka libedit
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static libedit library.

%description static -l pl
Statyczna biblioteka libedit.

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
# to be removed after removing libeditline from heimdal?
%exclude %{_mandir}/man3/editline*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
