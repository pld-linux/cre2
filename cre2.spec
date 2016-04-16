#
# Conditional build:
%bcond_without	tests		# build without tests
%bcond_with	doc		# build doc

Summary:	C language wrapper for RE2 the regular expressions library from Google
Name:		cre2
Version:	0.3.1
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/marcomaggi/cre2/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3aad10c2ea311e5d517b20edd3abf823
URL:		https://github.com/marcomaggi/cre2/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# common make args
%define		_make_opts %{!?with_doc:INFO_DEPS=}

%description
The CRE2 distribution is a C language wrapper for the RE2 library,
which is implemented in C++. RE2 is a fast, safe, thread-friendly
alternative to backtracking regular expression engines like those used
in PCRE, Perl, and Python.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q

%build
install -d meta/autotools
%{__aclocal} -I meta/autotools
%{__libtoolize}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}
%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
    DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README COPYING
%attr(755,root,root) %{_libdir}/libcre2.so.*.*.*
%ghost %{_libdir}/libcre2.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/cre2.h
%{_libdir}/libcre2.la
%{_libdir}/libcre2.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libcre2.a
