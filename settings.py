
SCREEN_WIDTH = 240 # 16x32    
SCREEN_HEIGHT = 240 # 16x28
FPS = 60
TILESIZE = 16
DEBUGLINEWIDTH = 10
DEBUGLINECOLOR = (200, 30, 10)

# ui 
'''
BAR_HEIGHT = 10 
HEALTH_BAR_WIDTH = 100
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 20
'''
UI_FONT = 'graphics/font/joystix monospace.otf'
UI_FONT_SIZE = 12

# general colors

BG_COLOR = '#6dc286'
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#7ee4ff'
UI_BORDER_COLOR = '#4bb2cd'
TEXT_COLOR = '#fffde4'

# ui colors
HEALTH_COLOR = '#dd5929'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# weapons 
weapon_data = {
	'fireball': {'cooldown': 450, 'damage' : 3, 'projectile_speed' : 3, 'graphic':'graphics/player/weapons/fireball.png'},
    'blue_fireball': {'cooldown': 200, 'damage' : 1, 'projectile_speed' : 3, 'graphic':'graphics/player/weapons/blue_fireball.png'}
			  } 

# items
item_data = {
	'health potion': {'strength': 5, 'cooldown': 6, 'units' : 1, 'graphic':'graphics/player/items/health_potion.png'},
    'slime': {'strength': 2, 'cooldown': 6, 'units' : 2, 'graphic':'graphics/player/items/slime.png'}
			} 

# enemy
enemy_data = {
    'skele' : {'health' : 8, 'exp' : 2, 'damage' : 0.5, 'attack_type' : 'contact', 'attack_sound' : None, 'speed' : 2, 'resistance' : 5, 'attack_radius' : 60, 'notice_radius': 100, 'action_type' : 'melee'},
    'goblin' : {'health' :6, 'exp' : 10, 'damage' : 5, 'attack_type' : 'contact', 'attack_sound' : None, 'speed' : 1.5, 'resistance' : 10, 'attack_radius' : 60, 'notice_radius': 100, 'action_type' : 'zone'},
    'knight' : {'health' :10, 'exp' : 5, 'damage' : 1, 'attack_type' : 'contact', 'attack_sound' : None, 'speed' : 1, 'resistance' : 5, 'attack_radius' : 60, 'notice_radius': 60, 'action_type' : 'turret'}
    	}