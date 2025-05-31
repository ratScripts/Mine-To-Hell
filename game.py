import pygame

pygame.init()

class Player():
    def __init__(self, W, H):
        self.x, self.y = W // 2, H // 2
        self.speed = 5
        self.W, self.H = W, H
        self.vy = 0
        self.grounded = False
        self.camX = self.x - W // 2
        self.camY = self.y - H // 2
        self.camVX = 0
        self.camVY = 0

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
        if keys[pygame.K_d]:
            self.x += self.speed

        if keys[pygame.K_SPACE] and self.grounded == False:
            self.vy = -6
    
        self.y += self.vy
        
    def draw(self, window):
        pygame.draw.rect(window, (0,0,0), (self.x - self.camX, self.y - self.camY, 50, 50))

class Tilemap():
    def __init__(self):
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
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,]
    

    def draw(self, window, W, H, camX, camY):
        
        for v, i in enumerate(self.map):
            row = v % 20
            column = v // 20
            if i == 0:
                pygame.draw.rect(window, (7, 207, 242), ((60 * row) - camX - W // 2, (60 * column) - camY - H // 2, 60, 60))
            elif i == 1:
                pygame.draw.rect(window, (21, 242, 10), ((60 * row) - camX - W // 2, (60 * column) - camY - H // 2, 60, 60))

            elif i == 2:
                pygame.draw.rect(window, (56, 21, 2), ((60 * row) - camX - W // 2, (60 * column) - camY - H // 2, 60, 60))
        


class Game():
    def __init__(self):
        self.running = True
         
        self.W, self.H = 1000, 800

        self.window = pygame.display.set_mode((self.W, self.H))
        self.clock = pygame.time.Clock()       
        self.Player = Player(self.W, self.H)
        self.Tilemap = Tilemap()

    def game(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.window.fill((255, 255, 255))


            self.Tilemap.draw(self.window, self.W, self.H, self.Player.camX, self.Player.camY)

            self.Player.controller()
            self.Player.camera()
            self.Player.draw(self.window)




            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    Game().game()
