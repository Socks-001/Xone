import pygame
from settings import config
from utilities import search_dict

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type):
        super().__init__(groups)
        self.sprite_type = sprite_type
        tile_size = search_dict(config, 'TILESIZE') 
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.FRect(self.rect.inflate((self.rect.x*0.90), (self.rect.y*0.90)))
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = config['lvl']['obstacle_sprites']
        self.collision_tolerance = 10
    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        #self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        #self.collision('vertical')
        self.rect.center = self.hitbox.center
        
    def death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,self.weapon_sprites)

    def create_attack(self):
          Weapon(self.player, [self.weapon_sprites],  self.obstacle_sprites, self.enemy_sprites)

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups, obstacle_sprites, entity_sprites):
        super().__init__(groups)	

        self.player = player

        # graphic
        self.sprite_type = 'player_shot'
        self.weapon_index = player.weapon_index
        self.attack_damage = player.attack_damage
        self.direction = pygame.Vector2(1,0)
        
        #self.weapon_datas

        full_path = f'graphics/player/weapons/{player.weapon}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        #Flip if shooting backwards
        '''if self.player.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)'''

        #self.velocity = float(weapon_data[player.weapon]['projectile_speed']) + float(player.direction.x * player.speed)	
        self.velocity = float(weapon_data[player.weapon]['projectile_speed'])

        # placement 
        self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,2))
        
        #self.rect = self.image.get_rect(center = player.rect.center)
        self.hitbox = pygame.FRect(self.rect.inflate(-1,0))
        self.direction = pygame.math.Vector2(1, self.player.direction.y)

        # obstacles
        self.obstacle_sprites = obstacle_sprites

        # enemies 
        self.entity_sprites = entity_sprites

    def move(self, velocity):
        if self.direction.x == 0:
            self.direction.x = 1
        
        if self.direction.x < 0:
            self.direction.x = -1
            
        if self.direction.x > 0:
            self.direction.x = 1


        self.hitbox.x += self.direction.x  * velocity
        self.rect.center = self.hitbox.center

    def check_collision(self):
        for entity in self.entity_sprites:
            if hasattr (entity, 'sprite_type') and entity.sprite_type == 'enemy':
                if self.hitbox.colliderect(entity.hitbox) and entity.vulnerable == True:
                    pygame.mixer.Sound(entity.hit_sound).play()
                    entity.health -= self.attack_damage
                    entity.vulnerable = False
                    entity.hit_time = pygame.time.get_ticks()
                    #not sure why it woorks this way (values are reversed) 
                    if self.hitbox.centerx < entity.hitbox.centerx:
                        entity.shot_direction = 'left'
                        #print (f'shot direction {entity.shot_direction}')
                        #print (f'b : {self.rect.centerx} e : {entity.hitbox.centerx}')
                    elif self.hitbox.centerx > entity.hitbox.centerx:
                        entity.shot_direction = 'right'
                        #print (f'shot direction {entity.shot_direction}')
                        #print (f'b : {self.hitbox.centerx} e : {entity.hitbox.centerx}')
                        
                    self.kill()

                elif self.rect.colliderect(entity.hitbox) and entity.vulnerable == False:
                    self.kill()

                else:
                    pass

        for sprite in self.obstacle_sprites:
            if self.hitbox.colliderect(sprite.rect) or self.hitbox.x > + SCREEN_WIDTH + 4 or self.hitbox.x <= 0:
                self.kill()

    def update(self):
        
        self.check_collision()
        self.move(self.velocity)

        #Treasure of the Rudras SNES Art
        #Shadownrun SNES