extends Node2D

@onready var character = $".."
@onready var characters = $"../.."
@onready var hex_grid = $"../../.."
@onready var main = $"../../../.."

@onready var controlled = false
@onready var selected = false
@onready var dragging = false
@onready var attacking = []

func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	pass


func distance_to_visible_enemy(tile)-> int:
	var distance=10
	for other_character in characters.get_children():
		if other_character.faction != character.faction:
			if hex_grid.char_in_los(character.hex_position,other_character.hex_position):
				
				distance = min(distance,hex_grid.travel_distance(tile,other_character.hex_position))
	return distance

func get_best_move():
	var attacks = character.attack.get_attacks()
	var moves = character.movement.get_moves()
	
	var distance = distance_to_visible_enemy(character.hex_position)
	
	var visible_enemies=[]
	for other_character in characters.get_children():
		if other_character.faction != character.faction:
			if hex_grid.char_in_los(character.hex_position,other_character.hex_position):
				visible_enemies.append(other_character.hex_position)
	
	var behaviour
	
	if distance > 4:
		behaviour = [1,0,0,0,0,0]
	else:
		behaviour = character.attack.behaviour[distance-1]
	
	var actions = [[],[],[],[],[],[]]
	
	for move in moves:
		if move in visible_enemies:
			pass
		elif len(visible_enemies)==0:
			#if character.hex_position+Vector2i(0,1) not in moves:
				actions[0].append(["Move",move])
		else:
			actions[distance_to_visible_enemy(move)-distance+1].append(["Move",move])
	#if len(visible_enemies)==0 and character.hex_position+Vector2i(0,1) in moves:
		#actions[0].append(["Move",character.hex_position+Vector2i(0,1)])
	
	for attack in attacks:

		for tile in attack:
			if tile in visible_enemies:
				actions[3].append(["Attack",attack])
	
	for attack in attacks:

		for tile in attack:
			for enemy in visible_enemies:
				if tile in hex_grid.get_surrounding_cells(enemy) and hex_grid.get_cell_source_id(enemy) not in [1,3] and hex_grid.travel_distance(character.hex_position,enemy)>hex_grid.travel_distance(character.hex_position,tile):
					actions[4].append(["Attack",attack])
	
	for attack in attacks:
		for tile in attack:
			for enemy in visible_enemies:
				if tile in hex_grid.get_surrounding_cells(enemy) and hex_grid.get_cell_source_id(enemy) not in [1,3] and hex_grid.travel_distance(character.hex_position,enemy)==hex_grid.travel_distance(character.hex_position,tile):
					actions[5].append(["Attack",attack])
	
	
	var total_prob=0
	
	#print("\n",character.name,": ",distance)
	
	#var action_names = ["Adv","Sid","Ret","E Sq","F Sq","S Sq"]
	
	for i in range(6):
		if actions[i] !=[]:
			total_prob+=behaviour[i]
			#print(action_names[i]," Actions: ",behaviour[i])
	
	var remaining_prob=0
	var random = randf_range(0,total_prob)
	
	if total_prob==0:
		#print("No Actions Found")
		return []
	
	for i in range(6):
		if actions[i] !=[]:
			remaining_prob+=behaviour[i]
			if remaining_prob>random:
				#print("Using Behaviour: ",action_names[i])
				return actions[i].pick_random()


	#print("No action found (Reached End)")
	
	return []
	
	
	
	

	
	
	
	
