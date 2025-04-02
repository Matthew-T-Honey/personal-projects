extends Node2D

@onready var character = $".."
@onready var characters = $"../.."
@onready var hex_grid = $"../../.."
@onready var attack_weapons: Node2D = $"../../../Attack Weapons"

var behaviour = [[0,0.4,0,0.6,0,0],
				[0.5,0.2,0,0,0.3,0],
				[0.8,0.2,0,0,0,0],
				[0.9,0.1,0,0,0,0]]

func is_valid(tiles) -> bool:
	if character.cooldown:
		return false
	if len(tiles) != 2:
		return false
	if character.hex_position in tiles:
		return false
	if not hex_grid.in_los(character.hex_position,tiles[0]) or not hex_grid.in_los(character.hex_position,tiles[1]):
		return false
	if hex_grid.line_distance(character.hex_position,tiles[0])+hex_grid.line_distance(character.hex_position,tiles[1])==2 and tiles[0] in hex_grid.get_surrounding_cells(tiles[1]):
		return true
	else:
		return false


func get_attack_tiles() -> Array:
	if character.cooldown:
		return []
	var tiles = []
	for i in range(-1,2):
		for j in range(-1,2):
			var V = character.hex_position + Vector2i(i,j)
			if V not in [character.hex_position,character.control.attacking]:
				if len(character.control.attacking)==0:
					if hex_grid.in_los(character.hex_position,V) and hex_grid.line_distance(character.hex_position,V)==1:
						tiles.append(V)
				elif len(character.control.attacking)==1:
					if is_valid([character.control.attacking[0],V]):
						tiles.append(V)

	return tiles


func get_attacks() -> Array:
	if character.cooldown:
		return []
	var attacks = []
	for tile1 in hex_grid.get_surrounding_cells(character.hex_position):
		for tile2 in hex_grid.get_surrounding_cells(character.hex_position):
			if tile1 in hex_grid.get_surrounding_cells(tile2) and [tile1,tile2] not in attacks and [tile2,tile1] not in attacks:
				attacks.append([tile1,tile2])
	
	return attacks
	
	

func execute_attack(tiles) -> void:
	for tile in tiles:
		attack_weapons.attack(hex_grid.get_location(tile),tile,character.hex_position,character.weapon)
	
	
