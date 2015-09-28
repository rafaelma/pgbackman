#!/usr/bin/env bash

rpm -ivh http://yum.postgresql.org/9.1/redhat/rhel-6-x86_64/pgdg-centos91-9.1-4.noarch.rpm
yum -y update
yum -y groupinstall "PostgreSQL Database Server 9.1 PGDG"
yum -y upgrade

echo "10.10.10.101   pg-backup01.example.net   pg-backup01" >> /etc/hosts
echo "10.10.10.102   pg-backup02.example.net   pg-backup02" >> /etc/hosts
echo "10.10.10.103   pg-node01.example.net   pg-node01" >> /etc/hosts
echo "10.10.10.104   pgbackmandb.example.net   pgbackmandb" >> /etc/hosts
echo "10.10.10.105   pg-node02.example.net   pg-node02" >> /etc/hosts

sudo /etc/init.d/postgresql-9.1 initdb

echo "host   all     postgres     10.10.10.101/32            trust" > /var/lib/pgsql/9.1/data/pg_hba.conf
echo "host   all     postgres     10.10.10.102/32            trust" >> /var/lib/pgsql/9.1/data/pg_hba.conf
echo "local  all     all                                     peer" >> /var/lib/pgsql/9.1/data/pg_hba.conf

echo "listen_addresses = '10.10.10.103'" >>   /var/lib/pgsql/9.1/data/postgresql.conf

sudo /etc/init.d/postgresql-9.1 start

