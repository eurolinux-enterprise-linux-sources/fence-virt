Name:		fence-virt
Version:	0.2.3
Release:	24%{?dist}
Summary:	A pluggable fencing framework for virtual machines
Group:		System Environment/Base
License:	GPLv2+
URL:		http://master.dl.sourceforge.net/project/fence-virt/fence-virt-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

ExclusiveArch:	i686 x86_64

BuildRequires:	corosynclib-devel clusterlib-devel libvirt-devel
BuildRequires:	openaislib-devel
BuildRequires:	automake autoconf libxml2-devel nss-devel nspr-devel
BuildRequires:	flex bison libuuid-devel
Conflicts:	fence-agents < 3.0.5-2

# Patches
Patch0: bz720767-fix_incorrect_return_value_on_hash_mismatch.patch
Patch1: bz691200-fix_error_getting_status_from_libvirt_qpid_plugin.patch
Patch2: bz691200-2-convert_libvirt_qpid_plugin_to_qmfv2.patch
Patch3: bz691200-3-add_libvirt_qmf_support_to_the_libvirt_qpid_plugin.patch
Patch4: bz734687-don_t_reference_out_of_scope_temporary.patch
Patch5: bz753974-catch_exceptions_for_libvirt_qmf_detection_failures.patch
Patch6: bz758392-fix_crash_when_we_fail_to_read_key_file.patch
Patch7: bz761215-fix_erroneous_man_page_xml.patch
Patch8: bz806949-stop_linking_against_unnecessary_qpid_libs.patch
Patch9: bz809101.patch
Patch10: bz853927.patch
Patch11: bz843104.patch
Patch12: bz823542.patch
Patch13: bz761228-fix_typo_in_fence_virt_8_man_page.patch
Patch14: bz823542-explicitly_set_delay_to_0.patch
Patch15: bz853927-return_success_if_a_domain_exists_but_is.patch
Patch16: bz883588.patch
Patch17: bz903172-fix_for_missed_libvirtd_events.patch
Patch18: bz1014238-clarify_the_path_option_in_serial_mode.patch
Patch19: bz1104740-send_complete_hostlist_info.patch
Patch20: bz914144-allow_multiple_hypervisors_for_the_libvirt.patch
Patch21: bz1020992-fence_xvm_print_status_when_invoked_with_o.patch
Patch22: bz1078197-fix_broken_restrictions_on_the_port_ranges.patch
Patch23: bz1125290-fix_static_analysis_errors.patch
Patch24: bz1204873-client_fix_delay_parameter_checking_copy_paste.patch
Patch25: bz908455-add_list_status_operation_for_compat_with_other.patch
Patch26: bz1010346-log_status_error_to_syslog_also.patch
Patch27: bz1204873-permit_explicitly_setting_delay_to_0.patch
Patch28: bz908455-add_list_status_command_to_man_page_and_metadata.patch
Patch29: bz1204873-remove_delay_from_the_status,_monitor_and_list.patch


%description
Fencing agent for virtual machines.


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


%package -n fence-virtd-libvirt
Summary:	Libvirt backend for fence-virtd
Group:		System Environment/Base
Requires:	libvirt > 0.6.0
Requires:	fence-virtd

%description -n fence-virtd-libvirt
Provides fence_virtd with a connection to libvirt to fence
virtual machines.  Useful for running a cluster of virtual
machines on a desktop.

%package -n fence-virtd-checkpoint
Summary:	Cluster+Libvirt backend for fence-virtd
Group:		System Environment/Base
Requires:	fence-virtd

%description -n fence-virtd-checkpoint
Provides fence_virtd with a connection to libvirt to fence
virtual machines.  Utilizes corosync's CPG framework to route
requests as well as the AIS Checkpoint API to store virtual
machine states across a cluster and make intelligent decisions
about whether a virtual machine is running.


%prep
%setup -q

