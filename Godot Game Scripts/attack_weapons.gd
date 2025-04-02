extends Node2D
@onready var hex_grid: TileMapLayer = $".."
@onready var characters: Node2D = $"../Characters"

var speed = 1000

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	
	for child in get_children():
		var target = hex_grid.map_to_local(child.get_meta("target"))
		if child.position != target:
			if get_tree().paused == false:
				child.rotation= (child.position - target).angle() -PI/2
				child.position = child.position.move_toward(target, delta*speed)
				
		else:
			var character = child.get_meta("character")
			if character!=characters:
				character.health-=1
				character.update_health()
			child.queue_free()

func attack(character, tile, origin, sprite) -> void:
	
	var weapon_scene = load("res://Scenes/attack_weapon.tscn")
	var weapon = weapon_scene.instantiate()
	add_child(weapon)
	
	weapon.scale = Vector2(8,8)
	weapon.position=hex_grid.map_to_local(origin)
	weapon.frame=sprite
	weapon.set_meta("target",tile)
	if character==null:
		weapon.set_meta("character",characters)
	else:
		weapon.set_meta("character",character)
	
