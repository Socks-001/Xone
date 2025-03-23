# Game Data
WEAPON_DATA = {
	'fireball': {'cooldown': 450, 'damage' : 3, 'projectile_speed' : 3, 'graphic':'graphics/player/weapons/fireball.png'},
    'blue_fireball': {'cooldown': 200, 'damage' : 1, 'projectile_speed' : 3, 'graphic':'graphics/player/weapons/blue_fireball.png'}
			  } 

# items
ITEM_DATA = {
	'health potion': {'strength': 5, 'cooldown': 6, 'units' : 1, 'graphic':'graphics/player/items/health_potion.png'},
    'slime': {'strength': 2, 'cooldown': 6, 'units' : 2, 'graphic':'graphics/player/items/slime.png'}
			} 

# enemy
ENEMY_DATA = {
    'skele' : {'health' : 8, 'exp' : 2, 'damage' : 0.5, 'attack_type' : 'contact', 'attack_sound' : None, 'speed' : 2, 'resistance' : 5, 'attack_radius' : 60, 'notice_radius': 100, 'action_type' : 'melee'},
    'goblin' : {'health' :6, 'exp' : 10, 'damage' : 5, 'attack_type' : 'contact', 'attack_sound' : None, 'speed' : 1.5, 'resistance' : 10, 'attack_radius' : 60, 'notice_radius': 100, 'action_type' : 'zone'},
    'knight' : {'health' :10, 'exp' : 5, 'damage' : 1, 'attack_type' : 'contact', 'attack_sound' : None, 'speed' : 1, 'resistance' : 5, 'attack_radius' : 60, 'notice_radius': 60, 'action_type' : 'turret'}
    	}