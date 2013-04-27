#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Framebuffer abstraction library
Name:		libnsfb
Version:	0.1.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	686a4d2064edfed47d2653588c3b5512
Patch0:		%{name}-link.patch
URL:		http://www.netsurf-browser.org/projects/libnsfb/
BuildRequires:	SDL-devel
BuildRequires:	libvncserver-devel
BuildRequires:	libxcb-devel
BuildRequires:	netsurf-buildsystem
BuildRequires:	wayland-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibNSFB is a framebuffer abstraction library, written in C. It is
currently in development for use with NetSurf and is intended to be
suitable for use in other projects too.

The overall idea of the library is to provide a generic abstraction to
a linear section of memory which corresponds to a visible array of
pixel elements on a display device. Different colour depths are
supported and the library provides routines for tasks such as drawing
onto the framebuffer and rectangle copy operations.

LibNSFB currently supports the following as framebuffer providers:

- Linux framebuffer
- X
- SDL
- VNC
- ABLE framebuffer

%package devel
Summary:	libnsfb library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libnsfb
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the libraries, include files and other resources you can use
to incorporate libnsfb into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libnsfb w swoich
programach.

%package static
Summary:	libnsfb static libraries
Summary(pl.UTF-8):	Statyczne biblioteki libnsfb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libnsfb libraries.

%description static -l pl.UTF-8
Statyczna biblioteka libnsfb.

%prep
%setup -q
%patch0 -p1

%build
CFLAGS="%{rpmcflags}"
LDFLAGS="%{rpmldflags}"
export CFLAGS
export LDFLAGS

%{__make} PREFIX=%{_prefix} COMPONENT_TYPE=lib-shared Q='' \
	-Iinclude -Isrc"
%if %{with static_libs}
%{__make} PREFIX=%{_prefix} COMPONENT_TYPE=lib-static Q='' \
	-Iinclude -Isrc"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared \
	Q=''

%if %{with static_libs}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static \
	Q=''
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*.h
%{_pkgconfigdir}/*pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
