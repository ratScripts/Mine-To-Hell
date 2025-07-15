import pygame
import random

pygame.init()

class Player():
    def __init__(self, W = 1000, H = 800):
        self.x, self.y = W // 2, -70
        self.speed = 5
        self.W, self.H = W, H
        self.vy = 0
        self.grounded = False
        self.camX = self.x - W // 2
        self.camY = self.y - H // 2
        self.camVX = 0
        self.camVY = 0
        self.flipped = False

        self.map_end_pos = 28*60 #28 Blocks, each 60 Pixels wide

        self.playerSprite = pygame.transform.scale(pygame.image.load("Player.png").convert_alpha(), (35, 50))
        self.playerMask = pygame.mask.from_surface(self.playerSprite)

        self.pick_name = "wooden_pick"
        self.mineDir = "right"
        self.pickX, self.pickY = self.x - 20 - self.camX, self.y + 12 - self.camY
        self.pick_sprite = pygame.transform.scale(pygame.image.load(f"{self.pick_name}.png").convert_alpha(), (28, 28))
        self.pick_mask = pygame.mask.from_surface(self.pick_sprite)
        

    def camera(self):
        
        targetX = self.x - self.W // 2
        targetY = self.y - self.H // 2
        self.camVX = (targetX - self.camX) * 0.1
        self.camVY = (targetY - self.camY) * 0.1
        self.camX += self.camVX
        self.camY += self.camVY
        if self.camX <= 0:
            self.camX = 0
        if self.camX >= self.map_end_pos - 1000:
            self.camX = self.map_end_pos - 1000


    def controller(self):
        if self.grounded == False:
            self.vy += 0.3


        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.mineDir = "left"
        if keys[pygame.K_RIGHT]:
            self.mineDir = "right"
        if keys[pygame.K_UP]:
            self.mineDir = "up"
        if keys[pygame.K_DOWN]:
            self.mineDir = "down"



        if keys[pygame.K_a]:
            if self.x - self.speed >= 0:
                self.x -= self.speed
            self.flipped = True
        if keys[pygame.K_d]:
            if self.x + self.speed + 35 <= self.map_end_pos:
                self.x += self.speed
            self.flipped = False

        if keys[pygame.K_SPACE] and self.grounded:
            self.vy = -6

        self.grounded = False 
    
        self.y += self.vy
        
    def draw(self, window):
        window.blit(self.playerSprite if not self.flipped else pygame.transform.flip(self.playerSprite, True, False), (self.x - self.camX, self.y - self.camY))
        if self.mineDir == "left":
            self.pickX, self.pickY = self.x - 20 - self.camX, self.y + 12 - self.camY
            window.blit(pygame.transform.flip(self.pick_sprite, True, False), (self.pickX, self.pickY))
        elif self.mineDir == "right":
            self.pickX, self.pickY = self.x + 30 - self.camX, self.y + 12 - self.camY
            window.blit(self.pick_sprite, (self.pickX, self.pickY))
        elif self.mineDir == "up":
            self.pickX, self.pickY = self.x + 10 - self.camX, self.y - 20 - self.camY
            window.blit(pygame.transform.flip(self.pick_sprite, True, False), (self.pickX, self.pickY))
        elif self.mineDir == "down":
            self.pickX, self.pickY = self.x - self.camX, self.y + 40 - self.camY
            window.blit(pygame.transform.flip(self.pick_sprite, False, True), (self.pickX, self.pickY))

    def update(self, window):
        self.controller()
        self.camera()
        self.draw(window)





