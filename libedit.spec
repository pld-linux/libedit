#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
%define	snap	20191231
%define	rel	1
Summary:	Editline Library
Summary(pl.UTF-8):	Biblioteka Editline (edytor linii poleceń)
Name:		libedit
Version:	3.1
Release:	1.%{snap}.%{rel}
Epoch:		0
License:	BSD
Group:		Libraries
Source0:	http://thrysoee.dk/editline/%{name}-%{snap}-%{version}.tar.gz
# Source0-md5:	2e22a51131de94ff2df24901f7cfe416
Patch0:		%{name}-man.patch
URL:		http://thrysoee.dk/editline/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Port of the NetBSD Editline library (libedit). This Berkeley-style
licensed command line editor library provides generic line editing,
history, and tokenization functions, similar to those found in GNU
Readline.

%description -l pl.UTF-8
Port biblioteki Editline z NetBSD (libedit). Jest to biblioteka
edytora linii poleceń na licencji w stylu BSD udostępniająca
funkcjonalność ogólnego modyfikowania linii, historii oraz tokenizacji
podobną do obecnych w GNU Readline.

%package devel
Summary:	Header files and development documentation for libedit
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja programisty do libedit
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	ncurses-devel
Conflicts:	heimdal-devel <= 0.6.3-1

%description devel
Header files and development documentation for libedit.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja programisty do libedit.

%package static
Summary:	Static libedit library
Summary(pl.UTF-8):	Statyczna biblioteka libedit
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static libedit library.

%description static -l pl.UTF-8
Statyczna biblioteka libedit.

%prep
%setup -q -n %{name}-%{snap}-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
LANG=C; export LANG
LC_ALL=C; export LC_ALL
CPPFLAGS="%{rpmcppflags} -I/usr/include/ncurses"
%configure \
	--enable-widec \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make} -C src vi.h emacs.h common.h
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# conflicts with readline
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/history.3
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libedit.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog THANKS
%attr(755,root,root) %{_libdir}/libedit.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedit.so.0
%{_mandir}/man5/editrc.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libedit.so
%{_includedir}/editline
%{_includedir}/histedit.h
%{_pkgconfigdir}/libedit.pc
%{_mandir}/man3/editline.3*
%{_mandir}/man3/el_*.3*
%{_mandir}/man3/history_end.3*
%{_mandir}/man3/history_init.3*
%{_mandir}/man3/history_w.3*
%{_mandir}/man3/history_wend.3*
%{_mandir}/man3/history_winit.3*
%{_mandir}/man3/tok_end.3*
%{_mandir}/man3/tok_init.3*
%{_mandir}/man3/tok_line.3*
%{_mandir}/man3/tok_reset.3*
%{_mandir}/man3/tok_str.3*
%{_mandir}/man3/tok_wend.3*
%{_mandir}/man3/tok_winit.3*
%{_mandir}/man3/tok_wline.3*
%{_mandir}/man3/tok_wreset.3*
%{_mandir}/man3/tok_wstr.3*
%{_mandir}/man7/editline.7*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libedit.a
%endif
