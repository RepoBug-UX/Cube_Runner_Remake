# -*- coding: utf-8 -*-
"""
Team Name:

Team Members:
    

Game Name:
    
"""
import random
import pygame
import math


#player class

class player_main():
    def __init__(self):
        self.siz = 40
        self.col = (220, 220, 220)  # Lighter grey color
        self.border_col = (255, 255, 255)  # White border
        self.speed = 10
        self.hp = 1
        self.pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 100)  # Position player near bottom of screen
        self.z_pos = 0  # Player is at z=0 (foreground)
        
        
#enemy class
        
class enemy():
    def __init__(self, x,y, direc):
        # Start position from a vanishing point
        self.pos = pygame.Vector2(x,y)
        self.col = (255, 0, 0)    # Bright red color for squares
        self.outline_col = (80, 80, 80)  # Grey color for outline
        self.siz = 40       # Base size of square
        self.z_pos = 3000   # Start far in the distance
        self.z_speed = 25   # Forward speed (appears as if player is moving forward)
        
        # No random x movement - squares should be stationary
        self.x_speed = 0
        
        # Perspective projection parameters
        self.focal_length = 500
        self.vanishing_point_y = screen.get_height() / 3  # Place vanishing point at 1/3 from top
        
    def move(self):
        self.z_pos -= self.z_speed   # Move towards viewer
        
    def project_to_screen(self, screen_width, screen_height):
        # Always project, even if z_pos is negative
        # Calculate perspective scale - use absolute value to prevent reversal
        scale = self.focal_length / (self.z_pos + self.focal_length)
        
        # Project coordinates with vanishing point perspective
        screen_x = screen_width/2 + (self.pos.x - screen_width/2) * scale
        
        # Calculate y position relative to vanishing point
        screen_y = self.vanishing_point_y + (self.pos.y - self.vanishing_point_y) * scale
        
        # Calculate visual size with more dramatic scaling
        visual_size = self.siz * scale * 2  # Doubled for more visible size
        
        return (screen_x, screen_y, visual_size)
            
    def draw(self, screen):
        projection = self.project_to_screen(screen.get_width(), screen.get_height())
        if projection:
            screen_x, screen_y, visual_size = projection
            # Draw the filled red square
            pygame.draw.rect(screen, self.col, pygame.Rect(screen_x-visual_size/2, screen_y-visual_size/2, visual_size, visual_size))
            # Draw grey outline
            pygame.draw.rect(screen, self.outline_col, pygame.Rect(screen_x-visual_size/2, screen_y-visual_size/2, visual_size, visual_size), 2)
        
    def collision_with_player(self, player_x, player_y, player_size):
        projection = self.project_to_screen(screen.get_width(), screen.get_height())
        if projection:
            screen_x, screen_y, visual_size = projection
            # Get the bottom y-coordinate of both the player and enemy
            player_bottom = player_y + player_size/2
            enemy_bottom = screen_y + visual_size/2
            
            # Check if the bottom lines overlap horizontally
            if (abs(player_bottom - enemy_bottom) < 5 and  # Small threshold for vertical alignment
                player_x + player_size/2 > screen_x - visual_size/2 and  # Player right edge > enemy left edge
                player_x - player_size/2 < screen_x + visual_size/2):    # Player left edge < enemy right edge
                return True
        return False
        
    def is_off_screen(self, screen_width, screen_height):
        projection = self.project_to_screen(screen_width, screen_height)
        if projection:
            screen_x, screen_y, visual_size = projection
            # Check if the enemy is completely outside the visible screen area
            return (screen_x + visual_size/2 < 0 or  # Completely off left edge
                    screen_x - visual_size/2 > 1280 or  # Completely off right edge
                    screen_y + visual_size/2 < 0 or  # Completely off top edge
                    screen_y - visual_size/2 > 720)  # Completely off bottom edge
        return True  # If projection fails, consider it off screen

    
    
