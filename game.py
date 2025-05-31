import pygame

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
        self.playerSprite = pygame.transform.scale(pygame.image.load("Player.png").convert_alpha(), (42, 60))
        self.flipped = False
        self.playerMask = pygame.mask.from_surface(self.playerSprite)
        

    def camera(self):

        targetX = self.x - self.W // 2
        targetY = self.y - self.H // 2
        self.camVX = (targetX - self.camX) * 0.1
        self.camVY = (targetY - self.camY) * 0.1
        self.camX += self.camVX
        self.camY += self.camVY


    def controller(self):


        if self.grounded == False:
            self.vy += 0.3


        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x -= self.speed
            self.flipped = True
        if keys[pygame.K_d]:
            self.x += self.speed
            self.flipped = False

        if keys[pygame.K_SPACE] and self.grounded:
            self.vy = -6

        self.grounded = False 
    
        self.y += self.vy
        
    def draw(self, window):
        window.blit(self.playerSprite if not self.flipped else pygame.transform.flip(self.playerSprite, True, False), (self.x - self.camX, self.y - self.camY))


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

        self.map = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    

    def draw(self, window, W, H, player):
        for v, i in enumerate(self.map):
            row = v % 20
            col = v // 20
            block_x = (60 * row)
            block_y = (60 * col)

            screen_x = block_x - player.camX
            screen_y = block_y - player.camY

            if i != 0:
                window.blit(self.grassBlock if i == 1 else self.dirtBlock, (screen_x, screen_y))

                offset = (int(block_x - player.x), int(block_y - player.y))

                if player.playerMask.overlap(self.grassBlockMask if i == 1 else self.dirtBlockMask, offset):
                    player_rect = pygame.Rect(player.x, player.y, 60, 60)
                    block_rect = pygame.Rect(block_x, block_y, 60, 60)

                    if player.vy > 0 and player_rect.bottom - player.vy <= block_rect.top:
                        player.y = block_rect.top - 60
                        player.vy = 0
                        player.grounded = True
                    elif player.vy < 0 and player_rect.top - player.vy >= block_rect.bottom:
                        player.y = block_rect.bottom
                        player.vy = 0
                    elif player.x + 42 > block_rect.left and player.x < block_rect.left and player_rect.bottom > block_rect.top and player_rect.top < block_rect.bottom:
                        player.x = block_rect.left - 42
                    elif player.x < block_rect.right and player.x + 42 > block_rect.right and player_rect.bottom > block_rect.top and player_rect.top < block_rect.bottom:
                        player.x = block_rect.right

    

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
                for i in range(20):
                    self.Tilemap.map.append(2)
                self.last_row_added_y += 60


            self.Tilemap.draw(self.window, self.W, self.H, self.Player)
            self.Player.update(self.window)

            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    Game().game()