%patch0 -p1 -b .bz720767.1
%patch1 -p1 -b .bz691200.1
%patch2 -p1 -b .bz691200.2
%patch3 -p1 -b .bz691200.3
%patch4 -p1 -b .bz734687.1
%patch5 -p1 -b .bz753974.1
%patch6 -p1 -b .bz758392.1
%patch7 -p1 -b .bz761215.1
%patch8 -p1 -b .bz806949.1
%patch9 -p1 -b .bz809101.1
%patch10 -p1 -b .bz853927.1
%patch11 -p1 -b .bz843104.1
%patch12 -p1 -b .bz823542.1
%patch13 -p1 -b .bz761228.1
%patch14 -p1 -b .bz823542.1
%patch15 -p1 -b .bz853927.1
%patch16 -p1 -b .bz883588.1
%patch17 -p1 -b .bz903172.1
%patch18 -p1 -b .bz1014238.1
%patch19 -p1 -b .bz1104740.1
%patch20 -p1 -b .bz914144.1
%patch21 -p1 -b .bz1020992.1
%patch22 -p1 -b .bz1078197.1
%patch23 -p1 -b .bz1125290.1
%patch24 -p1 -b .bz1204873.1
%patch25 -p1 -b .bz908455.1
%patch26 -p1 -b .bz1010346.1
%patch27 -p1 -b .bz1204873.1
%patch28 -p1 -b .bz908455.1
%patch29 -p1 -b .bz1204873.1

%build
./autogen.sh
%{configure} --disable-libvirt-qpid-plugin
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}/rc.d/init.d
install -m 0755 fence_virtd.init %{buildroot}/%{_sysconfdir}/rc.d/init.d/fence_virtd

%post
# Update cluster schema (ignore return code)
ccs_update_schema > /dev/null 2>&1 ||:

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING TODO README
%{_sbindir}/fence_virt
%{_sbindir}/fence_xvm
%{_mandir}/man8/fence_virt.*
%{_mandir}/man8/fence_xvm.*

%files -n fence-virtd
%defattr(-,root,root,-)
%{_sbindir}/fence_virtd
%{_sysconfdir}/rc.d/init.d/fence_virtd
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

%files -n fence-virtd-libvirt
%defattr(-,root,root,-)
%{_libdir}/%{name}/libvirt.so

%files -n fence-virtd-checkpoint
%defattr(-,root,root,-)
%{_libdir}/%{name}/checkpoint.so

%changelog
* Wed Jan 04 2017 Ryan McCabe <rmccabe@redhat.com> - 0.2.3-24
- fence-virt: Add list-status command to man page and metadata
  Resolves: rhbz#908455
- Remove delay from the status, monitor and list
  Resolves: rhbz#1204873

* Fri Nov 11 2016 Ryan McCabe <rmccabe@redhat.com> - 0.2.3-23
- fence-virt: Permit explicitly setting delay to 0
  Resolves: rhbz#1204873

* Tue Nov 08 2016 Ryan McCabe <rmccabe@redhat.com> - 0.2.3-22
- fence-virt: Log client status and errors to syslog
  Resolves: rhbz#1010346

* Tue Nov 01 2016 Ryan McCabe <rmccabe@redhat.com> - 0.2.3-21
- fence-virt: Add 'list-status' operation for compat with other
  Resolves: rhbz#908455

* Tue Nov 01 2016 Ryan McCabe <rmccabe@redhat.com> - 0.2.3-20
- client: fix "delay" parameter checking (copy-paste)
  Resolves: rhbz#1204873

* Tue Mar 03 2015 Ryan McCabe <rmccabe@redhat.com> - 0.2.3-19
- fence_virt/fence_xvm: Print status when invoked with -o
  Resolves: rhbz#1020992
- fence-virt: Fix broken restrictions on the port ranges
  Resolves: rhbz#1078197
- Fix static analysis errors
  Resolves: rhbz#1125290

* Mon Jun 30 2014 Ryan McCabe <rmccabe@redhat.com> - 0.2.3-18
- fence-virtd: Allow multiple hypervisors for the libvirt
  Resolves: rhbz#914144

* Sun Jun 22 2014 Ryan McCabe <rmccabe@redhat.com> - 0.2.3-17
- fence-virt: Send complete hostlist info
  Resolves: rhbz#1104740

* Sun Jun 22 2014 Ryan McCabe <rmccabe@redhat.com> - 0.2.3-16
- fence-virt: Clarify the path option in serial mode
  Resolves: rhbz#1014238

* Fri Sep 13 2013 Ryan McCabe <rmccabe@redhat.com> - 0.2.3-15
- fence-virt: Fix for missed libvirtd events
  Resolves: rhbz#903172

* Tue Jul 16 2013 Ryan McCabe <rmccabe@redhat.com> - 0.2.3-14
- Install manual pages with file permission mode 644 instead of 755
  Resolves rhbz#883588
 
* Fri Oct 26 2012 Ryan McCabe <rmccabe@redhat.com> - 0.2.3-13
- Return success if a domain exists but is off
  Resolves: rhbz#853927

* Wed Oct 17 2012 Ryan McCabe <rmccabe@redhat.com> - 0.2.3-12
- fence-virt: Explicitly set delay to 0
  Resolves: rhbz#823542

