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
import socket
from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )

class RealServer(SnmpPlugin):
    relname = 'realservers'
    modname = 'ZenPacks.ndgov.keepalived.RealServer'

    snmpGetTableMaps = (
        GetTableMap(
            'RealServerTable', '.1.3.6.1.4.1.9586.100.5.3.4.1', {
                '.2': 'RealServerType',
                '.4': 'RealServerAddress',
                '.5': 'RealServerPort',
                '.6': 'RealServerStatus',
                '.7': 'RealServerWeight'
                }
            ),
        )

    def process(self, device, results, log):
        real_servers = results[1].get('RealServerTable', {})

        rm = self.relMap()

        for snmpindex, row in real_servers.items():
            name = row.get('RealServerAddress')
            if not name:
                log.warn('Skipping real server with no name')
                continue

            ip = struct.unpack('!4B', row.get('RealServerAddress'))
            ipAddress = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(ip[3])
            hostname = socket.gethostbyaddr(ipAddress)[0]

            rm.append(self.objectMap({
                'id': self.prepId(snmpindex),
                'title': hostname + ":" + str(row.get('RealServerPort')),
                'snmpindex': snmpindex.strip('.'),
                'realServerType': row.get('RealServerType'),
                'realServerAddress': ipAddress,
                'realServerPort': row.get('RealServerPort'),
                'realServerStatus': row.get('RealServerStatus'),
                'realServerWeight': row.get('RealServerWeight')
                }))

        return rm