#Enemy Spawner
"""
Spawns the red enemy blocks

"""
class enemy_spawner():
    def __init__(self, x,y, directi, wait, screen_height, screen_width):
        self.screen_h = screen_height
        self.screen_w = screen_width                 
        self.wait_spawn = wait      # Time between spawns
        self.siz = 40              # Size of cubes
        self.self_time = 0         # Spawn timer
        self.pattern_offset = 0    # Used to create patterns
        
    def update(self, enemy_array):
        self.self_time += 1
        if self.self_time > self.wait_spawn:
            # Create a pattern of 9-12 cubes (3 times the original 3-4)
            num_cubes = random.randint(9, 12)
            base_x = self.screen_w/2 + math.sin(self.pattern_offset) * 200  # Sine wave pattern
            
            for i in range(num_cubes):
                # Calculate x position for each cube in pattern
                x_pos = base_x + random.randint(-300, 300)
                # Keep within screen bounds
                x_pos = max(self.siz, min(self.screen_w - self.siz, x_pos))
                
                # Check if new enemy would overlap with existing enemies
                new_enemy = enemy(x_pos, self.screen_h/2, None)
                can_spawn = True
                
                for existing_enemy in enemy_array:
                    if abs(existing_enemy.pos.x - new_enemy.pos.x) < self.siz * 2:  # Check horizontal overlap
                        can_spawn = False
                        break
                
                if can_spawn:
                    enemy_array.append(new_enemy)
            
            self.pattern_offset += 0.5  # Increment pattern offset
            self.self_time = 0

            
        
        
    
    
#player health
player_health = 0
    
def enemy_updates(curr_time, screen, enemy_arr, spawner_arr, player_x, player_y, player_size):
    global collision_count, player_health
    i = 0
    while i < len(enemy_arr):    #loop through enemy array
        enemy_arr[i].move()      #make each enemy move from the array
        enemy_arr[i].draw(screen)    #draws the enemy 
        
        # Check for collision first
        if enemy_arr[i].collision_with_player(player_x, player_y, player_size):
            player_health -= 1
            collision_count += 1  # Increment collision counter
            print(f"Collision detected! Total collisions: {collision_count}")  # Debug print
            enemy_arr.pop(i)    #remove enemy on collision
            continue
            
        # Then check if enemy is off screen
        if enemy_arr[i].is_off_screen(screen.get_width(), screen.get_height()):
            enemy_arr.pop(i)    #remove enemy if off screen
            continue
            
        i += 1  # Only increment if we didn't remove an enemy
        
    for i in range(len(spawner_arr)):
        spawner_arr[i].update(enemy_arr)        #Updates Spawners

        
        
    
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Visibility toggles
SHOW_ENEMY_COUNT = False  # Set to False to hide enemy count
SHOW_COLLISION_COUNT = False  # Set to False to hide collision count

# Camera settings
camera_distance = 500  # Distance from player to camera
camera_height = 300    # Height of camera above ground

curr_time = 0 #counter for spawner
score = 0       #your score
score_font = pygame.font.Font(None, 50)
last_score_update = 0  # Track when we last updated the score
collision_count = 0    # Track number of z-plane collisions

enemy_array = []        #array for enemies
spawner_array = []      #array for spawners

# Game Screen Name text
pygame.display.set_caption('Third-Person Perspective Game')

# Set up font and size
font = pygame.font.SysFont(None, 100)  # Default font, size 100
subfont = pygame.font.SysFont(None, 50)  # Smaller font for subtext
# Set up text object for The End screen
text = font.render('The End', True, (255, 255, 255))  # White color for the text
# Get the rectangle of the text to center it
text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))

#Set spawners (only need one spawner for center of screen)
spawner_array.append(enemy_spawner(
    screen.get_width()/2,    # x position
    screen.get_height()/2,   # y position
    None,                    # direction (not used)
    45,                      # Spawn frequency (increased from 30 to 45)
    screen.get_height(), 
    screen.get_width()
))

#Creates player object
player = player_main()
player_health = 1  # Set initial health to 1

