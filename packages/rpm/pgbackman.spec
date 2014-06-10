#
# File: pgbackman.spec
#
# Autor: Rafael Martinez <rafael@postgreslq.org.es>
#  

%define majorversion 1.0
%define minorversion 0
%define pbm_owner pgbackman
%define pbm_group pgbackman
%{!?pybasever: %define pybasever %(python -c "import sys;print(sys.version[0:3])")}
%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:        PostgreSQL backup manager
Name:           pgbackman
Version:        %{majorversion}.%{minorversion}
Release:        1%{?dist}
License:        GPLv3
Group:          Applications/Databases
Url:            http://www.pgbackman.org/
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       python-psycopg2 python-argparse at cronie python-setuptools shadow-utils logrotate

%description 
PgBackMan is a tool for managing PostgreSQL logical backups created
with pg_dump and pg_dumpall.

It is designed to manage backups from thousands of databases running
in multiple PostgreSQL nodes, and it supports a multiple backup
servers topology.

It also manages role and database configuration information when
creating a backup of a database. This information is necessary to
ensure a 100% restore of a logical backup of a database and the
elements associated to it.

%prep
%setup -n pgbackman-%{version} -q

%build
python setup_packages.py build

%install
python setup_packages.py install -O1 --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/init.d
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}/var/lib/%{name}
mkdir -p %{buildroot}/var/log/%{name}
install -pm 644 etc/pgbackman.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -m 755 etc/pgbackman_init_rh.sh %{buildroot}%{_sysconfdir}/init.d/%{name}
install -pm 644 etc/pgbackman.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
touch %{buildroot}/var/log/%{name}/%{name}.log

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
#%doc INSTALL NEWS README
%{python_sitelib}/%{name}-%{version}-py%{pybasever}.egg-info/
%{python_sitelib}/%{name}/
%{_bindir}/%{name}*
%{_sysconfdir}/init.d/%{name}*
%{_sysconfdir}/logrotate.d/%{name}*
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%attr(700,%{pbm_owner},%{pbm_group}) %dir /var/lib/%{name}
%attr(755,%{pbm_owner},%{pbm_group}) %dir /var/log/%{name}
%attr(600,%{pbm_owner},%{pbm_group}) %ghost /var/log/%{name}/%{name}.log

%pre
groupadd -f -r pgbackman >/dev/null 2>&1 || :
useradd -M -n -g pgbackman -r -d /var/lib/pgbackman -s /bin/bash \
        -c "PostgreSQL Backup Manager" pgbackman >/dev/null 2>&1 || :

%changelog
* Mon Jun 09 2014 - Rafael Martinez Guerrero <rafael@postgresql.org.es> 1.0.0-1
- New release 1.0.0
