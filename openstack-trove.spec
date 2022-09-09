%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global release_name mitaka
%global service trove
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc OpenStack DBaaS (codename %{service}) provisioning service.

%global with_doc 0

Name:             openstack-%{service}
Epoch:            1
Version:          XXX
Release:          XXX
Summary:          OpenStack DBaaS (%{service})

License:          ASL 2.0
URL:              https://wiki.openstack.org/wiki/Trove
Source0:          https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

Source1:          %{service}.logrotate
Source2:          guest_info

Source10:         %{name}-api.service
Source11:         %{name}-taskmanager.service
Source12:         %{name}-conductor.service
Source13:         %{name}-guestagent.service
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:        noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr >= 2.0.0
BuildRequires:    crudini
BuildRequires:    intltool
BuildRequires:    openstack-macros

# To build default config files
BuildRequires:    python3-keystoneauth1
BuildRequires:    python3-keystonemiddleware
BuildRequires:    python3-oslo-config
BuildRequires:    python3-oslo-log
BuildRequires:    python3-oslo-messaging
BuildRequires:    python3-oslo-middleware
BuildRequires:    python3-oslo-policy
BuildRequires:    python3-osprofiler

Requires:         %{name}-api = %{epoch}:%{version}-%{release}
Requires:         %{name}-taskmanager = %{epoch}:%{version}-%{release}
Requires:         %{name}-conductor = %{epoch}:%{version}-%{release}


%description
%{common_desc}

%package common
Summary:          Components common to all OpenStack %{service} services

Requires:         python3-%{service} = %{epoch}:%{version}-%{release}

%{?systemd_requires}
BuildRequires:    systemd

Requires(pre):    shadow-utils
Requires:         python3-pbr >= 2.0.0

%description common
%{common_desc}

This package contains scripts, config and dependencies shared
between all the OpenStack %{service} services.


%package api
Summary:          OpenStack %{service} API service
Requires:         %{name}-common = %{epoch}:%{version}-%{release}

%description api
%{common_desc}

This package contains the %{service} interface daemon.


%package taskmanager
Summary:          OpenStack %{service} taskmanager service
Requires:         %{name}-common = %{epoch}:%{version}-%{release}

%description taskmanager
%{common_desc}

This package contains the %{service} taskmanager service.


%package conductor
Summary:          OpenStack %{service} conductor service
Requires:         %{name}-common = %{epoch}:%{version}-%{release}

%description conductor
%{common_desc}

This package contains the %{service} conductor service.


%package guestagent
Summary:          OpenStack %{service} guest agent
Requires:         python3-pexpect

Requires:         %{name}-common = %{epoch}:%{version}-%{release}

%description guestagent
%{common_desc}

This package contains the %{service} guest agent service
that runs within the database VM instance.


%package -n       python3-%{service}
Summary:          Python libraries for %{service}
%{?python_provide:%python_provide python3-%{service}}

Requires:         python3-PyMySQL >= 0.7.6

Requires:         python3-kombu

Requires:         python3-cryptography >= 2.1.4
Requires:         python3-eventlet >= 0.18.2
Requires:         python3-iso8601 >= 0.1.11
Requires:         python3-netaddr >= 0.7.18
Requires:         python3-stevedore >= 1.20.0
Requires:         python3-xmltodict >= 0.10.1

Requires:         python3-webob >= 1.7.1

Requires:         python3-sqlalchemy >= 1.0.10
Requires:         python3-routes >= 2.3.1

Requires:         python3-troveclient >= 2.2.0
Requires:         python3-cinderclient >= 3.3.0
Requires:         python3-designateclient >= 2.7.0
Requires:         python3-glanceclient >= 1:2.8.0
Requires:         python3-heatclient >= 1.10.0
Requires:         python3-keystoneclient >= 1:3.8.0
Requires:         python3-keystonemiddleware >= 4.17.0
Requires:         python3-neutronclient >= 6.7.0
Requires:         python3-novaclient >= 1:9.1.0
Requires:         python3-swiftclient >= 3.2.0

