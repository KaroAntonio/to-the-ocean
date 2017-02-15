var game_objs, msgs;

var width = window.innerWidth,
	height = window.innerHeight;

$(document).ready(function() {
	$.getJSON( "assets/scenes.json", function( scenes ) {

		game_objs = init_game(width, height, scenes);

		$('#loading').hide();
		//loop();
	});
})

function loop() {
	update(game_objs);
	requestAnimationFrame(loop);	
}


