(function(){

var ZC = Ext.ns('Zenoss.component');

ZC.registerName('RealServer', _t('RealServer'), _t('RealServers'));
ZC.registerName('KeepalivedDevice', _t('KeepalivedDevice'), _t('KeepalivedDevices'));
ZC.registerName('VirtualServer', _t('Virtual Server'), _t('Virtual Servers'));


Ext.apply(Zenoss.render, {
    ZenPacks_ndgov_keepalived_KeepalivedDevice_entityLinkFromGrid: function(obj, col, record) {
        if (!obj)
            return;

        if (typeof(obj) == 'string')
            obj = record.data;

        if (!obj.title && obj.name)
            obj.title = obj.name;

        var isLink = false;

        if (this.refName == 'componentgrid') {
            // Zenoss >= 4.2 / ExtJS4
            if (this.subComponentGridPanel || this.componentType != obj.meta_type)
                isLink = true;
        } else {
            // Zenoss < 4.2 / ExtJS3
            if (!this.panel || this.panel.subComponentGridPanel)
                isLink = true;
        }

        if (isLink) {
            return '<a href="javascript:Ext.getCmp(\'component_card\').componentgrid.jumpToEntity(\''+obj.uid+'\', \''+obj.meta_type+'\');">'+obj.title+'</a>';
        } else {
            return obj.title;
        }
    },
});

ZC.realServerPanel = Ext.extend(ZC.ZenPacks_ndgov_keepalived_keepalivedDeviceComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'RealServer',
            autoExpandColumn: 'name',
            sortInfo: {
                field: 'name',
                direction: 'asc',
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'meta_type'},
                {name: 'status'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'realServerIndex'},
                {name: 'realServerPort'},
                {name: 'realServerType'},
                {name: 'realServerAddress'},
                {name: 'realServerWeight'},
                {name: 'realServerStatus'},
                {name: 'locking'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                renderer: Zenoss.render.NetBotz_entityLinkFromGrid,
                sortable: true
            },{
                dataIndex: 'realServerIndex',
                header: _t('realServerIndex'),
                sortable: true,
                width: 10,
                id: 'realServerIndex'
            },{
                dataIndex: 'realServerPort',
                header: _t('realServerPort'),
                sortable: true,
                width: 10,
                id: 'realServerPort'
            },{
                dataIndex: 'realServerType',
                header: _t('realServerType'),
                sortable: true,
                width: 10,
                id: 'realServerType'
            },{
                dataIndex: 'realServerAddress',
                header: _t('realServerAddress'),
                sortable: true,
                width: 10,
                id: 'realServerAddress'
            },{
                dataIndex: 'realServerWeight',
                header: _t('realServerWeight'),
                sortable: true,
                width: 10,
                id: 'realServerWeight'
            },{
                dataIndex: 'realServerStatus',
                header: _t('realServerStatus'),
                sortable: true,
                width: 10,
                id: 'realServerStatus'
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 70
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });

        ZC.realServerPanel.superclass.constructor.call(
            this, config);
    }
});

Ext.reg('realServerPanel', ZC.realServerPanel);

ZC.virtualServerPanel = Ext.extend(ZC.ZenPacks_ndgov_keepalived_KeepalivedDeviceComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'VirtualServer',
            autoExpandColumn: 'name',
            sortInfo: {
                field: 'virtualServerVirtualHost',
                direction: 'asc',
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'meta_type'},
                {name: 'status'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'virtualServerIndex'},
                {name: 'virtualServerType'},
                {name: 'virtualServerNameOfGroup'},
                {name: 'virtualServerFwMark'},
                {name: 'virtualServerAddress'},
                {name: 'virtualServerPort'},
                {name: 'virtualServerProtocol'},
                {name: 'virtualServerLoadBalancingAlgo'},
                {name: 'virtualServerStatus'},
                {name: 'virtualServerVirtualHost'},
                {name: 'virtualServerPersist'},
                {name: 'virtualServerPersistTimeout'},
                {name: 'virtualServerRealServersTotal'},
                {name: 'locking'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                renderer: Zenoss.render.NetBotz_entityLinkFromGrid,
                sortable: true
            },{
                dataIndex: 'virtualServerType',
                header: _t('virtual Server Type'),
                sortable: true,
                width: 10,
                id: 'virtualServerType'
            },{
                dataIndex: 'virtualServerNameOfGroup',
                header: _t('virtual Server Name Of Group'),
                sortable: true,
                width: 10,
                id: 'virtualServerNameOfGroup'
            },{
                dataIndex: 'virtualServerFwMark',
                header: _t('virtual Server FwMark'),
                sortable: true,
                width: 10,
                id: 'virtualServerFwMark'
            },{
                dataIndex: 'virtualServerAddress',
                header: _t('virtual Server Address'),
                sortable: true,
                width: 15,
                id: 'virtualServerAddress'
            },{
                dataIndex: 'virtualServerPort',
                header: _t('virtual Server Port'),
                sortable: true,
                width: 10,
                id: 'virtualServerPort'
            },{
                dataIndex: 'virtualServerProtocol',
                header: _t('virtual Server Protocol'),
                sortable: true,
                width: 10,
                id: 'virtualServerProtocol'
            },{
                dataIndex: 'virtualServerLoadBalancingAlgo',
                header: _t('virtual Server LoadBalancing Algorithm'),
                sortable: true,
                width: 10,
                id: 'virtualServerLoadBalancingAlgo'
            },{
                dataIndex: 'virtualServerStatus',
                header: _t('virtual Server Status'),
                sortable: true,
                width: 10,
                id: 'virtualServerStatus'
            },{
                dataIndex: 'virtualServerVirtualHost',
                header: _t('virtual Server Virtual Host'),
                sortable: true,
                width: 25,
                id: 'virtualServerVirtualHost'
            },{
                dataIndex: 'virtualServerPersist',
                header: _t('virtual Server Persist'),
                sortable: true,
                width: 10,
                id: 'virtualServerPersist'
            },{
                dataIndex: 'virtualServerPersistTimeout',
                header: _t('virtual Server Persist Timeout'),
                sortable: true,
                width: 10,
                id: 'virtualServerPersistTimeout'
            },{
                dataIndex: 'virtualServerRealServersTotal',
                header: _t('virtual Server Real Servers Total'),
                sortable: true,
                width: 10,
                id: 'virtualServerRealServersTotal'
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 70
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });

        ZC.virtualServerPanel.superclass.constructor.call(
            this, config);
    }
});

Ext.reg('virtualServerPanel', ZC.virtualServerPanel);


})();
