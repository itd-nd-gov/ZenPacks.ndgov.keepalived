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


from zope.interface import implements
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.Zuul.form import schema
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.utils import ZuulMessageFactory as _t
from Products.ZenModel.Device import Device
from Products.Zuul.infos.device import DeviceInfo
from Products.Zuul.interfaces import IDeviceInfo
from Products.ZenRelations.RelSchema import ToManyCont, ToOne


class KeepalivedDevice(Device):
    meta_type = portal_type = 'KeepalivedDevice'

    Klasses = [Device]

    _relations = ()
    for Klass in Klasses:
        _relations = _relations + getattr(Klass, '_relations', ())

    _relations = _relations + (
        ('realservers', ToManyCont(ToOne, 'ZenPacks.ndgov.keepalived.RealServer', 'keepaliveddevice',)),
        ('virtualservers', ToManyCont(ToOne, 'ZenPacks.ndgov.keepalived.VirtualServer', 'keepaliveddevice',)),
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



class IKeepalivedDeviceInfo(IDeviceInfo):
    virtualserver_count = schema.Int(title=_t(u'Number of VirtualServers'))
    realserver_count = schema.Int(title=_t(u'Number of RealServers'))


class KeepalivedDeviceInfo(DeviceInfo):
    implements(IKeepalivedDeviceInfo)

    @property
    def virtualserver_count(self):
        # Using countObjects is fast.
        try:
            return self._object.virtualservers.countObjects()
        except:
            # Using len on the results of calling the relationship is slow.
            return len(self._object.virtualservers())

    @property
    def realserver_count(self):
        # Using countObjects is fast.
        try:
            return self._object.realservers.countObjects()
        except:
            # Using len on the results of calling the relationship is slow.
            return len(self._object.realservers())
