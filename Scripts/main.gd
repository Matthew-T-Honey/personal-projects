extends Node2D

var height = 0
var kills = 0

@onready var characters: Node2D = $HexGrid/Characters
@onready var tile_generator: Node2D = $"HexGrid/Tile Generator"
@onready var fow_control: Node2D = $"HexGrid/FOW Control"
@onready var grid_outline: Node2D = $"HexGrid/Grid Outline"
@onready var height_label: Label = $"CanvasLayer/Height Label"
@onready var initiative_label: Label = $"CanvasLayer/Initiative Label"
@onready var attack_weapons: Node2D = $"HexGrid/Attack Weapons"
@onready var spawner: Node2D = $HexGrid/Spawner
@onready var hex_grid: TileMapLayer = $HexGrid
@onready var kills_label: Label = $"CanvasLayer/Kills Label"
@onready var camera: Camera2D = $Camera

@export var debug = false



# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	update_grid()


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	var textlines=[]
	textlines.resize(len(characters.get_children()))
	var offset = characters.get_children()[0].initiative
	for character in characters.get_children():
		if character.visible:
			if character.initiative==0:
				textlines[(character.initiative-offset) % len(textlines)]="> "+character.name.split(" ")[0]+": "+str(character.initiative)
			else:
				textlines[(character.initiative-offset) % len(textlines)]=character.name.split(" ")[0]+": "+str(character.initiative)
	
	for i in range(len(textlines)-1,-1,-1):
		if textlines[i]==null:
			textlines.remove_at(i)
	
	initiative_label.text="\n".join(textlines)
	
func waiting_for_animations() -> bool:
	var waiting=false
	for character in characters.get_children():
		if (character.body.animation!="Idle" and character.control.dragging!=true) or character.shaking:
			waiting = true
	
	if len(attack_weapons.get_children())>0:
		waiting = true
	return waiting

func update_grid() -> void:
	fow_control.update_fow()
	for character in characters.get_children():
		if character.faction==0:
			while -character.hex_position.y > height+2:
				tile_generator.generate_row(height+25)
				height +=1
				
				spawner.spawn_enemy(height)
	grid_outline.queue_redraw()
	height_label.text = "Distance:" + str(height)

func update_fow() -> void:
	fow_control.update_fow()


func remove_character(character) -> void:
	var char_init=character.initiative
	character.queue_free()
	await character.tree_exited
	for child in characters.get_children():
		if child.initiative>char_init:
			child.initiative-=1
	if char_init==0:
		next_turn()

func next_turn() -> void:
	for child in characters.get_children():
		child.initiative-=1
		if child.initiative==-1:
			child.initiative=len(characters.get_children())-1
	var next = false
	for child in characters.get_children():
		if child.initiative==0:
			child.cooldown = false
			if child.queued_action!=[]:
				if child.body.animation=="Death":
					pass
				elif child.queued_action[0]=="Move":
					child.movement.execute_move(child.queued_action[1])
				elif child.queued_action[0]=="Attack":
					child.attack.execute_attack(child.queued_action[1])
					child.cooldown = true
			if child.control.controlled:
				child.queued_action=[]
				#child.queued_action=["Move",child.hex_position+Vector2i(0,-1)]
				#next=true
			else:
				while waiting_for_animations():
					await get_tree().create_timer(0.1).timeout
				if child.distance_to_enemy(child.hex_position)==10 and false:
					child.queue_free()
					await child.tree_exited
				else:
					child.queued_action=child.control.get_best_move()
				next=true
			break

	update_grid()
	if next:
		next_turn()


func _on_reset_button_pressed() -> void:
	get_tree().reload_current_scene()
