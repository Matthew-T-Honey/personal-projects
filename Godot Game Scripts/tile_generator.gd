extends Node2D

@onready var HexGrid: TileMapLayer = $".."
var width: int = 10 

var MountainSpawnRate = 20
var HillSpawnRate = 40
var ForestSpawnRate = 15
var SwampSpawnRate = 35

var starting_height = 30


func _ready() -> void:
	for k in range(5):
		for j in range (1,-starting_height,-1):
			for i in range(-width + 1,width + 1, 2):
				generate_tile(Vector2i(i,j-k))
			
			
			for i in range(-width,width + 1, 2):
				generate_tile(Vector2i(i,j-k))


func generate_tile(tile) -> void:
	if tile.x < -width + 1 or tile.x > width - 1 or tile.y > 0:
		var atlas_coords = Vector2i (randi_range(0,4),0)
		HexGrid.set_cell(tile,1,atlas_coords,2)
		return
	var Mountain_Count = 0
	var Forest_count = 0
	var Hill_Count = 0
	var Swamp_Count = 0
	for adj_tile in HexGrid.get_surrounding_cells(tile):
		if HexGrid.get_cell_source_id(adj_tile) == 1:
			Mountain_Count += 1
		if HexGrid.get_cell_source_id(adj_tile) == 2:
			Forest_count += 1
		if HexGrid.get_cell_source_id(adj_tile) == 3:
			Swamp_Count += 1
		if HexGrid.get_cell_source_id(adj_tile) == 4:
			Hill_Count += 1
	
	if randi_range(0,MountainSpawnRate) <= Mountain_Count**2 and tile.x != 0 and tile not in HexGrid.spawn_locations: 
		var atlas_coords = Vector2i (randi_range(0,4),0)
		HexGrid.set_cell(tile,1,atlas_coords,2)
	
	elif randi_range(0,HillSpawnRate) <= (Hill_Count + 2*Mountain_Count)**2: 
		var atlas_coords = Vector2i (randi_range(0,4),0)
		HexGrid.set_cell(tile,4,atlas_coords,2)
	
	elif randi_range(0,ForestSpawnRate) <= Forest_count**2: 
		var atlas_coords = Vector2i (randi_range(0,6),0)
		HexGrid.set_cell(tile,2,atlas_coords,2)
		
	elif randi_range(0,SwampSpawnRate) <= (2*Swamp_Count - Mountain_Count) * abs(2*Swamp_Count - Mountain_Count) and tile.x != 0 and tile not in HexGrid.spawn_locations: 
		var atlas_coords = Vector2i (randi_range(0,4),0)
		HexGrid.set_cell(tile,3,atlas_coords,2)
	
	else:
		var atlas_coords = Vector2i (randi_range(0,4),0)
		HexGrid.set_cell(tile,0,atlas_coords,2)


func generate_row(height) -> void:
	for k in range(3):
		for i in range(-width + 1,width + 1, 2):
			generate_tile(Vector2i(i,-height + k))
		
		
		for i in range(-width,width + 1, 2):
			generate_tile(Vector2i(i,-height + k))
