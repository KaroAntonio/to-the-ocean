import json
import re

def build_opts_dict(opts_str):
	t = [ e.strip() for e in re.split(':|,',opts_str) ]
	return { eval(t[i*2]):eval(t[i*2+1]) for i in range(len(t)/2) }

def parse_markup(s):
	''' parse string s into a list of dicts formatted as
	{
	'type':[img/text]
	if text
		'txt':
	if img
		'img path':
	'hover': 'img path'
	'scene': 'next scene num
	}	
	'''
	txt_pattern = '(?:\A|[^!])\[(\s?[^\[]*\s?)\](\{((?:\s?\S*\s?):(?:\s?\S*\s?),?)*\})*'
	img_pattern = '!\[(\s?[^\[]*\s?)\](\{((?:\s?\S*\s?):(?:\s?\S*\s?),?)*\})*'

	# type: pattern
	patterns = {
			'txt':txt_pattern,
			'img':img_pattern
			}

	matches = []
	for t,p in patterns.items():
		matches += [(t.lower(),m) for m in re.finditer(p,s)]

	matches.sort(key=lambda x: x[1].start())
	tokens = []
	last_end = 0
	for typ,m in matches:
		pref = s[last_end:m.start()]
		tokens += [{'type':'txt','txt':t.strip()} for t in pref.split()]
		last_end = m.end()
		match_dict = {'type':typ}
		match_dict[typ] = m.group(1)
		if m.group(3):
			opts_dict = build_opts_dict(m.group(3))
			match_dict.update(opts_dict)
		tokens += [match_dict]

	# add that last string of tokens	
	pref = s[last_end:]
	tokens += [{'type':'txt','txt':t.strip()} for t in pref.split()]

	return tokens

def add_scene(scenes,ID, full, options):
	scene = {
		'id':ID, 
		'scene':parse_markup(full), 
		'opts':options
		}
	if ID in scenes:
		scenes[ID] += [scene]
	else: 
		scenes[ID] = [scene]

def load_scenes(filename):
	'''
	Store all scenes from filename (scenes.txt) into the variable "self.scenes"
	however you think is best.
	Remember to keep track of the integer number representing each location.
	Make sure the Location class is used to represent each location.
	Change this docstring as needed.
	:param filename:
	:return:
	'''
	f = open(filename, 'r')
	scenes = {}
	l_i = 0     # location index
	full = ""
	for line in f:
		line=line.strip()
		line = line.replace('\xe2\x80\x99',"'")
		line = line.replace('\xe2\x80\x98',"'")
		if line == "END":
			add_scene(scenes,ID,full,options)
			full = ""
			l_i = -1000

		if line.startswith("SCENE"):
			ID = int(line.split(' ')[1])
			l_i = 0
			full = ""
		else: l_i += 1
		if l_i == 1:
			options = []
			if (line.strip() != '/'):
				parsed_options = line.split('/')
				for o in parsed_options:
					if o != "":
						options.append(o.split(':'))
		if l_i == 2:
			full = line
		if l_i > 2:
			full += " <br> " + line

	return scenes

scenes = load_scenes('assets/scenes.txt')

with open('assets/scenes.json', 'w') as outfile:
	json.dump(scenes, outfile)
