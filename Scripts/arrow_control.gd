extends Node2D
@onready var characters: Node2D = $"../Characters"
@onready var hex_grid: TileMapLayer = $".."
@onready var main: Node2D = $"../.."


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	queue_redraw()


func _draw():
	for child in characters.get_children():
		if child.queued_action!=[] and child.body.animation=="Idle" and (child.faction==0 or main.debug):
			if child.queued_action[0]=="Move":
				draw_arrow(to_local(child.global_position),hex_grid.map_to_local(child.queued_action[1]),Color.LIME_GREEN)
			if child.queued_action[0]=="Attack":
				for tile in child.queued_action[1]:
					draw_arrow(to_local(child.global_position),hex_grid.map_to_local(tile),Color.INDIAN_RED)
	for child in characters.get_children():
		if child.control.selected==true:
			for tile in child.attack.get_attack_tiles():
				for attack in child.attack.get_attacks():
					if tile in attack:
						draw_circle(hex_grid.map_to_local(tile),20,Color.RED)
						break


func draw_arrow(from,to,col):
	var new_to=to-50*(to-from).normalized()
	draw_line(from,new_to+5*(new_to-from).normalized(),col,20)
	var head = -(new_to-from).normalized()*100
	draw_line(new_to,new_to+head.rotated(0.6),col,20)
	draw_line(new_to,new_to+head.rotated(-0.6),col,20)
