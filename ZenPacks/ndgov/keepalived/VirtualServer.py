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


import os
import sys
from Products.ZenModel.Device import Device
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.interfaces.component import IComponentInfo
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from zope.interface import implements
from Products.Zuul.form import schema
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.device import DeviceInfo
from Products.Zuul.utils import ZuulMessageFactory as _t


class VirtualServer(DeviceComponent, ManagedEntity):
    meta_type = portal_type = 'VirtualServer'

    Klasses = [DeviceComponent, ManagedEntity]

    VirtualServerPersistTimeout = None
    VirtualServerNameOfGroup = None
    VirtualServerFwMark = None
    VirtualServerProtocol = None
    VirtualServerRealServersTotal = None
    VirtualServerAddress = None
    VirtualServerStatus = None
    VirtualServerIndex = None
    VirtualServerPort = None
    VirtualServerType = None
    VirtualServerVirtualHost = None
    VirtualServerLoadBalancingAlgo = None
    VirtualServerPersist = None

    _properties = ()
    for Klass in Klasses:
        _properties = _properties + getattr(Klass, '_properties', ())

    _properties = _properties + (
        {'id': 'VirtualServerPersistTimeout', 'type': 'string', 'mode': 'w'},
        {'id': 'VirtualServerNameOfGroup', 'type': 'string', 'mode': 'w'},
        {'id': 'VirtualServerFwMark', 'type': 'string', 'mode': 'w'},
        {'id': 'VirtualServerProtocol', 'type': 'string', 'mode': 'w'},
        {'id': 'VirtualServerRealServersTotal', 'type': 'string', 'mode': 'w'},
        {'id': 'VirtualServerAddress', 'type': 'string', 'mode': 'w'},
        {'id': 'VirtualServerStatus', 'type': 'string', 'mode': 'w'},
        {'id': 'VirtualServerIndex', 'type': 'string', 'mode': 'w'},
        {'id': 'VirtualServerPort', 'type': 'string', 'mode': 'w'},
        {'id': 'VirtualServerType', 'type': 'string', 'mode': 'w'},
        {'id': 'VirtualServerVirtualHost', 'type': 'string', 'mode': 'w'},
        {'id': 'VirtualServerLoadBalancingAlgo', 'type': 'string', 'mode': 'w'},
        {'id': 'VirtualServerPersist', 'type': 'string', 'mode': 'w'},
        )

    _relations = ()
    for Klass in Klasses:
        _relations = _relations + getattr(Klass, '_relations', ())

    _relations = _relations + (
        ('keepaliveddevice', ToOne(ToManyCont, 'ZenPacks.ndgov.keepalived.KeepalivedDevice', 'virtualservers',)),
        )

    factory_type_information = ({
        'actions': ({
            'id': 'perfConf',
            'name': 'Template',
            'action': 'objTemplates',
            'permissions': (ZEN_CHANGE_DEVICE,),
            },),
        },)

    def device(self):
        '''
        Return device under which this component/device is contained.
        '''
        obj = self

        for i in range(200):
            if isinstance(obj, Device):
                return obj

            try:
                obj = obj.getPrimaryParent()
            except AttributeError as exc:
                raise AttributeError(
                    'Unable to determine parent at %s (%s) '
                    'while getting device for %s' % (
                        obj, exc, self))

    def manage_deleteComponent(self, REQUEST=None):
        """
        Delete Component
        """
        try:
            # Default to using built-in method in Zenoss >= 4.2.4.
            return super(VirtualServer, self).manage_deleteComponent(REQUEST)
        except AttributeError:
            # Fall back to copying the Zenoss 4.2.4 implementation.
            url = None
            if REQUEST is not None:
                url = self.device().absolute_url()
            self.getPrimaryParent()._delObject(self.id)
            if REQUEST is not None:
                REQUEST['RESPONSE'].redirect(url)

    def getRRDTemplateName(self):
        return 'KeepalivedVirtualServer'


class IVirtualServerInfo(IComponentInfo):

    VirtualServerPersistTimeout = schema.TextLine(title=_t(u'VirtualServerPersistTimeouts'), readonly=True)
    VirtualServerNameOfGroup = schema.TextLine(title=_t(u'VirtualServerNameOfGroups'), readonly=True)
    VirtualServerFwMark = schema.TextLine(title=_t(u'VirtualServerFwMarks'), readonly=True)
    VirtualServerProtocol = schema.TextLine(title=_t(u'VirtualServerProtocols'), readonly=True)
    VirtualServerRealServersTotal = schema.TextLine(title=_t(u'VirtualServerRealServersTotals'), readonly=True)
    VirtualServerAddress = schema.TextLine(title=_t(u'VirtualServerAddresses'), readonly=True)
    VirtualServerStatus = schema.TextLine(title=_t(u'VirtualServerStatuses'), readonly=True)
    VirtualServerIndex = schema.TextLine(title=_t(u'VirtualServerIndexes'), readonly=True)
    VirtualServerPort = schema.TextLine(title=_t(u'VirtualServerPorts'), readonly=True)
    VirtualServerType = schema.TextLine(title=_t(u'VirtualServerTypes'), readonly=True)
    VirtualServerVirtualHost = schema.TextLine(title=_t(u'VirtualServerVirtualHosts'), readonly=True)
    VirtualServerLoadBalancingAlgo = schema.TextLine(title=_t(u'VirtualServerLoadBalancingAlgoes'), readonly=True)
    VirtualServerPersist = schema.TextLine(title=_t(u'VirtualServerPersists'), readonly=True)


class VirtualServerInfo(ComponentInfo):
    implements(IVirtualServerInfo)

    VirtualServerPersistTimeout = ProxyProperty('VirtualServerPersistTimeout')
    VirtualServerNameOfGroup = ProxyProperty('VirtualServerNameOfGroup')
    VirtualServerFwMark = ProxyProperty('VirtualServerFwMark')
    VirtualServerProtocol = ProxyProperty('VirtualServerProtocol')
    VirtualServerRealServersTotal = ProxyProperty('VirtualServerRealServersTotal')
    VirtualServerAddress = ProxyProperty('VirtualServerAddress')
    VirtualServerStatus = ProxyProperty('VirtualServerStatus')
    VirtualServerIndex = ProxyProperty('VirtualServerIndex')
    VirtualServerPort = ProxyProperty('VirtualServerPort')
    VirtualServerType = ProxyProperty('VirtualServerType')
    VirtualServerVirtualHost = ProxyProperty('VirtualServerVirtualHost')
    VirtualServerLoadBalancingAlgo = ProxyProperty('VirtualServerLoadBalancingAlgo')
    VirtualServerPersist = ProxyProperty('VirtualServerPersist')
