plugin.register('wgn', {
	route: '{replace-route}',
	title: 'Default Registration',
	icon: 'icon-bookmark-empty',
	interfaces: [
		{
			controller: 'wgnCntl',
			template: 'wgn-main',
			type: 'fullPage',
			order: 300,
			topNav: true,
			routes: [
				'/:page'
			]
		},
		{
			controller: 'wgnSettingsCntl',
			template: 'wgn-settings',
			type: 'settings'
		}
	]
});
