extends Node2D

@onready var character = $".."
@onready var characters = $"../.."
@onready var hex_grid = $"../../.."
@onready var main = $"../../../.."



func is_valid(tile) -> bool:
	return tile in get_moves()


func get_moves() -> Array:
	var moves = []
	for tile in hex_grid.get_surrounding_cells(character.hex_position):
		if hex_grid.get_cell_source_id(tile) not in [1,3]:
			moves.append(tile)

	return moves

func execute_move(tile) -> void:
	if !is_valid(tile):
		print("Invalid Move")
	elif hex_grid.get_location(tile) == null:
		character.hex_position = tile
		character.target_position = hex_grid.map_to_local(character.hex_position)
		character.body.animation="Run"
		main.update_fow()
	else:
		character.shaketime = Time.get_unix_time_from_system()
		character.shaking=true
		
