#!/usr/bin/env bash

echo "10.10.10.105   centos6.example.net   centos6" >> /etc/hosts
echo "10.10.10.106   debian7.example.net   debian7" >> /etc/hosts
echo "10.10.10.107   ubuntu14.example.net   ubuntu14" >> /etc/hosts

apt-get -y update
apt-get -y install git make
apt-get -y upgrade