class Tilemap():
    def __init__(self):
        self.grassBlock = pygame.image.load("GrassBlock.png").convert_alpha()
        self.dirtBlock = pygame.image.load("DirtBlock.png").convert_alpha()
        self.grassBlockMask = pygame.mask.from_surface(self.grassBlock)
        self.dirtBlockMask = pygame.mask.from_surface(self.dirtBlock)

        self.map = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    
        for v,i in enumerate(self.map):
            row = v % 28
            if i == 2 and row > 11:
                if random.randint(1,15) == 1:
                    self.map[v] = 3
    
    
    def collide(self, player, block_x, block_y):
        player_rect = pygame.Rect(player.x, player.y, 35, 50)
        block_rect = pygame.Rect(block_x, block_y, 60, 60)

        if player.vy > 0 and player_rect.bottom - player.vy <= block_rect.top:
            player.y = block_rect.top - 50
            player.vy = 0
            player.grounded = True
        elif player.vy < 0 and player_rect.top - player.vy >= block_rect.bottom:
            player.y = block_rect.bottom
            player.vy = 0
        elif player.x + 35 > block_rect.left and player.x < block_rect.left and player_rect.bottom > block_rect.top and player_rect.top < block_rect.bottom:
            player.x = block_rect.left - 35
        elif player.x < block_rect.right and player.x + 35 > block_rect.right and player_rect.bottom > block_rect.top and player_rect.top < block_rect.bottom:
            player.x = block_rect.right

    def draw(self, window, player):
        tile_size = 60
        tiles_per_row = 28

        start_col = max(0, int(player.camY // tile_size))
        end_col = int((player.camY + player.H) // tile_size) + 1

        start_row = max(0, int(player.camX // tile_size))
        end_row = int((player.camX + player.W) // tile_size) + 1

        for col in range(start_col, min(end_col, len(self.map) // tiles_per_row)):
            for row in range(start_row, min(end_row, tiles_per_row)):
                v = col * tiles_per_row + row
                i = self.map[v]

                if i != 0:
                    block_x = row * tile_size
                    block_y = col * tile_size
                    screen_x = block_x - player.camX
                    screen_y = block_y - player.camY

                    offset = (int(block_x - player.x), int(block_y - player.y))
                    if player.mineDir == "left":
                        pick_world_x = player.x - 20
                        pick_world_y = player.y + 12
                    elif player.mineDir == "right":
                        pick_world_x = player.x + 30
                        pick_world_y = player.y + 12
                    elif player.mineDir == "up":
                        pick_world_x = player.x + 10
                        pick_world_y = player.y - 20
                    elif player.mineDir == "down":
                        pick_world_x = player.x
                        pick_world_y = player.y + 40

                    pickoffset = (int(block_x - pick_world_x), int(block_y - pick_world_y))

                    if i == 1:
                        window.blit(self.grassBlock, (screen_x, screen_y))

                        if player.pick_mask.overlap(self.grassBlockMask, pickoffset):
                            self.map[v] = 0

                        if player.playerMask.overlap(self.grassBlockMask, offset):
                            self.collide(player, block_x, block_y)
                        

                    elif i == 2:
                        window.blit(self.dirtBlock, (screen_x, screen_y))

                        if player.pick_mask.overlap(self.dirtBlockMask, pickoffset):
                            self.map[v] = 0

                        if player.playerMask.overlap(self.dirtBlockMask, offset):
                            self.collide(player, block_x, block_y)

                    if i == 3:
                        continue

    
class Game():
    def __init__(self):
        self.running = True
         
        self.W, self.H = 1000, 800

        self.window = pygame.display.set_mode((self.W, self.H))
        self.clock = pygame.time.Clock()       
        self.Player = Player(self.W, self.H)
        self.Tilemap = Tilemap()
        self.last_row_added_y = self.Player.y

    def game(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.window.fill((255, 255, 255))

            if self.Player.y - self.last_row_added_y >= 60:
                for i in range(28):
                    if random.randint(1,15) == 2:
                        self.Tilemap.map.append(3)
                    else:
                        self.Tilemap.map.append(2)
                self.last_row_added_y += 60


            self.Player.update(self.window)
            self.Tilemap.draw(self.window, self.Player)
            print(self.clock.get_fps())
            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    Game().game()
