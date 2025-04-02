extends TileMapLayer

var spawn_locations: Array = [Vector2i(0,-2),Vector2i(2,-2),Vector2i(-2,-2)]#,Vector2i(0,-1),Vector2i(0,0)]#
@onready var characters: Node2D = $Characters
@onready var main: Node2D = $".."



func get_location(tile):
	for character in characters.get_children():
		if character.hex_position == tile:
			return character
	#queue_redraw()
	return null


func oddq_to_axial(hex):
	var q = hex.x
	var r = hex.y - (hex.x - abs(hex.x%2)) / 2
	return Vector2i(q, r)
	
func line_distance(tile_1,tile_2) -> int:
	var a = oddq_to_axial(tile_1)
	var b = oddq_to_axial(tile_2)
	
	return (abs(a.x - b.x) + abs(a.x + a.y - b.x - b.y) + abs(a.y - b.y)) / 2

func travel_distance(tile_1,tile_2) -> int:

	if tile_1==tile_2:
		return 0
	var searched=[tile_1]
	var new_searched=[tile_1]

	for distance in range(10):
		for tile in searched:
			for next_tile in get_surrounding_cells(tile):
				if next_tile==tile_2:
					return distance+1
				if next_tile not in new_searched and get_cell_source_id(next_tile) not in [1,3]:
					new_searched.append(next_tile)
		searched=new_searched.duplicate()
	
	return 10




func char_in_los(tile_1,tile_2) -> bool:
	if in_los(tile_1,tile_2) and (get_cell_source_id(tile_2) != 2 or tile_2 in get_surrounding_cells(tile_1) or tile_1==tile_2):
		return true
	else:
		return false
		

func in_los(tile_1,tile_2) -> bool:
	
	var distance = line_distance(tile_1,tile_2)
	var tile_1_coords = map_to_local(tile_1)
	var tile_2_coords = map_to_local(tile_2)
	var increment = (tile_2_coords-tile_1_coords)/distance
	var perpendicular = Vector2(increment.y,-increment.x).normalized()
	if distance>5:
		return false
	
	var valid = true
	for i in range(1,distance):
		var tile_left = local_to_map(tile_1_coords + increment*i + perpendicular)
		var tile_right = local_to_map(tile_1_coords + increment*i - perpendicular)
		var source_left = get_cell_source_id(tile_left)
		var source_right = get_cell_source_id(tile_right)
		if (source_left in [1] and source_right in [1]) or (source_left in [1,4] and source_right in [1,4] and get_cell_source_id(tile_2) != 1) or (source_left in [1,2,4] and source_right in [1,2,4] and get_cell_source_id(tile_1) != 4 and get_cell_source_id(tile_2) != 4):
			valid = false
		
		#if !(!(source_left in [1,2,4] and source_right in [1,2,4]) and !(get_cell_source_id(tile_1) == 4 and get_cell_source_id(tile_2) == 4 and source_left in [1,4] and source_right in [1,4]) and !(get_cell_source_id(tile_2) == 1 and source_left in [1] and source_right in [1])):
			#valid = false
	
	return valid
