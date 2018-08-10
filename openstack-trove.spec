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

BuildArch:        noarch
BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr >= 2.0.0
BuildRequires:    python-d2to1
BuildRequires:    python-sphinx
BuildRequires:    crudini
BuildRequires:    intltool
BuildRequires:    openstack-macros

Requires:         %{name}-api = %{epoch}:%{version}-%{release}
Requires:         %{name}-taskmanager = %{epoch}:%{version}-%{release}
Requires:         %{name}-conductor = %{epoch}:%{version}-%{release}


%description
%{common_desc}

%package common
Summary:          Components common to all OpenStack %{service} services

Requires:         python-%{service} = %{epoch}:%{version}-%{release}

%{?systemd_requires}
BuildRequires:    systemd

Requires(pre):    shadow-utils
Requires:         python-pbr >= 2.0.0

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
%if 0%{?rhel}
Requires:         pexpect
%else
Requires:         python-pexpect
%endif

Requires:         %{name}-common = %{epoch}:%{version}-%{release}

%description guestagent
%{common_desc}

This package contains the %{service} guest agent service
that runs within the database VM instance.


%package -n       python-%{service}
Summary:          Python libraries for %{service}

Requires:         MySQL-python

Requires:         python2-kombu

Requires:         diskimage-builder >= 1.1.2
Requires:         python2-cryptography >= 2.1.4
Requires:         python-enum34
Requires:         python2-eventlet
Requires:         python2-iso8601
Requires:         python2-netaddr
Requires:         python-lxml
Requires:         python2-six >= 1.10.0
Requires:         python2-stevedore >= 1.20.0
Requires:         python2-xmltodict >= 0.10.1

Requires:         python-webob >= 1.7.1
Requires:         python-migrate >= 0.11.0

Requires:         python2-sqlalchemy >= 1.2.0
Requires:         python-paste
Requires:         python-paste-deploy
Requires:         python2-routes

Requires:         python2-troveclient
Requires:         python2-cinderclient >= 3.3.0
Requires:         python2-designateclient >= 2.7.0
Requires:         python2-glanceclient >= 1:2.8.0
Requires:         python2-heatclient >= 1.10.0
Requires:         python2-keystoneclient >= 1:3.8.0
Requires:         python2-keystonemiddleware >= 4.17.0
Requires:         python2-neutronclient >= 6.7.0
Requires:         python2-novaclient >= 1:9.1.0
Requires:         python2-swiftclient >= 3.2.0

Requires:         python2-oslo-concurrency >= 3.26.0
Requires:         python2-oslo-config >= 2:5.2.0
Requires:         python2-oslo-context >= 2.19.2
Requires:         python2-oslo-db >= 4.27.0
Requires:         python2-oslo-i18n >= 3.15.3
Requires:         python2-oslo-log >= 3.36.0
Requires:         python2-oslo-messaging >= 5.29.0
Requires:         python2-oslo-middleware >= 3.31.0
Requires:         python2-oslo-policy >= 1.30.0
Requires:         python2-oslo-serialization >= 2.18.0
Requires:         python2-oslo-service >= 1.24.0
Requires:         python2-oslo-utils >= 3.33.0

Requires:         python2-osprofiler >= 1.4.0
Requires:         python2-jsonschema
Requires:         python2-babel
Requires:         python2-jinja2

Requires:         python-httplib2
Requires:         python2-passlib

%description -n   python-%{service}
%{common_desc}

This package contains the %{service} python library.

%package -n python-%{service}-tests
Summary:        Trove tests
Requires:       python-%{service} = %{epoch}:%{version}-%{release}

%description -n python-%{service}-tests
%{common_desc}

This package contains the Trove test files

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack %{service}


%description      doc
%{common_desc}

This package contains documentation files for %{service}.
%endif

%prep
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
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

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
install -p -D -m 640 etc/%{service}/trove-taskmanager.conf.sample %{buildroot}%{_sysconfdir}/%{service}/trove-taskmanager.conf
install -p -D -m 640 etc/%{service}/trove-conductor.conf.sample %{buildroot}%{_sysconfdir}/%{service}/trove-conductor.conf
install -p -D -m 640 etc/%{service}/trove-guestagent.conf.sample %{buildroot}%{_sysconfdir}/%{service}/trove-guestagent.conf
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
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
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

%files -n python-%{service}
%license LICENSE
%{python2_sitelib}/%{service}
%{python2_sitelib}/%{service}-%{version}*.egg-info
%exclude %{python2_sitelib}/%{service}/tests

%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
