extends Node2D


var hex_position: Vector2i
var target_position: Vector2

var health: int
var max_health: int

var initiative: int

var weapon: int

var faction: int

var queued_action = []

var cooldown: bool = false

@onready var main: Node2D = $"../../.."
@onready var hex_grid: TileMapLayer = $"../.."
@onready var characters: Node2D = $".."
@onready var movement: Node2D = $Movement
@onready var control: Node2D = $Control
@onready var attack: Node2D = $Attack
@onready var body: Node2D = $Body
@onready var hearts: Node2D = $Hearts

var shaking: bool = false
var shaketime: int = 0

func _ready() -> void:
	
	position = hex_grid.map_to_local(hex_position)
	target_position = position
	health = max_health
	

func _physics_process(delta):
	
	if shaking:
		var time = Time.get_unix_time_from_system() -shaketime
		if time>1.5:
			shaking = false
			position = target_position
		else:
			position.x = target_position.x + 20*sin(time*PI*(16/3))

	elif control.dragging:
		global_position = get_global_mouse_position() - control.dragging_offset
	if body.animation=="Death":
		for limb in get_children():
			if limb.name not in ["Movement","Control","Attack","Body","Hearts","body"]:
				var limb_velocity = limb.get_meta("Velocity")
				limb.rotation+=abs(limb.position.y-27)*limb.position.x/8000
				limb.position.y+=limb_velocity
				if limb.position.y>27:
					limb_velocity=abs(limb_velocity)*-1
					limb_velocity*=0.6
				else:
					limb_velocity+=0.1
				limb.set_meta("Velocity",limb_velocity)
	elif target_position!=position and not shaking:
		body.animation = "Run"
		if position.x > target_position.x or (position.x==target_position.x and scale.x == -8):
			scale.x = -8
			hearts.scale.x=-1
		else:
			scale.x = 8
			hearts.scale.x=1
		if control.dragging:
			scale.x *= -1
			hearts.scale.x *= -1
		
		var speed
		if visible:
			speed = 400
		else:
			speed = 10000
		position = position.move_toward(target_position, delta*speed)
	else:
		body.animation = "Idle"
	
	queue_redraw()



func distance_to_enemy(tile)-> int:
	var distance=10
	for other_character in characters.get_children():
		if other_character.faction != faction:
			distance = min(distance,hex_grid.travel_distance(tile,other_character.hex_position))
	return distance


func update_health():
	hearts.frame = health
	if health == 0:
		queued_action=[]
		for limb in get_children():
			if limb.name not in ["Movement","Control","Attack","Body","Hearts"]:
				limb.set_meta("Velocity",-2.0*randf())
		body.animation="Death"
		
		await get_tree().create_timer(1.7).timeout
		if faction==1:
			main.kills+=1
			main.kills_label.text = "Kills:   "+str(main.kills)
		main.remove_character(self)


func _draw(): 
	if control==null:
		return
	if not control.controlled:
		return
	if control.selected and not control.dragging:
		var mouse_pos = get_global_mouse_position()
		var mouse_tile = hex_grid.local_to_map(hex_grid.to_local(mouse_pos))
		draw_outline(hex_grid.to_global(hex_grid.map_to_local(mouse_tile))-global_position,Color.RED)
	if control.selected or control.dragging:
		draw_outline(Vector2(0,0),Color.GREEN)
	for tile in control.attacking:
		draw_outline(hex_grid.to_global(hex_grid.map_to_local(tile))-global_position,Color.RED)


func draw_outline(pos,col):
	var w = 508/16 - 0.5
	var h = 442/16 - 0.5
	var e = 0.5
	var e2 = e * sqrt(3)/2
	var hex :Array = [[w+e/2,-e2,w/2-e/2,h+e2],[w/2+e,h,-w/2-e,h],[-w/2+e/2,h+e2,-w-e/2,-e2],[-w-e/2,+e2,-w/2+e/2,-h-e2],[-w/2-e,-h,w/2+e,-h],[w/2-e/2,-h-e2,w+e/2,e2]]
	var ls:Vector2
	var le:Vector2
	for l in hex:
		ls = Vector2(l[0],l[1]) + pos/Vector2(scale.x,scale.y)
		le = Vector2(l[2],l[3]) + pos/Vector2(scale.x,scale.y)
		self.draw_line(ls,le,col,2.0,false)
