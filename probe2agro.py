#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# probe2agro.py
# Takes nmap probe scan output file and agressively scans the resolved hosts.
#
# First run a probe scan: nmap -Pn -sP 10.0.0.0/24 -oN results.txt
# and then run... sudo python probe2agro.py results.txt
#

import os
import sys
import time


def main():
    if os.geteuid() != 0:
        print('Error: This script must be run as root!')
        sys.exit(1)

    if len(sys.argv) == 2:
        probe_file = sys.argv[1]
    else:
        print('Usage: ./probe2agro.py <probe_scan_file>')
        sys.exit(2)

    if not os.path.isfile(probe_file):
        print('Error: Probe scan file not found!')
        sys.exit(3)

    with open(probe_file) as f:
        probe_scan = f.read().splitlines()

    hosts = []
    for line in probe_scan:
        if ('scan report' in line) and (len(line.split()) == 6):
            fqdn = line.split()[4]
            ip = line.split()[5][1:-1]
            hosts.append((ip, fqdn))

    print('*** Running probe2agro, grab some coffee yo ***')

    output = []
    for h in hosts:
        agro_command = 'nmap -Pn -A {} -oN {}-agroscan.txt'.format(h[0], h[0].replace('.','-'))
        dt_start = time.strftime('%a, %d %b %Y %H:%M:%S {}'.format(time.tzname[0]), time.localtime())
        print('*** Scanning: {} ***'.format(h[0]))
        os.system(agro_command)
        dt_end = time.strftime('%a, %d %b %Y %H:%M:%S {}'.format(time.tzname[0]), time.localtime())
        output.append('TIME START: {}\nTIME END: {}\nCOMMAND: {}\nFQDN: {}\n'.format(
            dt_start, dt_end, agro_command, h[1]))

    for i in output:
        print(i)


if __name__ == '__main__':
    main()
