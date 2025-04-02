extends Node2D

@onready var character = $".."
@onready var characters = $"../.."
@onready var hex_grid = $"../../.."
@onready var attack_weapons: Node2D = $"../../../Attack Weapons"

var behaviour = [[0,0.2,0.5,0.2,0,0.1],
				[0,0.2,0.3,0.1,0.3,0.1],
				[0,0.2,0,0.3,0.3,0.2],
				[0.4,0.3,0,0,0.3,0]]

func is_valid(tiles) -> bool:
	if character.cooldown:
		return false
	if len(tiles) != 1:
		return false
	if tiles[0]==character.hex_position:
		return false
	if not hex_grid.in_los(character.hex_position,tiles[0]):
		return false
	if hex_grid.line_distance(character.hex_position,tiles[0])>3:
		return false
	return true


func get_attack_tiles() -> Array:
	if character.cooldown:
		return []
	var tiles = []
	for i in range(-3,4):
		for j in range(-3,4):
			var V = character.hex_position + Vector2i(i,j)
			if V not in [character.hex_position,character.control.attacking]:
				if len(character.control.attacking)==0:
					if hex_grid.in_los(character.hex_position,V) and hex_grid.line_distance(character.hex_position,V)<4:
						tiles.append(V)
	
	return tiles


func get_attacks() -> Array:
	if character.cooldown:
		return []
	var attacks = []
	for i in range(-3,4):
		for j in range(-3,4):
			var V = character.hex_position + Vector2i(i,j)
			if V not in [character.hex_position,character.control.attacking]:
				if len(character.control.attacking)==0:
					if hex_grid.in_los(character.hex_position,V) and hex_grid.line_distance(character.hex_position,V)<4:
						attacks.append([V])
	
	return attacks


func execute_attack(tiles) -> void:
	for tile in tiles:
		attack_weapons.attack(hex_grid.get_location(tile),tile,character.hex_position,character.weapon)
	
