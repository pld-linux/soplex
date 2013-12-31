#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
#
Summary:	SoPlex - the Sequential object-oriented simPlex
Summary(pl.UTF-8):	SoPlex - sekwencyjna, zorientowana obiektowo metoda simplex
Name:		soplex
Version:	1.7.2
Release:	1
License:	ZIB Academic License (free for academic use) or commercial
Group:		Libraries
#Source0Download: http://soplex.zib.de/download.shtml
Source0:	http://soplex.zib.de/download/%{name}-%{version}.tgz
# NoSource0-md5:	8a4d3022286c2eced23613d435c9cd7f
# Cannot freely distribute sources or binaries according to license, 3c:
# "You must keep track of access to the Program (e.g., similar to the
#  registration procedure at ZIB)."
NoSource:	0
URL:		http://soplex.zib.de/
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	gmp-c++-devel
BuildRequires:	libstdc++-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SoPlex is a Linear Programming (LP) solver based on the revised
simplex algorithm. It features preprocessing techniques, exploits
sparsity, and offers primal and dual solving routines. It can be used
as a standalone solver reading MPS or LP format files as well as
embedded into other programs via a C++ class library.

%description -l pl.UTF-8
SoPlex to narzędzie do rozwiązywania problemów programowania liniowego
(LP) w oparciu o zmodyfikowany algorytm simplex. Obsługiwane są
techniki preprocesingu, wykorzystywana rzadkość, dostępne są procedury
rozwiązywania metodą prostą i dualną. Pakietu można używać jako
samodzielnego programu odczytującego pliki w formacie MPS lub LP, a
także w postaci osadzonej w innych programach poprzez bibliotekę klas
C++.

%package devel
Summary:	Header files for SoPlex library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SoPlex
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for SoPlex library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SoPlex.

%package static
Summary:	Static SoPlex library
Summary(pl.UTF-8):	Statyczna biblioteka SoPlex
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SoPlex library.

%description static -l pl.UTF-8
Statyczna biblioteka SoPlex.

%package apidocs
Summary:	SoPlex API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki SoPlex
Group:		Documentation

%description apidocs
API documentation for SoPlex library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki SoPlex.

%prep
%setup -q

%build
%if %{with static_libs}
%{__make} \
	CXX="%{__cxx}" \
	GMP=true \
	USRCXXFLAGS="%{rpmcxxflags} %{rpmcppflags}" \
	USRLDFLAGS="%{rpmldflags}" \
	VERBOSE=true
%endif

# abuse REPOSIT variable to append required libs to the end of link command
%{__make} \
	CXX="%{__cxx}" \
	GMP=true \
	LIBBUILDFLAGS="-shared -Wl,-soname,libsoplex.so.1" \
	REPOSIT="-lgmpxx -lgmp -lz" \
	SHARED=true \
	USRCXXFLAGS="%{rpmcxxflags} %{rpmcppflags}" \
	USRLDFLAGS="%{rpmldflags}" \
	VERBOSE=true

%if %{with apidocs}
%{__make} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

# make install just headers, libraries and binary manually
%{__make} installheader \
	INSTALLDIR=$RPM_BUILD_ROOT%{_prefix} \
	INCLUDEDIR=include/soplex

install -D bin/soplex $RPM_BUILD_ROOT%{_bindir}/soplex
install -D lib/libsoplex-%{version}.linux.*.so $RPM_BUILD_ROOT%{_libdir}/libsoplex.so.%{version}
ln -sf libsoplex.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libsoplex.so.1
ln -sf libsoplex.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libsoplex.so
%if %{with static_libs}
install -D lib/libsoplex-%{version}.linux.*.a $RPM_BUILD_ROOT%{_libdir}/libsoplex.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG COPYING
%attr(755,root,root) %{_bindir}/soplex
%attr(755,root,root) %{_libdir}/libsoplex.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsoplex.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsoplex.so
%{_includedir}/soplex

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsoplex.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
%endif