Requires:         python3-oslo-concurrency >= 3.26.0
Requires:         python3-oslo-config >= 2:6.8.0
Requires:         python3-oslo-context >= 4.0.0
Requires:         python3-oslo-db >= 4.27.0
Requires:         python3-oslo-i18n >= 3.15.3
Requires:         python3-oslo-log >= 3.36.0
Requires:         python3-oslo-messaging >= 5.29.0
Requires:         python3-oslo-middleware >= 3.31.0
Requires:         python3-oslo-policy >= 3.6.0
Requires:         python3-oslo-serialization >= 2.18.0
Requires:         python3-oslo-service >= 1.24.0
Requires:         python3-oslo-upgradecheck >= 1.3.0
Requires:         python3-oslo-utils >= 3.40.0

Requires:         python3-osprofiler >= 1.4.0
Requires:         python3-jsonschema >= 3.2.0
Requires:         python3-jinja2 >= 2.10

Requires:         python3-passlib >= 1.7.0

Requires:         python3-pexpect >= 3.1
Requires:         python3-lxml >= 3.4.1
Requires:         python3-migrate >= 0.11.0
Requires:         python3-paste >= 2.0.2
Requires:         python3-paste-deploy >= 1.5.0
Requires:         python3-httplib2 >= 0.9.1
Requires:         python3-psycopg2 >= 2.6.2
Requires:         python3-docker >= 4.2.0
Requires:         python3-semantic_version >= 2.7.0
Requires:         python3-oslo-cache >= 1.26.0
Requires:         diskimage-builder >= 1.1.2

%description -n   python3-%{service}
%{common_desc}

This package contains the %{service} python library.

%package -n python3-%{service}-tests
Summary:        Trove tests
%{?python_provide:%python_provide python3-%{service}-tests}
Requires:       python3-%{service} = %{epoch}:%{version}-%{release}

%description -n python3-%{service}-tests
%{common_desc}

This package contains the Trove test files

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack %{service}

BuildRequires:    python3-sphinx

%description      doc
%{common_desc}

This package contains documentation files for %{service}.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{service}-%{upstream_version} -S git

# Avoid non-executable-script rpmlint while maintaining timestamps
find %{service} -name \*.py |
while read source; do
  if head -n1 "$source" | grep -F '/usr/bin/env'; then
    touch --ref="$source" "$source".ts
    sed -i '/\/usr\/bin\/env python/{d;q}' "$source"
    touch --ref="$source".ts "$source"
    rm "$source".ts
  fi
done

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{py3_build}

%install
%{py3_install}

# docs generation requires everything to be installed first

%if 0%{?with_doc}
pushd doc

SPHINX_DEBUG=1 sphinx-build -b html source build/html
# Fix hidden-file-or-dir warnings
rm -fr build/html/.doctrees build/html/.buildinfo

