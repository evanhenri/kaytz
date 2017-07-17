#!/usr/bin/env bash

exec /sbin/setuser root /usr/sbin/kea-dhcp4 -c /etc/kea/dhcp4.json
