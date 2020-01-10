Name:		fence-virt
Version:	0.3.2
Release:	13%{?dist}
Summary:	A pluggable fencing framework for virtual machines
Group:		System Environment/Base
License:	GPLv2+

%if 0%{?rhel}
ExclusiveArch: i686 x86_64 ppc64le
%endif

URL:		http://fence-virt.sourceforge.net
Source0:	http://people.redhat.com/rmccabe/fence-virt/%{name}-%{version}.tar.bz2

Patch0: bz1207422-client_do_not_truncate_vm_domains_in_list_output.patch
Patch1: bz1078197-fix_broken_restrictions_on_the_port_ranges.patch
Patch2: bz1204873-fix_delay_parameter_checking_copy_paste.patch
Patch3: bz1204877-remove_delay_from_the_status,_monitor_and_list.patch
Patch4: bz1334170-allow_fence_virtd_to_run_as_non_root.patch
Patch5: bz1334170-2-fix_use_of_undefined_#define.patch
Patch6: bz1291522-Install_firewalld_unit_file.patch
Patch7: bz1393958-cleanup_numeric_argument_parsing.patch
Patch8: bz1411910-fence_virtd_drop_legacy_sysvstartpriority_from_service.patch
Patch9: bz1334170-cleanup_documentation_of_the_tcp_listener.patch
Patch10: bz1092531-enable_hardening.patch
Patch11: bz1447700-virt_add_support_for_the_validate_all_status.patch
Patch12: bz1384181-make_the_libvirt_backend_survive_libvirtd.patch

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	corosynclib-devel libvirt-devel
BuildRequires:	automake autoconf libxml2-devel nss-devel nspr-devel
BuildRequires:	flex bison libuuid-devel

BuildRequires: systemd-units
Requires(post):	systemd-sysv systemd-units firewalld-filesystem
Requires(preun):	systemd-units
Requires(postun):	systemd-units

Conflicts:	fence-agents < 3.0.5-2


%description
Fencing agent for virtual machines.

%global _hardened_build 1

%package -n fence-virtd
Summary:	Daemon which handles requests from fence-virt
Group:		System Environment/Base

%description -n fence-virtd
This package provides the host server framework, fence_virtd,
for fence_virt.  The fence_virtd host daemon is resposible for
processing fencing requests from virtual machines and routing
the requests to the appropriate physical machine for action.


%package -n fence-virtd-multicast
Summary:	Multicast listener for fence-virtd
Group:		System Environment/Base
Requires:	fence-virtd

%description -n fence-virtd-multicast
Provides multicast listener capability for fence-virtd.


%package -n fence-virtd-serial
Summary:	Serial VMChannel listener for fence-virtd
Group:		System Environment/Base
Requires:	libvirt >= 0.6.2
Requires:	fence-virtd

%description -n fence-virtd-serial
Provides serial VMChannel listener capability for fence-virtd.

%package -n fence-virtd-tcp
Summary:	Tcp listener for fence-virtd
Group:	System Environment/Base
Requires:	fence-virtd

%description -n fence-virtd-tcp
Provides TCP listener capability for fence-virtd.

%package -n fence-virtd-libvirt
Summary:	Libvirt backend for fence-virtd
Group:		System Environment/Base
Requires:	libvirt >= 0.6.0
Requires:	fence-virtd

%description -n fence-virtd-libvirt
Provides fence_virtd with a connection to libvirt to fence
virtual machines.  Useful for running a cluster of virtual
machines on a desktop.


%prep
%setup -q

%patch0 -p1 -b .bz1207422
%patch1 -p1 -b .bz1078197.1
%patch2 -p1 -b .bz1204873.1
%patch3 -p1 -b .bz1204877.1
%patch4 -p1 -b .bz1334170.1
%patch5 -p1 -b .bz1334170.2
%patch6 -p1 -b .bz1291522.1
%patch7 -p1 -b .bz1393958.1
%patch8 -p1 -b .bz1411910.1
%patch9 -p1 -b .bz1334170.1
%patch10 -p1 -b .bz1092531.1
%patch11 -p1 -b .bz1447700.1
%patch12 -p1 -b .bz1384181.1

%build
%ifarch s390 s390x sparcv9 sparc64
export PIECFLAGS="-fPIE"
%else
export PIECFLAGS="-fpie"
%endif

export RELRO="-Wl,-z,relro,-z,now"
export CFLAGS="$RPM_OPT_FLAGS $CPPFLAGS $PIECFLAGS $RELRO"
export CXXFLAGS="$RPM_OPT_FLAGS $CPPFLAGS $PIECFLAGS $RELRO"
export LDFLAGS="$LDFLAGS -pie"

