#!/usr/bin/env bash

rpm -ivh http://yum.postgresql.org/9.3/redhat/rhel-6-x86_64/pgdg-centos93-9.3-1.noarch.rpm
rpm -ivh http://yum.postgresql.org/9.2/redhat/rhel-6-x86_64/pgdg-centos92-9.2-6.noarch.rpm
rpm -ivh http://yum.postgresql.org/9.1/redhat/rhel-6-x86_64/pgdg-centos91-9.1-4.noarch.rpm
rpm -ivh http://yum.postgresql.org/9.0/redhat/rhel-6-x86_64/pgdg-centos90-9.0-5.noarch.rpm

yum -y install python-setuptools gcc postgresql93 postgresql92 postgresql91 postgresql90 python-devel python-psycopg2 python-argparse

echo "10.10.10.101   pg-backup01.example.net   pg-backup01" >> /etc/hosts
echo "10.10.10.102   pg-backup02.example.net   pg-backup02" >> /etc/hosts
echo "10.10.10.103   pg-node01.example.net   pg-node01" >> /etc/hosts
echo "10.10.10.104   pgbackmandb.example.net   pgbackmandb" >> /etc/hosts

