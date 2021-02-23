import sys, pygame, os 

pygame.init() 
size = width, height = 600, 400 

screen = pygame.display.set_mode(size) 

white = 255,255, 255 
black = 0,0,0
green = 23, 200, 16
red  = 219, 15, 10
dark_red = 153, 9, 9
yellow = 245, 241, 10

class Bouncer(pygame.sprite.Sprite): 
    def __init__(self, startpos): 
        pygame.sprite.Sprite.__init__(self) 
        # Direction: 1=right, -1=left 
        self.direction = 1 
        
        # Loads the image and sets its position 
        self.image, self.rect = load_image("bouncer.png") 
        self.rect.centerx = startpos[0] 
        self.rect.centery = startpos[1] 
    
    def update(self): 
        # Makes the bouncer faster
        self.rect.move_ip((self.direction*3,0)) 
        
        # If the bouncer reaches the limits of the screen, reverses the direction 
        if self.rect.left < 0: 
            self.direction = 1 
        elif self.rect.right > width: 
            self.direction = -1 
    
class Ball(pygame.sprite.Sprite):  
    def __init__(self, startpos): 
        pygame.sprite.Sprite.__init__(self) 
        self.speed = [2,2] 
    
        # Loads the image and sets its position 
        self.image, self.rect = load_image("ball.png") 
        self.rect.centerx = startpos[0] 
        self.rect.centery = startpos[1] 
        
        # Sets the initial position for everytime the ball outs the scre 
        self.init_pos = startpos 
    
    def update(self): 
        self.rect.move_ip(self.speed) 
        
        # If the ball reaches the horizontals limits of the screen, reverses the direction(x) 
        if self.rect.left < 0 or self.rect.right > width: 
            self.speed[0] = -self.speed[0] 
        # If the ball reaches the verticals limits of the screen, reverses the direction(y) 
        if self.rect.top < 0: 
            self.speed[1] = -self.speed[1] 
        
        #If the ball reaches the screen bottom, sets the initial position 
        if self.rect.bottom > height: 
            self.rect.centerx = self.init_pos[0] 
            self.rect.centery = self.init_pos[1] 
            return -10
        return 0

def load_image(name): 
    fullname = os.path.join("img", name) 
    
    try: 
        image = pygame.image.load(fullname) 
    except pygame.error:
        print ("Cannot load image:", fullname) 
        raise SystemExit 
    
    return image, image.get_rect() 

def drawText(text, font, surface, color, pos_x, pos_y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (pos_x, pos_y)
    surface.blit(text_obj, text_rect)

def finish_game(surface):
    # Defines the font of the gameOver message
    game_over_font = pygame.font.SysFont(None, 30)
    subtitle_font =  pygame.font.SysFont(None, 25)

    surface.fill(white)
    
    pygame.draw.rect(screen, dark_red , [180, 130, 240, 130])
    drawText('GAMER OVER', game_over_font, surface, white, (230), (150))
    drawText('Tap SPACE to play again', subtitle_font, surface, white,(200),(200))




    
def main(): 
    # Defines the font of the points
    points_font = pygame.font.SysFont(None, 18)

    # Defines points of the gamer
    points = 0
    lifes = 3
    
    game_over = False

    # Defines the ball and the bouncer
    ball = Ball([100,100]) 
    bouncer = Bouncer([20,395])

    pygame.display.set_caption("PONG") 
    clock = pygame.time.Clock() 

    while 1: 
        # The program will run at 120fps 
        clock.tick(120) 

        # Checks the key pressed 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                sys.exit() 
            
            elif event.type == pygame.KEYDOWN: 
                # Moves the bouncer
                if event.key == pygame.K_LEFT: 
                    bouncer.direction = -1 
                if event.key == pygame.K_RIGHT: 
                    bouncer.direction = 1
                # Restarts the game 
                elif game_over == True and event.key == pygame.K_SPACE:
                    game_over = False
                    lifes = 3
                    points = 0
                    

        if (not game_over):        
            # Checks the colision and the ball direction 
            if bouncer.rect.colliderect(ball.rect): 
                if ball.speed[1] > 0: 
                    ball.speed[1] = -ball.speed[1] 
                    points += 10


            # Uptade of points and position of the objects
            user_mistake = ball.update()
            bouncer.update() 

            if ( user_mistake < 0 ):
                lifes -= 1
                points -= 0 if points <= 0 else 10 

            screen.fill(white) 
            
            if( lifes == 0 ):
                finish_game(screen)
                game_over = True
            else:
                # Reloading the objects
                screen.blit(ball.image, ball.rect) 
                screen.blit(bouncer.image, bouncer.rect) 

                # Reloading the user points 
                pygame.draw.rect(screen, dark_red , [30, 20, 90, 20])
                pygame.draw.rect(screen, black , [10, 20, 20, 20])
                drawText('Points: {}'.format(points), points_font, screen, white, 37,24)

                # Reloading the lifes bar                
                if( lifes == 3 ):
                    pygame.draw.rect(screen, green, [445, 20, 40, 20])
                    pygame.draw.rect(screen, green, [490, 20, 40, 20])
                    pygame.draw.rect(screen, green, [535, 20, 40, 20])

                elif ( lifes == 2 ):
                    pygame.draw.rect(screen, yellow, [490, 20, 40, 20])
                    pygame.draw.rect(screen, yellow, [535, 20, 40, 20])

                elif ( lifes == 1 ):
                    pygame.draw.rect(screen, red, [535, 20, 40, 20])
                
        
        pygame.display.flip()
           
    
if __name__ == "__main__": 
    main()