screentype = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if screentype == 0:
        # Draw gradient backgrounds
        
        # Sky gradient (black to royal blue)
        sky_height = int(screen.get_height()/3)
        sky_steps = 20  # Number of gradient steps
        for i in range(sky_steps):
            progress = i / sky_steps
            # Interpolate from black (0,0,0) to royal blue (65,105,225)
            color = (
                int(65 * progress),
                int(105 * progress),
                int(225 * progress)
            )
            rect_height = sky_height // sky_steps
            rect_y = i * rect_height
            pygame.draw.rect(screen, color, pygame.Rect(0, rect_y, screen.get_width(), rect_height + 1))
            
        # Ground gradient (forest green to lighter green)
        ground_height = int(screen.get_height() * 2/3)
        ground_steps = 20  # Number of gradient steps
        for i in range(ground_steps):
            progress = i / ground_steps
            # Interpolate from forest green (34,139,34) to lighter green (144,238,144)
            color = (
                int(34 + (144 - 34) * progress),
                int(139 + (238 - 139) * progress),
                int(34 + (144 - 34) * progress)
            )
            rect_height = ground_height // ground_steps
            rect_y = sky_height + (i * rect_height)
            pygame.draw.rect(screen, color, pygame.Rect(0, rect_y, screen.get_width(), rect_height + 1))
        
        curr_time += 0.01 #increase time
        
        #Draw player on screen (fixed position near bottom)
        pygame.draw.rect(screen, player.col, pygame.Rect(player.pos.x-player.siz/2, player.pos.y-player.siz/2, player.siz, player.siz))
        pygame.draw.rect(screen, player.border_col, pygame.Rect(player.pos.x-player.siz/2, player.pos.y-player.siz/2, player.siz, player.siz), 2)
        
        #Move around keys (left and right)
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.pos.x > player.siz/2:
            player.pos.x -= 300 * dt
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.pos.x < screen.get_width() - player.siz/2:
            player.pos.x += 300 * dt
        
        #Calls the enemy updates method
        enemy_updates(curr_time, screen, enemy_array, spawner_array, player.pos.x, player.pos.y, player.siz)
        
        # Update score every 1.5 seconds
        current_time = pygame.time.get_ticks() / 1000  # Convert to seconds
        if current_time - last_score_update >= 1.5:  # If 1.5 seconds have passed
            score += 1
            last_score_update = current_time
  
        # Draw score, enemy count, and collision count
        score_text = score_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Only show enemy count if enabled
        if SHOW_ENEMY_COUNT:
            enemy_count_text = score_font.render(f'Enemies: {len(enemy_array)}', True, (255, 255, 255))
            screen.blit(enemy_count_text, (10, 60))
            
        # Only show collision count if enabled
        if SHOW_COLLISION_COUNT:
            collision_count_text = score_font.render(f'Collisions: {collision_count}', True, (255, 255, 255))
            screen.blit(collision_count_text, (10, 110))
        
        #The You Die and Score
        if player_health <= 0:
            screentype = 1
            print("You Died.")
            print("Score: "+str(round(score)))
            print("Collisions: "+str(collision_count))
        
    #Death screen
    if screentype == 1:
        # Draw the same gradient backgrounds as the game
        # Sky gradient (black to royal blue)
        sky_height = int(screen.get_height()/3)
        sky_steps = 20  # Number of gradient steps
        for i in range(sky_steps):
            progress = i / sky_steps
            # Interpolate from black (0,0,0) to royal blue (65,105,225)
            color = (
                int(65 * progress),
                int(105 * progress),
                int(225 * progress)
            )
            rect_height = sky_height // sky_steps
            rect_y = i * rect_height
            pygame.draw.rect(screen, color, pygame.Rect(0, rect_y, screen.get_width(), rect_height + 1))
            
        # Ground gradient (forest green to lighter green)
        ground_height = int(screen.get_height() * 2/3)
        ground_steps = 20  # Number of gradient steps
        for i in range(ground_steps):
            progress = i / ground_steps
            # Interpolate from forest green (34,139,34) to lighter green (144,238,144)
            color = (
                int(34 + (144 - 34) * progress),
                int(139 + (238 - 139) * progress),
                int(34 + (144 - 34) * progress)
            )
            rect_height = ground_height // ground_steps
            rect_y = sky_height + (i * rect_height)
            pygame.draw.rect(screen, color, pygame.Rect(0, rect_y, screen.get_width(), rect_height + 1))
            
        # Draw the end game text
        screen.blit(text, text_rect)
        
        # Draw the score subtext
        score_text = subfont.render(f'Final Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 50))
        screen.blit(score_text, score_rect)
        
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    


pygame.quit()
