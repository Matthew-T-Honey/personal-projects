extends Node2D

@onready var character = $".."
@onready var characters = $"../.."
@onready var hex_grid = $"../../.."
@onready var attack_weapons: Node2D = $"../../../Attack Weapons"

var behaviour = [[0,0.3,0.1,0.5,0,0.1],
				[0.6,0.2,0,0,0.2,0],
				[0.8,0.2,0,0,0,0],
				[0.9,0.1,0,0,0,0]]

func is_valid(tiles) -> bool:
	if character.cooldown:
		return false
	if len(tiles) != 1:
		return false
	if tiles[0]==character.hex_position:
		return false
	if not hex_grid.in_los(character.hex_position,tiles[0]):
		return false
	if hex_grid.line_distance(character.hex_position,tiles[0])!=1:
		return false
	return true


func get_attack_tiles() -> Array:
	if character.cooldown:
		return []
	var tiles = []
	for tile in hex_grid.get_surrounding_cells(character.hex_position):
		if hex_grid.in_los(character.hex_position,tile):
			tiles.append(tile)
	
	return tiles


func get_attacks() -> Array:
	if character.cooldown:
		return []
	var attacks = []
	for tile in hex_grid.get_surrounding_cells(character.hex_position):
		if hex_grid.in_los(character.hex_position,tile):
			attacks.append([tile])
	
	return attacks

func execute_attack(tiles) -> void:
	
	for tile in tiles:
		attack_weapons.attack(hex_grid.get_location(tile),tile,character.hex_position,character.weapon)
