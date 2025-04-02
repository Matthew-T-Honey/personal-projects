extends Node2D
@onready var hex_grid: TileMapLayer = $".."


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	pass


func _draw(): 
	draw_grid(Color.WEB_GRAY)

func draw_grid(col):
	for tile in hex_grid.get_used_cells():
		var w = 508/2
		var h = 442/2
		var e = 1
		var e2 = e * sqrt(3)/2
		var hex :Array = [[w+e/2,-e2,w/2-e/2,h+e2],[w/2+e,h,-w/2-e,h],[-w/2+e/2,h+e2,-w-e/2,-e2],[-w-e/2,+e2,-w/2+e/2,-h-e2],[-w/2-e,-h,w/2+e,-h],[w/2-e/2,-h-e2,w+e/2,e2]]
		var ls:Vector2
		var le:Vector2
		for l in hex:
			ls = hex_grid.to_global(hex_grid.map_to_local(tile)) + Vector2(l[0],l[1])
			le = hex_grid.to_global(hex_grid.map_to_local(tile)) + Vector2(l[2],l[3])
			self.draw_line(ls,le,col,10.0,false)
