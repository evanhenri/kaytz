#!/bin/bash

set -o pipefail

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root";
   exit 1;
else
    echo "Root user detected";
fi;

# ------------------------------------------------------------------

PIP_VERSION=9.0.1;
#PYTHON_VERSION=3.6.1;
USER=nonce;

apt-get update && apt-get install -y --no-install-recommends \
    libsasl2-dev \
    libssl-dev \
    python-minimal \
    python-pkg-resources \
    python-pip \
    python-setuptools

# ------------------------------------------------------------------

#if [ $(python3 --version | awk '{print $2}') == ${PYTHON_VERSION} ]; then
#    echo "python version ${PYTHON_VERSION} already installed";
#else
#    echo "Upgrading python to version ${PYTHON_VERSION}";
#
#    pushd /tmp
#    wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz
#    tar -xvf Python-${PYTHON_VERSION}.tar.xz
#    pushd Python-${PYTHON_VERSION}
#    ./configure && make && make install
#    popd
#    rm -rf Python-${PYTHON_VERSION}.tar.xz Python-${PYTHON_VERSION}
#    popd
#fi;

# ------------------------------------------------------------------

if [ $(python2 -m pip --version | awk '{print $2}') == ${PIP_VERSION} ]; then
    echo "pip version ${PIP_VERSION} already installed";
else
    echo "Upgrading pip to version ${PIP_VERSION}";

    pushd /tmp
    wget https://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-9.0.1.tar.gz#md5=35f01da33009719497f01a4ba69d63c9
    tar -xzvf pip-${PIP_VERSION}.tar.gz
    pushd pip-${PIP_VERSION}
    python2 setup.py install
    popd
    rm -rf pip-${PIP_VERSION}.tar.gz pip-${PIP_VERSION}
    popd
fi;

# ------------------------------------------------------------------

if id -Gn "${USER}" | grep -qw sudo; then
    echo "${USER} already in sudo group";
else
    echo "Adding ${USER} to sudo group";
    usermod -aG sudo "${USER}";
fi;

# ------------------------------------------------------------------

if grep -qw -- '%sudo   ALL=(ALL:ALL) NOPASSWD: ALL' /etc/sudoers; then
    echo "Sudoers file already up to date";
else
    echo "Updating sudoers file";
    sed -i -r 's/%sudo.*/%sudo   ALL=(ALL:ALL) NOPASSWD: ALL/g' /etc/sudoers;
fi;

# ------------------------------------------------------------------

#if pcregrep -Mq 'export VISUAL=/usr/bin/vi\nexport EDITOR="\${VISUAL}"' /home/${USER}/.bashrc; then
#	echo "Text editor environment variables already set";
#else
#    echo "Setting text editor environment variables";
#    echo -e 'export VISUAL=/usr/bin/vi\nexport EDITOR="${VISUAL}"' >> /home/${USER}/.bashrc;
#fi;

# ------------------------------------------------------------------

# Setup bridged networking
echo "Writing networking interface config";
cat <<EOF >/etc/network/interfaces
source /etc/network/interfaces.d/*.conf

auto lo
iface lo inet loopback

auto enp2s0
iface enp2s0 inet static
    address 192.168.0.101
    broadcast 192.168.0.255
    dns-nameservers 8.8.8.8 8.8.4.4
    gateway 192.168.0.1
    netmask 255.255.255.0
EOF
