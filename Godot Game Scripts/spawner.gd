extends Node2D
@onready var characters: Node2D = $"../Characters"
@onready var hex_grid: TileMapLayer = $".."
@onready var main: Node2D = $"../.."


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	hex_grid.spawn_locations.shuffle()
	spawn("knight","player_control",0,"basic_movement","reach_attack",0,hex_grid.spawn_locations[0],3)
	spawn("rogue","player_control",0,"basic_movement","slash_attack",1,hex_grid.spawn_locations[1],3)
	spawn("wizard","player_control",0,"basic_movement","ranged_attack",4,hex_grid.spawn_locations[2],3)


func spawn_enemy(height) -> void:
	var x_values=[]
	for i in range(-8,9):
		x_values.append(i)
	x_values.shuffle()
	for x in x_values:
		var tile=Vector2i(x,-9-height)
		if hex_grid.get_location(tile)==null and hex_grid.get_cell_source_id(tile) not in [1,3]:
			
			var health = clamp(roundf((randf_range(0,20) + height)/20),1.0,3.0)
			
			if (randf_range(0,50) + height)/50 > 1.0:
				var r = randi_range(1,3)
				if r==1:
					spawn("scout","ai_control",1,"basic_movement","slash_attack",3,Vector2i(x,-9-height),int(health))
				elif r==2:
					spawn("warrior","ai_control",1,"basic_movement","reach_attack",2,Vector2i(x,-9-height),int(health))
				else:
					spawn("shaman","ai_control",1,"basic_movement","ranged_attack",4,Vector2i(x,-9-height),int(health))
			else:
				spawn("grunt","ai_control",1,"basic_movement","simple_attack",1,Vector2i(x,-9-height),int(health))
			break
	


func spawn(sprite,control,faction,movement,attack,weapon,pos,health) -> void:

	var max_init = len(characters.get_children())

	var base_scene = load("res://Scenes/Sprites/"+sprite+".tscn")
	var base = base_scene.instantiate()
	base.set_name(base.name+" "+str(randi_range(1000,9999)))
	
	var control_scene = load("res://Scenes/"+control+".tscn")
	var control_node = control_scene.instantiate()
	control_node.set_name("Control")
	base.add_child(control_node)
	
	var movement_scene = load("res://Scenes/"+movement+".tscn")
	var movement_node = movement_scene.instantiate()
	movement_node.set_name("Movement")
	base.add_child(movement_node)
	
	var attack_scene = load("res://Scenes/"+attack+".tscn")
	var attack_node = attack_scene.instantiate()
	attack_node.set_name("Attack")
	base.add_child(attack_node)
	
	base.set_script(load("res://Scripts/character.gd"))
	
	base.hex_position = pos
	
	base.weapon=weapon
	base.faction=faction
	
	var hearts_scene = load("res://Scenes/hearts.tscn")
	var hearts = hearts_scene.instantiate()
	hearts.set_name("Hearts")
	base.add_child(hearts)
	hearts.animation = "Hearts "+str(health)
	hearts.frame = health
	base.max_health = health
	
	base.scale = Vector2(8,8)
	if control=="player_control":
		base.initiative = randi_range(0, max_init)
	else:
		base.initiative = randi_range(1, max_init)
	
	if faction!=0 and not main.debug:
		base.visible=false
	
	characters.add_child(base)
	
	for child in characters.get_children():
		if child.initiative>=base.initiative and child!=base:
			child.initiative+=1
	
	
