Summary:	X Printing Panel
Name:		xpp
Version:	1.5
Release:	%mkrel 3
License:	GPL
Group:		Publishing

Source:		http://cups.sourceforge.net/xpp/%{name}-%{version}cvs.tar.bz2
Source1:	xpp.png.bz2

Url:		http://cups.sourceforge.net/xpp/
BuildRoot:	%_tmppath/%name-%version-%release-root
Requires:	libcups1 >= 1.1.9
BuildRequires:	libcups-devel >= 1.1.9, libfltk-devel
BuildRequires:	cups, Mesa-common-devel, libstdc++-devel
BuildRequires:	libpng-devel, libjpeg-devel

%description
The X Printing Panel (XPP) is a completely free tool for easy choosing of
the desired printer out of a list of all available printers and
for setting printer options by an easy-to-use graphical user interface.
One simply calls the program (xpp) instead of the usual utilities
(lpr or lp) at the command line or out of applications.

%prep

%setup -q
# Load menu icon
bzcat %SOURCE1 > $RPM_BUILD_DIR/%name-%version/xpp.png

%build

#export CXXFLAGS="${CXXFLAGS:-%optflags} -fno-exceptions -fno-rtti" ;
%configure

make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# install menu icon
install -d %buildroot/%_datadir/icons/locolor/16x16/apps
install -m 644 xpp.png %buildroot/%_iconsdir/locolor/16x16/apps

# install menu entry
install -d %buildroot/%_menudir
cat <<EOF > %buildroot/%_menudir/xpp
?package(xpp): needs=X11 \
section=Configuration/Printing \
title="XPP - X Printing Panel" \
longtitle="Frontend for easy printing with CUPS" \
command="xpp" \
icon="printing_section.png"
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
%_iconsdir/locolor/16x16/apps/*
%_menudir/xpp
