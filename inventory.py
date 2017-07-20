#!/usr/bin/env python3.6

import argparse
import getpass
import ipaddress

import simplejson

from dynamic_inventory import core


def create_bastions(inventory):
    bastions = inventory.group('bastions')

    def create_bastion01():
        bastion01 = bastions.host('bastion01', ansible_host='192.168.0.101', ansible_user='nonce', domain='nonce.ch')

        k8s_host_prefix = ipaddress.ip_network('10.0.1.0/24')
        bastion01['k8s_bridge']       = 'k8s_br0'
        bastion01['k8s_host_prefix']  = k8s_host_prefix
        bastion01['k8s_gateway']      = k8s_host_prefix[1]
        bastion01['k8s_ip']           = k8s_host_prefix[100]
        bastion01['k8s_dhcp_start']   = k8s_host_prefix[101]
        bastion01['k8s_dhcp_stop']    = k8s_host_prefix[254]
        bastion01['k8s_broadcast']    = k8s_host_prefix.broadcast_address
        bastion01['k8s_netmask']      = k8s_host_prefix.netmask
        bastion01['k8s_prefix']       = k8s_host_prefix.prefixlen
        bastion01['k8s_ptr_record']   = k8s_host_prefix.network_address.reverse_pointer
        bastion01['k8s_node_ssh_rgx'] = f'*.{bastion01["domain"]}'

        bastion01['lxc_user'] = 'ubuntu'

        bastion01['controller_nodes'] = []
        controller_count = 2
        controller_id_width = len(str(controller_count))
        for controller_id in range(1, controller_count):
            name = f'controller{controller_id:0>{controller_id_width}}'
            fqdn = f'{name}.{bastion01["domain"]}'
            bastion01['controller_nodes'].append({
                'ansible_host': None,
                'arch'        : 'amd64',
                'dist'        : 'ubuntu',
                'fqdn'        : fqdn,
                'home'        : f'/var/lib/lxc/{fqdn}/rootfs/home/{bastion01["lxc_user"]}',
                'name'        : name,
                'release'     : 'xenial',
            })

        bastion01['worker_nodes'] = []
        worker_count = 2
        worker_id_width = len(str(worker_count))
        for worker_id in range(1, worker_count):
            name = f'worker{worker_id:0>{worker_id_width}}'
            fqdn = f'{name}.{bastion01["domain"]}'
            bastion01['worker_nodes'].append({
                'ansible_host': None,
                'arch'        : 'amd64',
                'dist'        : 'ubuntu',
                'fqdn'        : fqdn,
                'home'        : f'/var/lib/lxc/{fqdn}/rootfs/home/{bastion01["lxc_user"]}',
                'name'        : name,
                'release'     : 'xenial',
            })

        bastion01['nodes'] = bastion01['controller_nodes'] + bastion01['worker_nodes']

        phys_intf_host_prefix = ipaddress.ip_network('192.168.0.0/24')
        bastion01['phys_intf']                = 'enp2s0'
        bastion01['phys_intf_prefix']         = phys_intf_host_prefix.prefixlen
        bastion01['phys_intf_host_prefix']    = phys_intf_host_prefix
        bastion01['phys_intf_gateway']        = phys_intf_host_prefix[1]
        bastion01['phys_intf_ip']             = phys_intf_host_prefix[101]
        bastion01['phys_intf_broadcast']      = phys_intf_host_prefix.broadcast_address
        bastion01['phys_intf_netmask']        = phys_intf_host_prefix.netmask
        bastion01['phys_intf_ddns_server']    = '127.0.0.1'
        bastion01['phys_intf_dhcp4_server']   = '127.0.0.1'
        bastion01['phys_intf_dns_nameserver'] = '127.0.0.1'
        return bastion01

    inventory['bastion_configs'] = [{
        'ansible_host' : bastion_host['ansible_host'],
        'ansible_user' : bastion_host['ansible_user'],
        'fqdn'         : bastion_host.fqdn
    } for bastion_host in [
        create_bastion01()
    ]]
    return bastions


def create_inventory():
    inventory = core.Inventory()
    return inventory


def create_localhosts(inventory):
    localhosts = inventory.group('localhosts')
    localhosts['ansible_connection'] = 'local'

    pc = localhosts.host(
        'pc',
        ansible_host='127.0.0.1',
        ansible_user=getpass.getuser(),
        domain='localhost'
    )

    return localhosts


def main():
    inventory = create_inventory()
    create_bastions(inventory)
    create_localhosts(inventory)
    return inventory.list()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fancy', action='store_true')
    parser.add_argument('--list', action='store_true', required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    output = main()

    if args.fancy:
        print(simplejson.dumps(output, indent=4, sort_keys=True))
    else:
        print(simplejson.dumps(output))