* Mon Oct 08 2012 Ryan McCabe <rmccabe@redhat.com> - 0.2.3-11
- fence_virt: Fix typo in fence_virt(8) man page
  Resolves: rhbz#761228

* Wed Sep 26 2012 Ryan McCabe <rmccabe@redhat.com> - 0.2.3-10
- Drop the fence-virtd-libvirt-qpid subpackage.
  Resolves: rhbz#859235
- Add a delay option to fence_virt/fence_xvm
  Resolves: rhbz#823542
- Return failure from fence_virtd when attempting to fence a nonexistent VM
  Resolves: rhbz#853927
- Improve the documentation of the 'hash' parameter in fence_virt.conf
  Resolves: rhbz#843104

* Wed Apr 11 2012 Ryan McCabe <rmccabe@redhat.com> - 0.2.3-9
- Update the man page and configuration generator to reflect the actual
  behavior of the default value for the "interface" option.
  Resolves: rhbz#809101

* Tue Mar 27 2012 Lon Hohberger <lon@users.sourceforge.net> - 0.2.3-8
- Respin for newer version of QMF
  Resolves: rhbz#806949

* Mon Mar 26 2012 Lon Hohberger <lon@users.sourceforge.net> - 0.2.3-7
- Stop linking against unnecessary QPid libs.
  Resolves: rhbz#806949

* Wed Feb 08 2012 Lon Hohberger <lon@users.sourceforge.net> - 0.2.3-6
- Catch exceptions for libvirt-qmf detection failures
  Resolves: rhbz#753974
- Fix crash when we fail to read key file.
  Resolves: rhbz#758392
- Fix erroneous man page XML
  Resolves: rhbz#761215

* Mon Sep 19 2011 Lon Hohberger <lon@users.sourceforge.net> - 0.2.3-5
- Don't reference out-of-scope temporary
  Resolves: rhbz#734687

* Tue Aug 16 2011 Lon Hohberger <lon@users.sourceforge.net> - 0.2.3-4
- Correct spec file and requirements.
  Related: rhbz#691200

* Thu Aug 11 2011 Lon Hohberger <lon@users.sourceforge.net> - 0.2.3-3
- Fix error getting status from libvirt-qpid plugin
  Convert libvirt-qpid plugin to QMFv2
  Add libvirt-qmf support to the libvirt-qpid plugin
  Resolves: rhbz#691200

* Mon Aug 08 2011 Lon Hohberger <lhh@redhat.com> - 0.2.3-2
- Fix incorrect return value on hash mismatch
  Resolves: rhbz#720767

* Fri Jul 08 2011 Lon Hohberger <lon@users.sourceforge.net> - 0.2.3-1
- Zap patch queue
- Add post call to fence-virt to integrate with cluster 3.1.4
- Rebase to latest upstream
- Provide 'domain' in metadata output for compatibility
- Fix input parsing to allow domain again
  Resolves: rhbz#719645

* Mon Mar 28 2011 Lon Hohberger <lon@users.sourceforge.net> - 0.2.1-8
- Rebuild against newer QMF libraries
  Related: rhbz#690582

* Wed Feb 02 2011 Lon Hohberger <lon@users.sourceforge.net> - 0.2.1-7
- Rebuild against newer QMF libraries
  Related: rhbz#631002

* Wed Feb 02 2011 Lon Hohberger <lon@users.sourceforge.net> - 0.2.1-6
- Fix man page references: fence_virtd.conf -> fence_virt.conf
  (fix_man_page_references_fence_virtd_conf_fence_virt_conf.patch)
  Resolves: rhbz#667170

* Fri Aug 6 2010 Lon Hohberger <lhh@redhat.com> - 0.2.1-5
- Rebuild against current qmf-client-cpp
  Resolves: rhbz#621889

* Wed May 12 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.2.1-4
- Do not build on ppc and ppc64.
  Resolves: rhbz#590986

* Wed Feb 24 2010 Lon Hohberger <lhh@redhat.com> 0.2.1-3
- Fix spec file due to qpid package renaming and architecture changes
- Don't build on s390 and s390x
- Resolves: rhbz#568003 rhbz#567744

* Wed Feb 10 2010 Lon Hohberger <lhh@redhat.com> 0.2.1-2
- Fix man page location
- Fix metadata output
- Fix arguments to be more consistent with other fencing
  agents
- Resolves: rhbz#561418 rhbz#563624 rhbz#563626

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

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.1.2-1.1
- Rebuilt for RHEL 6

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
