#!/usr/bin/env bash

exec /sbin/setuser root /usr/sbin/kea-dhcp-ddns -c /etc/kea/ddns.json
