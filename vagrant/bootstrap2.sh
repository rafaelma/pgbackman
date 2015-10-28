#!/usr/bin/env bash

rpm -ivh http://yum.postgresql.org/9.3/redhat/rhel-6-x86_64/pgdg-centos93-9.3-1.noarch.rpm
yum -y update
yum -y groupinstall "PostgreSQL Database Server 9.3 PGDG"
yum -y upgrade

echo "10.10.10.101   pg-backup01.example.net   pg-backup01" >> /etc/hosts
echo "10.10.10.102   pg-backup02.example.net   pg-backup02" >> /etc/hosts
echo "10.10.10.103   pg-node01.example.net   pg-node01" >> /etc/hosts
echo "10.10.10.104   pgbackmandb.example.net   pgbackmandb" >> /etc/hosts
echo "10.10.10.105   pg-node02.example.net   pg-node02" >> /etc/hosts

sudo /etc/init.d/postgresql-9.3 initdb

echo "host   pgbackman     pgbackman_role_rw     10.10.10.101/32            trust" > /var/lib/pgsql/9.3/data/pg_hba.conf
echo "host   pgbackman     pgbackman_role_rw     10.10.10.102/32            trust" >> /var/lib/pgsql/9.3/data/pg_hba.conf
echo "local  all     all                                     peer" >> /var/lib/pgsql/9.3/data/pg_hba.conf

echo "listen_addresses = '10.10.10.104'" >>   /var/lib/pgsql/9.3/data/postgresql.conf

sudo /etc/init.d/postgresql-9.3 start