# Create dir link to avoid a sphinx-build exception
mkdir -p build/man/.doctrees/
ln -s .  build/man/.doctrees/man
SPHINX_DEBUG=1 sphinx-build -b man -c source source/man build/man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 build/man/*.1 %{buildroot}%{_mandir}/man1/

popd
%endif

# Create config file

export PYTHONPATH=$PYTHONPATH:.
oslo-config-generator --namespace trove.config --namespace oslo.messaging --namespace oslo.log --namespace oslo.log --namespace oslo.policy --output-file etc/%{service}/%{service}.conf.sample

# Setup directories
%if 0%{?rhel} != 6
install -d -m 755 %{buildroot}%{_unitdir}
%endif
install -d -m 755 %{buildroot}%{_datadir}/%{service}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}
install -d -m 750 %{buildroot}%{_localstatedir}/log/%{service}

# Install config files
install -p -D -m 640 etc/%{service}/%{service}.conf.sample %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf
# Use crudini to set some configuration keys
crudini --set %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf database connection mysql://trove:trove@localhost/trove
crudini --set %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf DEFAULT log_file %{_localstatedir}/log/%{service}/%{service}.log
mv %{buildroot}%{_prefix}/etc/%{service}/api-paste.ini %{buildroot}%{_sysconfdir}/%{service}/api-paste.ini
# Remove duplicate config files under /usr/etc/trove
rmdir %{buildroot}%{_prefix}/etc/%{service}
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
# FIXME(jpena): Trove has officially removed trove-conductor.conf
# and trove-taskmanager.conf. We should stop creating them once
# the deployment tools have been updated.
# Options for trove-guestagent.conf are the same as trove.conf
install -p -D -m 640 etc/%{service}/%{service}.conf.sample  %{buildroot}%{_sysconfdir}/%{service}/trove-taskmanager.conf
install -p -D -m 640 etc/%{service}/%{service}.conf.sample  %{buildroot}%{_sysconfdir}/%{service}/trove-conductor.conf
install -p -D -m 640 etc/%{service}/%{service}.conf.sample %{buildroot}%{_sysconfdir}/%{service}/trove-guestagent.conf
install -p -D -m 640 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{service}/guest_info

# Install initscripts
%if 0%{?rhel} == 6
install -p -D -m 755 %{SOURCE20} %{buildroot}%{_initrddir}/%{name}-api
install -p -D -m 755 %{SOURCE21} %{buildroot}%{_initrddir}/%{name}-taskmanager
install -p -D -m 755 %{SOURCE22} %{buildroot}%{_initrddir}/%{name}-conductor
install -p -D -m 755 %{SOURCE23} %{buildroot}%{_initrddir}/%{name}-guestagent
install -p -m 755 %{SOURCE30} %{SOURCE31} %{SOURCE32} %{SOURCE33} %{buildroot}%{_datadir}/%{service}
%else
install -p -m 644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{buildroot}%{_unitdir}
%endif

# Install logrotate
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{service}

# Remove unneeded in production stuff
rm -fr %{buildroot}%{_bindir}/trove-fake-mode
rm -fr %{buildroot}%{python3_sitelib}/run_tests.*
%pre common
# Origin: http://fedoraproject.org/wiki/Packaging:UsersAndGroups#Dynamic_allocation
USERNAME=%{service}
GROUPNAME=$USERNAME
HOMEDIR=%{_sharedstatedir}/$USERNAME
getent group $GROUPNAME >/dev/null || groupadd -r $GROUPNAME
getent passwd $USERNAME >/dev/null || \
  useradd -r -g $GROUPNAME -G $GROUPNAME -d $HOMEDIR -s /sbin/nologin \
    -c "$USERNAME Daemons" $USERNAME
exit 0

%post api
%systemd_post openstack-trove-api.service
%post taskmanager
%systemd_post openstack-trove-taskmanager.service
%post conductor
%systemd_post openstack-trove-conductor.service
%post guestagent
%systemd_post openstack-trove-guestagent.service

%preun api
%systemd_preun openstack-trove-api.service
%preun taskmanager
%systemd_preun openstack-trove-taskmanager.service
%preun conductor
%systemd_preun openstack-trove-conductor.service
%preun guestagent
%systemd_preun openstack-trove-guestagent.service

%postun api
%systemd_postun_with_restart openstack-trove-api.service
%postun taskmanager
%systemd_postun_with_restart openstack-trove-taskmanager.service
%postun conductor
%systemd_postun_with_restart openstack-trove-conductor.service
%postun guestagent
%systemd_postun_with_restart openstack-trove-guestagent.service


%files
%license LICENSE

%files common
%license LICENSE
%dir %{_sysconfdir}/%{service}
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}.conf
%attr(0640, root, %{service}) %{_sysconfdir}/%{service}/api-paste.ini
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%dir %attr(0750, %{service}, root) %{_localstatedir}/log/%{service}
%dir %attr(0755, %{service}, root) %{_localstatedir}/run/%{service}

%{_bindir}/%{service}-manage
%{_bindir}/%{service}-status
%{_bindir}/trove-mgmt-taskmanager

%{_datarootdir}/%{service}

%defattr(-, %{service}, %{service}, -)
%dir %{_sharedstatedir}/%{service}

%files api
%{_bindir}/%{service}-api
%{_unitdir}/%{name}-api.service

%files taskmanager
%{_bindir}/%{service}-taskmanager
%{_unitdir}/%{name}-taskmanager.service
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}-taskmanager.conf

%files conductor
%{_bindir}/%{service}-conductor
%{_unitdir}/%{name}-conductor.service
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}-conductor.conf

%files guestagent
%{_bindir}/%{service}-guestagent
%{_unitdir}/%{name}-guestagent.service
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}-guestagent.conf
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/guest_info

%files -n python3-%{service}
%license LICENSE
%{_bindir}/trove-wsgi
%{python3_sitelib}/%{service}
%{python3_sitelib}/%{service}-%{version}*.egg-info
%exclude %{python3_sitelib}/%{service}/tests

%files -n python3-%{service}-tests
%license LICENSE
%{python3_sitelib}/%{service}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
