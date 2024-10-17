%define name	xpp
%define version	1.5
%define release	%mkrel 11

Summary:	X Printing Panel
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Publishing

Source0:		http://cups.sourceforge.net/xpp/%{name}-%{version}cvs.tar.bz2
Patch0:		xpp-1.5-qualification.patch
Patch1:		xpp-bug27027.patch
Patch2:		xpp-new-fltk.patch
Patch3:		xpp_wformat.patch
Patch4:		xpp-1.5-constchar.patch
Url:		https://cups.sourceforge.net/xpp/
BuildRoot:	%_tmppath/%name-%version-%release-root
BuildRequires:	libcups-devel fltk-devel
BuildRequires:	cups libstdc++-devel
BuildRequires:	libpng-devel libjpeg-devel

%description
The X Printing Panel (XPP) is a completely free tool for easy choosing of
the desired printer out of a list of all available printers and
for setting printer options by an easy-to-use graphical user interface.
One simply calls the program (xpp) instead of the usual utilities
(lpr or lp) at the command line or out of applications.

%prep
%setup -q
%patch0 -p1 -b .qual
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1 -b .constchar

%build
%configure2_5x

make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=X Printing Panel
Comment=Frontend for easy printing with CUPS
Exec=%{_bindir}/%{name}
Icon=printing_section
Terminal=false
Type=Application
StartupNotify=true
Categories=Utility;Settings;Printing;X-MandrivaLinux-System-Configuration-Printing;
EOF

# Use update-alternatives to make printing with XPP also possible with
# the "lpr" command

( cd $RPM_BUILD_ROOT%{_bindir}
  ln -s xpp lpr-xpp
)

%post
%if %mdkversion < 200900
%update_menus
%endif
# Set up update-alternatives entry
%{_sbindir}/update-alternatives --install %{_bindir}/lpr lpr %{_bindir}/lpr-xpp 8

%preun

if [ "$1" = 0 ]; then
  # Remove update-alternatives entry
  %{_sbindir}/update-alternatives --remove lpr /usr/bin/lpr-xpp
fi

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -fr %buildroot

%files
%defattr(-,root,root)
%doc README LICENSE ChangeLog
%_bindir/*
%{_datadir}/applications/mandriva-%{name}.desktop
