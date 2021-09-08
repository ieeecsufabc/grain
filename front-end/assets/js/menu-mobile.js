jQuery(document).ready(function() {
	jQuery('.toggle-nav').click(function(e) {
		jQuery(this).toggleClass('active');
		jQuery('#menu-nav').toggleClass('active');

		e.preventDefault();
	});
});