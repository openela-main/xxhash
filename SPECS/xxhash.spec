Name:		xxhash
Version:	0.8.1
Release:	3%{?dist}
Summary:	Extremely fast hash algorithm

#		The source for the library (xxhash.c and xxhash.h) is BSD
#		The source for the command line tool (xxhsum.c) is GPLv2+
License:	BSD and GPLv2+
URL:		http://www.xxhash.com/
Source0:	https://github.com/Cyan4973/xxHash/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	make
BuildRequires:	gcc
BuildRequires:	doxygen

Patch0:		1-fix-man-page-installation.patch

%description
xxHash is an Extremely fast Hash algorithm, running at RAM speed
limits. It successfully completes the SMHasher test suite which
evaluates collision, dispersion and randomness qualities of hash
functions. Code is highly portable, and hashes are identical on all
platforms (little / big endian).

%package libs
Summary:	Extremely fast hash algorithm - library
License:	BSD

%description libs
xxHash is an Extremely fast Hash algorithm, running at RAM speed
limits. It successfully completes the SMHasher test suite which
evaluates collision, dispersion and randomness qualities of hash
functions. Code is highly portable, and hashes are identical on all
platforms (little / big endian).

%package devel
Summary:	Extremely fast hash algorithm - development files
License:	BSD
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
# By setting XXH_INLINE_ALL, xxhash may be used as a header-only library.
# Dependent packages that use xxhash this way must BR this virtual Provide:
Provides:	%{name}-static = %{version}-%{release}

%description devel
Development files for the xxhash library

%package doc
Summary:	Extremely fast hash algorithm - documentation files
License:	BSD
BuildArch:	noarch

%description doc
Documentation files for the xxhash library

%prep
%setup -q -n xxHash-%{version}
%patch0 -p1

%build
# Enable runtime detection of sse2/avx2/avx512 on intel architectures
%ifarch %{ix86} x86_64
%global dispatch 1
%else
%global dispatch 0
%endif

%make_build MOREFLAGS="%{__global_cflags} %{?__global_ldflags}" \
	    DISPATCH=%{dispatch}
doxygen

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}
rm %{buildroot}/%{_libdir}/libxxhash.a

%check
make check
make test-xxhsum-c

%ldconfig_scriptlets libs

%files
%{_bindir}/xxh*sum
%{_mandir}/man1/xxh*sum.1*
%license cli/COPYING
%doc cli/README.md

%files libs
%{_libdir}/libxxhash.so.*
%license LICENSE
%doc README.md

%files devel
%{_includedir}/xxhash.h
%{_includedir}/xxh3.h
%{_libdir}/libxxhash.so
%{_libdir}/pkgconfig/libxxhash.pc

%files doc
%doc doxygen/html

%changelog
* Mon Jul 18 2022 Vladis Dronov <vdronov@redhat.com> - 0.8.1-3
- Fix broken manpages (upstream commit 836f4e735cf3)
- Add OSCI testing harness

* Fri Jun 17 2022 Vladis Dronov <vdronov@redhat.com> - 0.8.1-1
- Packaging of xxhash v0.8.1 for CS and RHEL copied from Fedora 36
