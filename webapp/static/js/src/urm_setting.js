require.config({
	baseUrl: '../static/js',
	paths:{
		jquery: 'lib/jquery',
		bootstrap: 'lib/bootstrap',
		urmmain: 'src/urm_main'
	},
	shim: {
		bootstrap: {
			deps: ['jquery'],
			exports: 'bootstrap'
		}
	}
})

require(['jquery', 'bootstrap', 'urmmain'],function($, bootstrap, urmmain){
	// body...
	
	

})