./autogen.sh
%{configure} --disable-libvirt-qmf-plugin --enable-tcp-plugin
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Systemd unit file
mkdir -p %{buildroot}/%{_unitdir}/
install -m 0644 fence_virtd.service %{buildroot}/%{_unitdir}/

# firewalld service file
mkdir -p %{buildroot}/%{_prefix}/lib/firewalld/services/
install -m 0644 fence_virt.xml %{buildroot}/%{_prefix}/lib/firewalld/services/

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING TODO README
%{_sbindir}/fence_virt
%{_sbindir}/fence_xvm
%{_mandir}/man8/fence_virt.*
%{_mandir}/man8/fence_xvm.*


%post
ccs_update_schema > /dev/null 2>&1 ||:
# https://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Systemd
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
# https://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Systemd
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable fence_virtd.service &> /dev/null || :
    /bin/systemctl stop fence_virtd.service &> /dev/null || :
fi

%postun
# https://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Systemd
/bin/systemctl daemon-reload &> /dev/null || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart fence_virtd.service &> /dev/null || :
fi


%triggerun -- fence_virtd < 0.3.0-1
# https://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Packages_migrating_to_a_systemd_unit_file_from_a_SysV_initscript
/usr/bin/systemd-sysv-convert --save fence_virtd &> /dev/null || :
/sbin/chkconfig --del fence_virtd &> /dev/null || :
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
/bin/systemctl try-restart fence_virtd.service &> /dev/null || :


%files -n fence-virtd
%defattr(-,root,root,-)
%{_sbindir}/fence_virtd
%{_unitdir}/fence_virtd.service
%{_prefix}/lib/firewalld/services/fence_virt.xml
%config(noreplace) %{_sysconfdir}/fence_virt.conf
%dir %{_libdir}/%{name}
%{_mandir}/man5/fence_virt.conf.*
%{_mandir}/man8/fence_virtd.*

%files -n fence-virtd-multicast
%defattr(-,root,root,-)
%{_libdir}/%{name}/multicast.so

%files -n fence-virtd-serial
%defattr(-,root,root,-)
%{_libdir}/%{name}/serial.so

%files -n fence-virtd-tcp
%defattr(-,root,root,-)
%{_libdir}/%{name}/tcp.so

%files -n fence-virtd-libvirt
%defattr(-,root,root,-)
%{_libdir}/%{name}/libvirt.so

%changelog
* Wed Aug 09 2017 Ryan McCabe <rmccabe@redhat.com> - 0.3.2-13
- fence_virtd: Make the libvirt backend survive libvirtd restarts
  Resolves: rhbz#1384181
- fence_xvm/fence_virt: Add support for the validate-all status
  Resolves: rhbz#1447700

* Wed Jun 14 2017 Ryan McCabe <rmccabe@redhat.com> - 0.3.2-12
- fence-virt: Rebuild to restore debuginfo
  Resolves: rhbz#1092531

* Mon May 22 2017 Ryan McCabe <rmccabe@redhat.com> - 0.3.2-11
- fence-virt: Enable PIE and full RELRO
  Resolves: rhbz#1092531

* Mon May 22 2017 Ryan McCabe <rmccabe@redhat.com> - 0.3.2-10
- fence-virt: Enable PIE and RELRO
  Resolves: rhbz#1092531

* Wed May 17 2017 Ryan McCabe <rmccabe@redhat.com> - 0.3.2-9
- fence-virtd: Cleanup documentation of the TCP listener
  Resolves: rhbz#1334170

* Wed Mar 15 2017 Ryan McCabe <rmccabe@redhat.com> - 0.3.2-8
- fence-virt: Build for ppc64le
  Resolves: rhbz#1402572

* Mon Mar 13 2017 Ryan McCabe <rmccabe@redhat.com> - 0.3.2-7
- fence_virtd: drop legacy SysVStartPriority from service
  Resolves: rhbz#1411910

* Mon Mar 13 2017 Ryan McCabe <rmccabe@redhat.com> - 0.3.2-6
- fence-virt: Cleanup numeric argument parsing
  Resolves: rhbz#1393958

* Tue Jun 28 2016 Ryan McCabe <rmccabe@redhat.com> - 0.3.2-5
- fence-virt: Add firewalld service file.
  Resolves: rhbz#1291522

* Mon Jun 27 2016 Ryan McCabe <rmccabe@redhat.com> - 0.3.2-4
- fence-virt: Enable the TCP listener plugin
  Resolves: rhbz#1334170
- Allow fence_virtd to run as non-root
  Fix use of undefined define
  Resolves: rhbz#1334170

* Mon Jun 27 2016 Ryan McCabe <rmccabe@redhat.com> - 0.3.2-3
- fence-virt: Fix broken restrictions on the port ranges
  Resolves: rhbz#1214301
