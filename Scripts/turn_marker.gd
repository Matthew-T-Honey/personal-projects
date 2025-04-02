extends Polygon2D
@onready var characters: Node2D = $"../HexGrid/Characters"


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	for child in characters.get_children():
		if child.initiative==0:
			visible=child.visible
			global_position=child.global_position
