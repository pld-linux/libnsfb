#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	Framebuffer abstraction library
Summary(pl.UTF-8):	Biblioteka abstrakcji bufora ramki
Name:		libnsfb
Version:	0.2.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	598bf99aad38fd2083a9d668d1191238
Patch0:		%{name}-link.patch
URL:		http://www.netsurf-browser.org/projects/libnsfb/
BuildRequires:	SDL-devel
BuildRequires:	libvncserver-devel
BuildRequires:	libxcb-devel >= 1.3
BuildRequires:	netsurf-buildsystem >= 1.7
BuildRequires:	pkgconfig
BuildRequires:	wayland-devel
BuildRequires:	xcb-util-devel
BuildRequires:	xcb-util-image-devel
BuildRequires:	xcb-util-keysyms-devel
BuildRequires:	xcb-util-wm-devel >= 0.3.8
Requires:	libxcb-devel >= 1.3
Requires:	xcb-util-wm-devel >= 0.3.8
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

%description
LibNSFB to napisana w C biblioteka abstrakcji bufora ramki. Obecnie
jest rozwijana pod kątem użycia w przeglądarce NetSurf, ale może być
także używana w innych projektach.

Ogólną ideą biblioteki jest zapewnienie ogólnej abstrakcji liniowego
obszaru pamięci, który odpowiada widocznej tablicy pikseli na
urządzeniu wyświetlającym. Obsługiwane są różne głębie koloru, a
biblioteka udostępnia takie operacje, jak rysowanie w buforze ramki
czy kopiowanie prostokątów.

LibNSFB obecnie obsługuje następujące bufory ramki:
- linuksowy framebuffer
- X
- SDL
- VNC
- framebuffer ABLE

%package devel
Summary:	libnsfb library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libnsfb
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	SDL-devel
Requires:	libvncserver-devel
Requires:	libxcb-devel >= 1.3
Requires:	wayland-devel
Requires:	xcb-util-devel
Requires:	xcb-util-image-devel
Requires:	xcb-util-keysyms-devel
Requires:	xcb-util-wm-devel >= 0.3.8

%description devel
This package contains the include files and other resources you can
use to incorporate libnsfb into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libnsfb w swoich
programach.

%package static
Summary:	libnsfb static library
Summary(pl.UTF-8):	Statyczna biblioteka libnsfb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libnsfb library.

%description static -l pl.UTF-8
Statyczna biblioteka libnsfb.

%prep
%setup -q
%patch0 -p1

%build
export AR="%{__ar}"
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared
%if %{with static_libs}
%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static
%endif

%install
rm -rf $RPM_BUILD_ROOT

export AR="%{__ar}"
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnsfb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnsfb.so.0

%files devel
%defattr(644,root,root,755)
%doc usage
%attr(755,root,root) %{_libdir}/libnsfb.so
%{_includedir}/libnsfb*.h
%{_pkgconfigdir}/libnsfb.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnsfb.a
%endif
