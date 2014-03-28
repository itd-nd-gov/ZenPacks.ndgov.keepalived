##############################################################################
# Copyright (c) 2014 North Dakota Information Technology Department
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
##############################################################################

import struct
from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )

class VirtualServer(SnmpPlugin):
    relname = 'virtualservers'
    modname = 'ZenPacks.ndgov.keepalived.VirtualServer'

    snmpGetTableMaps = (
        GetTableMap(
            'VirtualServerTable', '1.3.6.1.4.1.9586.100.5.3.3.1', {

                '.2': 'VirtualServerType',
                '.3': 'VirtualServerNameOfGroup',
                '.4': 'VirtualServerFwMark',
                '.6': 'VirtualServerAddress',
                '.7': 'VirtualServerPort',
                '.8': 'VirtualServerProtocol',
                '.9': 'VirtualServerLoadBalancingAlgo',
                '.11': 'VirtualServerStatus',
                '.12': 'VirtualServerVirtualHost',
                '.13': 'VirtualServerPersist',
                '.14': 'VirtualServerPersistTimeout',
                '.20': 'VirtualServerRealServersTotal'
                }
            ),
        )

    def process(self, device, results, log):
        virtual_servers = results[1].get('VirtualServerTable', {})

        rm = self.relMap()
        for snmpindex, row in virtual_servers.items():
            # name = row.get('VirtualServerAddress')
            name = row.get('VirtualServerVirtualHost')
            if not name:
                log.warn('Skipping virtual server with no name')
                continue

            ip = struct.unpack('!4B', row.get('VirtualServerAddress'))
            ipAddress = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(ip[3])

            rm.append(self.objectMap({
                'id': self.prepId(name),
                'title': name + ":" + str(row.get('VirtualServerPort')),
                'snmpindex': snmpindex.strip('.'),
                'VirtualServerType': row.get('VirtualServerType'),
                'VirtualServerNameOfGroup': row.get('VirtualServerNameOfGroup'),
                'VirtualServerFwMark': row.get('VirtualServerFwMark'),
                'VirtualServerAddress': ipAddress,
                'VirtualServerPort': row.get('VirtualServerPort'),
                'VirtualServerProtocol': row.get('VirtualServerProtocol'),
                'VirtualServerLoadBalancingAlgo': row.get('VirtualServerLoadBalancingAlgo'),
                'VirtualServerStatus': row.get('VirtualServerStatus'),
                'VirtualServerVirtualHost': row.get('VirtualServerVirtualHost'),
                'VirtualServerPersist': row.get('VirtualServerPersist'),
                'VirtualServerPersistTimeout': row.get('VirtualServerPersistTimeout'),
                'VirtualServerRealServersTotal': row.get('VirtualServerRealServersTotal'),
                }))

        return rm