- client: Fix "delay" parameter checking
  Resolves: rhbz#1204877
- Remove delay from the status, monitor and list
  Resolves: rhbz#1204877

* Fri Jul 17 2015 Ryan McCabe <rmccabe@redhat.com> - 0.3.2-2
- Do not truncate VM domains in the output of the list command.
  Resolves: rhbz#1207422

* Mon Sep 08 2014 Ryan McCabe <rmccabe@redhat.com> - 0.3.2-1
- Rebase to the 0.3.2 release.
  Resolves: rhbz#1111384

* Wed Feb 19 2014 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-16
- Fail cleanly when unable to bind the TCP listener socket

* Tue Feb 18 2014 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-15
- Remove references to syslog.target from the fence_virtd systemd unit file

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.3.0-14
- Mass rebuild 2013-12-27

* Tue May 07 2013 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-13
- Rebuild

* Tue May 07 2013 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-12
- Drop libvirt-qmf-plugin

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 02 2012 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-10
- bswap fix for big endian

* Fri Nov 02 2012 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-9
- Return success if a domain exists but is already off.

* Thu Oct 25 2012 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-8
- Version bump

* Thu Oct 25 2012 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-7
- Fix uninitialized variable for the -w option.

* Mon Oct 15 2012 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-6
- Add a -w (delay) option.
- Return failure when attempting to fence a nonexistent domain
- Improve man pages

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 27 2012 Ryan McCabe <rmccabe@fedoraproject.org> 0.3.0-4
- Add QPid build fix patch from upstream.

* Fri Feb 10 2012 Lon Hohberger <lon@fedoraproject.org> 0.3.0-2
- Fix URL / Source0 lines
  Resolves: Fedora#706560

* Tue Feb 07 2012 Lon Hohberger <lhh@redhat.com> 0.3.0-1
- Rebase from upstream to 0.3.0
- Systemd unit file integration
- Pacemaker backend
- Various fixes for startup
- Rename libvirt-qpid to libvirt-qmf backend
- Updated default configuration for easier deployment on
  Fedora systems

* Tue Feb 07 2012 Lon Hohberger <lhh@redhat.com> - 0.2.3-6
- Bump and rebuild

* Tue Feb 07 2012 Lon Hohberger <lhh@redhat.com> - 0.2.3-5
- Fixup changelog

* Mon Feb 06 2012 Lon Hohberger <lhh@redhat.com> - 0.2.3-4
- Drop checkpoint backend since cman and openais are gone

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul  8 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.2.3-2
- add post call to fence-virt to integrate with cluster 3.1.4

* Wed Jun 29 2011 Fabio M. Di Nitto <fdinitto@redhat.com> 0.2.3-1
- new upstream release fix compat regression

* Mon Jun 27 2011 Fabio M. Di Nitto <fdinitto@redhat.com> 0.2.2-1
- new upstream release

* Mon May 09 2011 Fabio M. Di Nitto <fdinitto@redhat.com> 0.2.1-5
- Rebuilt for libqmfconsole soname change

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Apr 01 2010 Lon Hohberger <lhh@redhat.com> 0.2.1-3
- Update specfile to require correct qpid/qmf libraries
- Resolves: bz#565111

* Tue Feb 23 2010 Fabio M. Di Nitto <fdinitto@redhat.com> 0.2.1-2
- Update spec file to handle correctly versioned Requires

* Fri Jan 15 2010 Lon Hohberger <lhh@redhat.com> 0.2.1-1
- Update to latest upstream version
- Fix bug around status return codes for VMs which are 'off'

* Thu Jan 14 2010 Lon Hohberger <lhh@redhat.com> 0.2-1
- Update to latest upstream version
- Serial & VMChannel listener support
- Static permission map support
- Man pages
- Init script
- Various bugfixes

* Mon Sep 21 2009 Lon Hohberger <lhh@redhat.com> 0.1.3-1
- Update to latest upstream version
- Adds libvirt-qpid backend support
- Fixes UUID operation with libvirt backend
- Adds man page for fence_xvm and fence_virt
- Provides fence_xvm compatibility for cluster 3.0.6

* Mon Sep 21 2009 Lon Hohberger <lhh@redhat.com> 0.1.2-1
- Update to latest upstream version
- Fix build issue on i686

* Mon Sep 21 2009 Lon Hohberger <lhh@redhat.com> 0.1.1-1
- Update to latest upstream version
- Clean up spec file

* Mon Sep 21 2009 Lon Hohberger <lhh@redhat.com> 0.1-2
- Spec file cleanup

* Thu Sep 17 2009 Lon Hohberger <lhh@redhat.com> 0.1-1
- Initial build for rawhide
