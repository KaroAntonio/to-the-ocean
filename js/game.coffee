# This holds all the game logic **NO DRAWING** just the logix
window.init_game = (w, h, scenes) ->
	# initialize and return game objects	
	# objs scenes are in pixels, where the top left is 0,0
	# sprite keys are unique
	#
	#
	n = 1
	size = 30
	# game objects
	go =
		colors: init_colors()
		start: get_time()
		w: w
		h: h
		mouseX: w / 2
		mouseY: h / 2
		score:0
		t:0  # update count
		paused: true
		scenes: scenes
	
	init_listeners go
	init_scenes go

	go

window.update = (go) ->
	if not go.paused
		go.t += 1

add_toc_button = (go,parent) ->
	toc_button = $('<div>')
	toc_button.css
		cursor: 'pointer'
		paddingTop: 20

	toc_button.appendTo(parent)
	toc_button.text '~Table of Contents~'
	toc_button.click () ->
		show_scene(go,0)

init_scenes = (go) ->

	$('body').css
		fontFamily: 'monospace'

	go.scene_frame = $('<div>')
	go.scene_frame.attr
		id: 'scene-frame'

	go.scene_frame.css
		paddingLeft: 200
		paddingTop: 80
		paddingBottom: 200
		width:go.w - 400
		fontFamily: 'monospace'

	$('body').append go.scene_frame
	show_scene(go,0)
	
show_scene = (go,i) ->
	# where i is the scene number
	go.scene_frame.empty()
	
	idx = Math.floor(Math.random() * go.scenes[i].length)
	scene_data = go.scenes[i][idx]
	for token in scene_data.scene
		if token[token.type] == '<br>'
			token_div = $('<br>')
		else
			token_div = $('<div>')
			token_div.text token[token.type]
		token_div.css
			display: 'inline-block'
			paddingRight: 10
			fontSize: 20

		if token.scene
			token_div.css
				cursor: 'pointer'
				fontWeight: 'bold'

			do(token) ->
				token_div.click (e) ->
					show_scene(go,token.scene)

		if token.img
			token_div.css
				content:'url(assets/imgs/'+token.img+')'
				width: 200
				height: 'auto'

		go.scene_frame.append token_div
	
	add_toc_button(go,go.scene_frame)

init_colors = () ->
	seed: get_random_color()
	primary: get_random_color()

init_listeners = (go) ->
	# mouse listener
	$(document).mousemove (e) ->
		go['mouseX'] = e.clientX
		go['mouseY'] = e.clientY

	# keyboard listener
	handler = (e) ->
		if not go.paused
			key_map =
				32:'lamp'
		else
			$('body').css
				cursor: 'none'
			go.paused = false

	$(document).keypress(handler)

restart = (go) ->
	# clean up current level
	go.colors = init_colors()

get_time = ->
	d = new Date()
	d.getTime()

get_random_color = ->
	letters = '0123456789ABCDEF'
	color = '#'
	for i in [0..5]
		color += letters[Math.floor(Math.random() * 16)]
	color
