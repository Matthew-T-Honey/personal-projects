extends Node2D
@onready var hex_grid: TileMapLayer = $".."
@onready var characters: Node2D = $"../Characters"
@onready var main: Node2D = $"../.."

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	update_fow()
	



func update_fow() -> void:
	
	var selected = false
	for character in characters.get_children():
		if character.control.selected==true:
			selected=true
	for tile in hex_grid.get_used_cells():
		

		var rendered = false
		for character in characters.get_children():
			if character.faction==0 and abs(character.hex_position.y-tile.y)<7:
				rendered=true
		
		var tile_alt = hex_grid.get_cell_alternative_tile(tile)
		var atlas_coords = hex_grid.get_cell_atlas_coords(tile)
		var source_id = hex_grid.get_cell_source_id(tile)
		if rendered:
			var valid = false
			
			for character in characters.get_children():
				if hex_grid.in_los(character.hex_position,tile) and character.faction==0 and (character.control.selected==true or selected == false):
					if hex_grid.char_in_los(character.hex_position,tile):
						valid = true
					else:
						hex_grid.set_cell(tile,source_id,atlas_coords,1)
						tile_alt = 1
						
			
			if valid:
				hex_grid.set_cell(tile,source_id,atlas_coords,0)
			else:
				if tile_alt == 2 and not main.debug:
					hex_grid.set_cell(tile,source_id,atlas_coords,2)
				else:
					hex_grid.set_cell(tile,source_id,atlas_coords,1)
		else:
			if tile_alt == 2 and not main.debug:
				hex_grid.set_cell(tile,source_id,atlas_coords,2)
			else:
				hex_grid.set_cell(tile,source_id,atlas_coords,1)
			

	for character in characters.get_children():
		var was_visible=character.visible
		character.visible=false
		if character.control.selected==true or (character.faction==0 and not selected) or main.debug:
			character.visible=true
		else:
			
			for character2 in characters.get_children():
				if (hex_grid.char_in_los(character2.hex_position,character.hex_position) or (was_visible and character.body.animation=="Run")) and character2.faction==0:
					character.visible=true
				


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	pass
