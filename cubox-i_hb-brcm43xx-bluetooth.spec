%define debug_package %{nil}

Name:           cubox-i_hb-brcm43xx-bluetooth
Version:        1.1
Release:        3%{?dist}
Summary:        Cubox-i brcm43xx Bluetooth firmware loader
Group:          Applications/System
License:        ASL 2.0
ExclusiveArch:  %{arm}
Source1:        brcm_patchram_plus
Source2:        brcm43xx-firmware-update
Source3:        bcm4329.hcd
Source4:        bcm4330.hcd
Source5:        brcm43xx.service
Source6:        brcm43xx-firmware.service
Source7:        bcm43xx


Obsoletes:      brcm_patchram_plus
Obsoletes:      cubox-i-brcm4329-bluetooth
Obsoletes:      cubox-i_hb-brcm4329-bluetooth
Requires:       linux-firmware
Requires:       bluez
Requires(post):         systemd
Requires(preun):        systemd
Requires(postun):       systemd

%description
brcm43xx Bluetooth firmware loader

%prep

%build
CFLAGS="$RPM_OPT_FLAGS"
%{?__global_ldflags:LDFLAGS="%__global_ldflags"}
gcc $CFLAGS $LDFLAGS -o brcm_patchram_plus brcm_patchram_plus.c

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -m0755 %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}
install -m0755 %{SOURCE2} $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT/lib/firmware/brcm
install -m0644 %{SOURCE3} $RPM_BUILD_ROOT/lib/firmware/brcm
install -m0644 %{SOURCE4} $RPM_BUILD_ROOT/lib/firmware/brcm
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -m0644 %{SOURCE5} $RPM_BUILD_ROOT%{_unitdir}
install -m0644 %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m0644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%clean
rm -rf $RPM_BUILD_ROOT

%post
# Install/enable the new services but do not start them
/bin/systemctl enable brcm43xx-firmware.service >/dev/null 2>&1 || :
/bin/systemctl enable brcm43xx.service >/dev/null 2>&1 || :

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable --now brcm43xx-firmware.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable --now brcm43xx.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
# XXX - These shouldn't be wildcards, use specific files instead
%attr(0755,root,root) %{_sbindir}/*
%attr(0644,root,root) /lib/firmware/brcm/*
%attr(0644,root,root) %{_unitdir}/*.service
%attr(0644,root,root) %{_sysconfdir}/sysconfig/bcm43xx
%changelog
* Tue Feb 25 2014 Jason Montleon <jason@montleon.com> 1.0-1
- new version of the package for cubox-i which uses ttymx3 instead of ttymx2
- renamed package to prevent confusion as they are not quite the same
* Wed Jan 15 2014 Clive Messer <clive.messer@communitysqueeze.org> - 1.0-3
- Fix path to hciattach, /sbin on F19, /bin on F20.
- Build brcm_patchram_plus with system LDFLAGS.

* Fri Jul 26 2013 Clive Messer <clive.messer@communitysqueeze.org> - 1.0-2
- Add 'Requires: bluez' for hciattach dependency.

* Fri Jul 26 2013 Clive Messer <clive.messer@communitysqueeze.org> - 1.0-1
- Initial release.
