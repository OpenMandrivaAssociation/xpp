%define name	xpp
%define version	1.5
%define release	%mkrel 4

Summary:	X Printing Panel
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Publishing

Source0:		http://cups.sourceforge.net/xpp/%{name}-%{version}cvs.tar.bz2
Patch0:		xpp-1.5-qualification.patch

Url:		http://cups.sourceforge.net/xpp/
BuildRoot:	%_tmppath/%name-%version-%release-root
BuildRequires:	libcups-devel libfltk-devel
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

%build

#export CXXFLAGS="${CXXFLAGS:-%optflags} -fno-exceptions -fno-rtti" ;
%configure

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=X Printing Panel
Comment=Frontend for easy printing with CUPS
Exec=%{_bindir}/%{name} 
Icon=printing_section.png
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
%update_menus
# Set up update-alternatives entry
%{_sbindir}/update-alternatives --install %{_bindir}/lpr lpr %{_bindir}/lpr-xpp 8

%preun

if [ "$1" = 0 ]; then
  # Remove update-alternatives entry
  %{_sbindir}/update-alternatives --remove lpr /usr/bin/lpr-xpp
fi

%postun
%clean_menus

%clean
rm -fr %buildroot

%files
%defattr(-,root,root)
%doc README LICENSE ChangeLog
%_bindir/*
%{_datadir}/applications/mandriva-%{name}.desktop
