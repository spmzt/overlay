#!/usr/local/bin/python3.9
import io
import yaml
import ipaddress
import configparser

config = configparser.ConfigParser()
config.read('inventory.txt')
section_freebsd = config['freebsd']

# overlay subnet generator

master_subnet = config['ipam']['master_subnet']
prefix_length = config['ipam']['prefix_length']
freebsd_hosts = []
for key in section_freebsd:
    freebsd_hosts.append(key.split(' ')[0])

subnets = list(ipaddress.ip_network(master_subnet).subnets(new_prefix=int(prefix_length)))

freebsd_subnets = {}
for host_a in freebsd_hosts:
    freebsd_subnets[host_a] = {}

i = 0
freebsd_hosts_temp = freebsd_hosts
for host_a in freebsd_hosts:
    for host_b in freebsd_hosts_temp:
        if host_a != host_b:
            freebsd_subnets[host_a][host_b] = { 'ip': str(subnets[i][1]), 'vni': i}
            freebsd_subnets[host_b][host_a] = { 'ip': str(subnets[i][2]), 'vni': i}
        i += 1
    freebsd_hosts.remove(host_a)

with io.open('ipam.yml', 'w') as ipam_file:
    yaml.dump(freebsd_subnets, ipam_file)

# Jail epair subnet generator 

jail_master_subnet = config['ipam']['jail_master_subnet']
jail_prefix_length = config['ipam']['jail_prefix_length']

subnets = list(ipaddress.ip_network(jail_master_subnet).subnets(new_prefix=int(jail_prefix_length)))

freebsd_hosts = []
for key in section_freebsd:
    freebsd_hosts.append(key.split(' ')[0])

jail_subnets = {}
j = 1
for jail in freebsd_hosts:
    jail_subnets[jail] = {'epair1' : {'jail': str(subnets[j][1]), 'host': str(subnets[j][2]), 'vni': j, 'prefix': jail_prefix_length},
                          'epair2' : {'jail': str(subnets[j+1][1]), 'host': str(subnets[j+1][2]), 'vni': j+1, 'prefix': jail_prefix_length}}
    j += 2

with io.open('jail_ipam.yml', 'w') as ipam_file:
    yaml.dump(jail_subnets, ipam_file)

# VPN epair subnet generator 

vpn_master_subnet = config['ipam']['vpn_master_subnet']
vpn_prefix_length = config['ipam']['vpn_prefix_length']

subnets = list(ipaddress.ip_network(vpn_master_subnet).subnets(new_prefix=int(vpn_prefix_length)))

freebsd_hosts = []
for key in section_freebsd:
    freebsd_hosts.append(key.split(' ')[0])

vpn_subnets = {}
j = 1
for jail in freebsd_hosts:
    vpn_subnets[jail] = {'ocserv' : {'jail': str(subnets[j][1]), 'prefix': vpn_prefix_length}}
    j += 1

with io.open('vpn_ipam.yml', 'w') as ipam_file:
    yaml.dump(vpn_subnets, ipam_file)
