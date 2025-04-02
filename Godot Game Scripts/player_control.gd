extends Node2D



@onready var character = $".."
@onready var characters = $"../.."
@onready var hex_grid = $"../../.."
@onready var main = $"../../../.."

var controlled = true
var selected = false
var dragging = false
var dragging_offset: Vector2

var attacking: Array

func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	pass


func _input(event: InputEvent) -> void:
		
	
	
	
	if character.initiative!=0:
		return
	if main.waiting_for_animations():
		return
	
	if event.is_action_pressed("Skip"):
		if selected:
			attacking = []
			selected = false
			main.next_turn()
			main.update_fow()
	if event is not InputEventMouseButton:
		return
	var global_clicked = get_global_mouse_position()
	var pos_clicked = hex_grid.local_to_map(hex_grid.to_local(global_clicked))
	
	if event.button_index == MOUSE_BUTTON_LEFT and event.is_pressed():
		if selected:
			selected = false
			main.update_fow()
		attacking = []
		if pos_clicked == character.hex_position and character.body.animation == "Idle":
			dragging = true
			dragging_offset = global_clicked - character.global_position
		
	if event.button_index == MOUSE_BUTTON_LEFT and event.is_released() and dragging:
		character.position = hex_grid.map_to_local(character.hex_position)
		
		
		if pos_clicked == character.hex_position:
			selected = true
			dragging = false
		else:
			dragging = false
			if character.movement.is_valid(pos_clicked):
				character.queued_action=["Move",pos_clicked]
				main.next_turn()
		main.update_fow()
			
	if event.button_index == MOUSE_BUTTON_RIGHT and selected and event.is_pressed():
		var found = false
		for i in range(len(attacking)):
			if attacking[i] == pos_clicked:
				attacking.remove_at(i)
				found = true
				break
		if not found and pos_clicked!=character.hex_position:
			if pos_clicked in character.attack.get_attack_tiles():
				attacking.append(pos_clicked)

		if character.attack.is_valid(attacking):
			character.queued_action=["Attack",attacking]
			attacking = []
			selected = false
			main.next_turn()
			main.update_fow()
		
	
	
	queue_redraw()
