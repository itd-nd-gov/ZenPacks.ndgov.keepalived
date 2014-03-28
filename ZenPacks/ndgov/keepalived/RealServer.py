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


class RealServer(DeviceComponent, ManagedEntity):
    meta_type = portal_type = 'RealServer'

    Klasses = [DeviceComponent, ManagedEntity]

    realServerType = None
    realServerPort = None
    realServerAddress = None
    realServerStatus = None
    realServerIndex = None
    realServerWeight = None

    _properties = ()
    for Klass in Klasses:
        _properties = _properties + getattr(Klass, '_properties', ())

    _properties = _properties + (
        {'id': 'realServerType', 'type': 'string', 'mode': 'w'},
        {'id': 'realServerPort', 'type': 'string', 'mode': 'w'},
        {'id': 'realServerAddress', 'type': 'string', 'mode': 'w'},
        {'id': 'realServerStatus', 'type': 'string', 'mode': 'w'},
        {'id': 'realServerIndex', 'type': 'string', 'mode': 'w'},
        {'id': 'realServerWeight', 'type': 'string', 'mode': 'w'},
        )

    _relations = ()
    for Klass in Klasses:
        _relations = _relations + getattr(Klass, '_relations', ())

    _relations = _relations + (
        ('keepaliveddevice', ToOne(ToManyCont, 'ZenPacks.ndgov.keepalived.KeepalivedDevice', 'realservers',)),
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
            return super(RealServer, self).manage_deleteComponent(REQUEST)
        except AttributeError:
            # Fall back to copying the Zenoss 4.2.4 implementation.
            url = None
            if REQUEST is not None:
                url = self.device().absolute_url()
            self.getPrimaryParent()._delObject(self.id)
            if REQUEST is not None:
                REQUEST['RESPONSE'].redirect(url)

    def getRRDTemplateName(self):
        return 'KeepalivedRealServer'

class IRealServerInfo(IComponentInfo):

    realServerType = schema.TextLine(title=_t(u'realServerTypes'), readonly=True)
    realServerPort = schema.TextLine(title=_t(u'realServerPorts'), readonly=True)
    realServerAddress = schema.TextLine(title=_t(u'realServerAddresses'), readonly=True)
    realServerStatus = schema.TextLine(title=_t(u'realServerStatuses'), readonly=True)
    realServerIndex = schema.TextLine(title=_t(u'realServerIndexes'), readonly=True)
    realServerWeight = schema.TextLine(title=_t(u'realServerWeights'), readonly=True)


class RealServerInfo(ComponentInfo):
    implements(IRealServerInfo)

    realServerType = ProxyProperty('realServerType')
    realServerPort = ProxyProperty('realServerPort')
    realServerAddress = ProxyProperty('realServerAddress')
    realServerStatus = ProxyProperty('realServerStatus')
    realServerIndex = ProxyProperty('realServerIndex')
    realServerWeight = ProxyProperty('realServerWeight')
