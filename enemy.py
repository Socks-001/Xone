import pygame
from enemy_data import enemy_data
from entity import Entity
from debug import debug


class Enemy(Entity):
	def __init__(self, name, pos, groups, player):
		# general setup
		super().__init__(self, pos, groups, player)
		self.sprite_type = 'enemy'
		self.obstacle_sprites = config
		self.visible_sprites = groups[0]
		self.shot_direction = None
		self.player = player
		
		
		# graphics
		self.import_graphics(name)
		self.status = 'idle' # initializing default state
		self.image = self.animations[self.status][int(self.frame_index)]
		self.collision_tolerance = 5

		# Initializing Rect and Hitbox 
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = pygame.FRect(self.rect.inflate(-6,-6))
		
		self.gravity = 0

		# stats
		self.health = enemy_data[name]['health'] 
		self.exp = enemy_data[name]['exp'] 
		self.damage = enemy_data[name]['damage'] 
		self.attack_type = enemy_data[name]['attack_type'] 
		self.attack_sound = enemy_data[name]['attack_sound'] 
		self.speed = enemy_data[name]['speed']
		self.resistance = enemy_data[name]['resistance'] 
		self.attack_radius = enemy_data[name]['attack_radius'] 
		self.notice_radius = enemy_data[name]['notice_radius']
		self.action_type = enemy_data[name]['action_type']
		
		

		# player interaction
		self.can_attack = False
		self.attack_time = pygame.time.get_ticks()
		self.attack_cooldown = None
		self.attack_cooldown = 2000
		self.hit_time = None
		self.vulnerable = True
		self.invincibility_duration = 100
		self.attack = at

	def get_target_distance_direction(self, object):
		object_vec = pygame.math.Vector2 (object.center)
		enemy_vec = pygame.math.Vector2 (self.rect.center)

		distance = (object_vec - enemy_vec).magnitude()

		if distance > 0.8:
			direction = (object_vec - enemy_vec).normalize()
		else:
			direction = pygame.math.Vector2()

		return (distance, direction)

	def get_status(self, player):
		enemy_type = 
		distance = self.get_player_distance_direction(player)[0]
		if distance <= self.attack_radius and self.can_attack:
			if self.status != 'attack':
				self.status = 'attack'

		elif distance <= self.notice_radius:
			self.status = 'move'

		else:
			self.status = self.status

	def actions(self,player):
	
		if self.action_type == 'melee':
			
			if self.status == 'attack':
				self.attack_time = pygame.time.get_ticks()
					# print ("attack")
			elif self.status == 'move':
				self.direction = self.get_player_distance_direction(player)[1]
				#print ('move')

			else:
				self.direction = pygame.math.Vector2(-1,0)
