extends Camera2D

var velocity
var panning: bool = false
var held_position


var max_panx = 3850
var max_pany = 600
var max_zoom
var zoom_speed = 0.95

func _ready() -> void:
	velocity = Vector2 (0,0)
	position = Vector2 (0,600 - 2*get_viewport_rect().size.y)
	max_zoom = max(0.5*get_viewport_rect().size.x/max_panx,0.2)
	zoom = Vector2 (0.4,0.4)
	get_tree().get_root().size_changed.connect(resize)

func _input(event): 
	var speed = 700/zoom.x
	var mouse_pos = get_global_mouse_position()
	if event.is_action_pressed("MoveCamUp"):		
		velocity.y -= speed
	if event.is_action_pressed("MoveCamDown"):
		velocity.y += speed
	if event.is_action_pressed("MoveCamLeft"):
		velocity.x -= speed
	if event.is_action_pressed("MoveCamRight"):
		velocity.x += speed
	if event.is_action_released("MoveCamUp"):		
		velocity.y += speed
	if event.is_action_released("MoveCamDown"):
		velocity.y -= speed
	if event.is_action_released("MoveCamLeft"):
		velocity.x += speed
	if event.is_action_released("MoveCamRight"):
		velocity.x -= speed
	if event.is_action_pressed("ZoomCamOut"):
		if zoom.x*zoom_speed<max_zoom:
			velocity.x /= max_zoom/zoom.x
			velocity.y /= max_zoom/zoom.x
			zoom = Vector2 (max_zoom,max_zoom)
		else:
			zoom *= zoom_speed
			velocity.x /= zoom_speed
			velocity.y /= zoom_speed
		if position.x + 0.5*get_viewport_rect().size.x/zoom.x > max_panx:
			position.x = max_panx - 0.5*get_viewport_rect().size.x/zoom.x
		elif position.x - 0.5*get_viewport_rect().size.x/zoom.x < -max_panx:
			position.x = -max_panx + 0.5*get_viewport_rect().size.x/zoom.x
		else:
			position.x += mouse_pos.x - get_global_mouse_position().x
		
		if position.y + 0.5*get_viewport_rect().size.y/zoom.y > max_pany:
			position.y = max_pany - 0.5*get_viewport_rect().size.y/zoom.y
		else:
			position.y += mouse_pos.y - get_global_mouse_position().y
			
	if event.is_action_pressed("ZoomCamIn") and zoom.x<1:
		zoom /= zoom_speed
		velocity.x *= zoom_speed
		velocity.y *= zoom_speed
		position += mouse_pos - get_global_mouse_position()
	
	if event is InputEventMouseButton and event.is_pressed():
		if event.button_index == MOUSE_BUTTON_RIGHT:
			panning = true
			held_position = get_viewport().get_mouse_position()
	if event is InputEventMouseButton and event.is_released():
		if event.button_index == MOUSE_BUTTON_RIGHT:
			panning = false


func resize():
	max_zoom = max(0.5*get_viewport_rect().size.x/max_panx,0.2)
	if zoom.x<max_zoom:
		zoom = Vector2 (max_zoom,max_zoom)
		position.x = 0
	if position.x + 0.5*get_viewport_rect().size.x/zoom.x > max_panx:
		position.x = max_panx - 0.5*get_viewport_rect().size.x/zoom.x
	if position.x - 0.5*get_viewport_rect().size.x/zoom.x < -max_panx:
		position.x = -max_panx + 0.5*get_viewport_rect().size.x/zoom.x
	
	if position.y + 0.5*get_viewport_rect().size.y/zoom.y > max_pany:
		position.y = max_pany - 0.5*get_viewport_rect().size.y/zoom.y



func _physics_process(delta):
	#var hex_grid: TileMapLayer = $"../HexGrid"
	#var characters: Node2D = $"../HexGrid/Characters"
	#position.y=characters.get_children()[0].position.y
	
	if not panning:
		position.x = clamp(position.x + velocity.x * delta, -max_panx + 0.5*get_viewport_rect().size.x/zoom.x, max_panx - 0.5*get_viewport_rect().size.x/zoom.x)
		position.y = min(position.y + velocity.y * delta,  max_pany - 0.5*get_viewport_rect().size.y/zoom.y)
	else:
		var mouse_pos = get_viewport().get_mouse_position()
		position.x = clamp(position.x - (mouse_pos.x - held_position.x)/zoom.x, -max_panx + 0.5*get_viewport_rect().size.x/zoom.x, max_panx - 0.5*get_viewport_rect().size.x/zoom.x)
		position.y = min(position.y - (mouse_pos.y - held_position.y)/zoom.y, max_pany - 0.5*get_viewport_rect().size.y/zoom.y)
		held_position = mouse_pos
	
