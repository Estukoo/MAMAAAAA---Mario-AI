import math
import pygame
import numpy as np

class Compteur:
    def __init__(self):
        self.input = 0
        self.output = 0
        self.weight = 0.01
        self.weighted_input = 0.0
        
        self.padding = 65
        
    def update(self, input, output, weight, weighted_input):
        self.input = input
        self.output = output
        self.weight = weight
        self.weighted_input = weighted_input
        
    def draw(self, screen):
        self.font = pygame.font.SysFont("consolas", 15)
        
        # Dessiner le point d'entrée avec la valeur d'entrée
        pygame.draw.circle(screen, (255, 255, 255), (self.padding, self.padding), 15)
        text = self.font.render(str(self.input), True, (0, 0, 0))
        screen.blit(text, (self.padding-12, self.padding+20))
        
        # Dessiner la connexion (trait) avec le poids de la connexion
        pygame.draw.line(screen, (255, 255, 255), (self.padding, self.padding), (5*self.padding, self.padding), 5)
        text = self.font.render(str(self.weight), True, (0, 0, 0))
        screen.blit(text, (self.padding*2.95, self.padding-20))
        
        self.font = pygame.font.SysFont("consolas", 10)
        
        text = self.font.render(f"({str(self.weighted_input)})", True, (0, 0, 0))
        screen.blit(text, (self.padding*2.25, self.padding+10))
        
        self.font = pygame.font.SysFont("consolas", 15)
        
        # Dessiner le point de sortie avec la valeur de sortie
        pygame.draw.circle(screen, (255, 255, 255), (5*self.padding, self.padding), 15)
        text = self.font.render(str(self.output), True, (0, 0, 0))
        screen.blit(text, (5*self.padding-3, self.padding+20))

class Assets:
    @staticmethod
    def scale_image(image, factor):
        """Scales the given image by the given factor"""
        return pygame.transform.scale(image, (image.get_width() // factor, image.get_height() // factor))
      
    @staticmethod
    def flip_image(image):
        """Flips the given image horizontally"""
        return pygame.transform.flip(image, True, False)
      
class Mario:
    def __init__(self):
        self.state = 0 # 0 = not yelling, 1 = yelling
        self.x = 0
        self.y = 0
        self.scale = 4
        self.image_not_yelling = Assets.scale_image(pygame.image.load("Assets/Mario.png"), self.scale)
        self.image_yelling = Assets.scale_image(pygame.image.load("Assets/MarioYelling.png"), self.scale)
        
        pygame.mixer.init()
        
        self.sound_yelling = pygame.mixer.Sound("Assets/MARIO_SCREAMING.mp3")
        
        self.width, self.height = self.image_not_yelling.get_size()

    def set_position(self, x, y):
        self.x = x - self.width / 2
        self.y = y - self.height / 2
        
    def is_yelling(self):
        return self.state == 1
    
    def draw(self, screen):
        if self.state == 0:
            screen.blit(self.image_not_yelling, (self.x, self.y))
            pygame.mixer.Sound.stop(self.sound_yelling)
        else:
            screen.blit(self.image_yelling, (self.x, self.y))
            pygame.mixer.Sound.play(self.sound_yelling)

class Boo:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.scale = 13
        self.image = Assets.scale_image(pygame.image.load("Assets/Boo.png"), self.scale)
        self.image = Assets.flip_image(self.image)
        self.width, self.height = self.image.get_size()

    def set_position(self, x, y):
        self.x = x - self.width / 2
        self.y = y - self.height / 2
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
class AI:
    def __init__(self):
        self.mario = Mario()
        self.boo = Boo()
        self.compteur = Compteur()
        
        self.background_scale = 2
        
        # Création de la matrice de poids pour la synapse entre les neurones d'entrée et de sortie.
        self.weights = np.array([[0.01]])
        self.threshold = 2.5
        
    def update(self, mario_x, mario_y, boo_x, boo_y):
        self.mario.set_position(mario_x, mario_y)
        self.boo.set_position(boo_x, boo_y)
        
        # Calcul du vecteur d'entrée
        input_vector = np.array([[math.sqrt((self.mario.x - self.boo.x)**2 + (self.mario.y - self.boo.y)**2)]])
        
        # Exécution de la multiplication matricielle pour obtenir l'entrée pondérée
        weighted_input = np.matmul(input_vector, self.weights)
        
        # Appliquer la fonction de seuil pour obtenir la sortie
        output = 1 if weighted_input <= self.threshold else 0
        
        self.mario.state = output
        
        self.compteur.update(math.floor(input_vector[0][0]), output, self.weights[0][0], weighted_input[0][0])
        
    def draw(self, screen):
        self.mario.draw(screen)
        self.boo.draw(screen)
        self.compteur.draw(screen)

    def set_threshold(self, threshold):
        self.threshold = threshold
        
    def set_background(self, background_path):
        self.background = Assets.scale_image(pygame.image.load(background_path), self.background_scale)
        self.background_rect = self.background.get_rect()

    def draw_background(self, screen):
        screen.blit(self.background, self.background_rect)
        
App = AI()

# Initialisation de pygame
pygame.init()

# Création de la fenêtre de jeu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "MAMAAAAAA"

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)

# Définition de l'arrière-plan
App.set_background("Assets/Background.jpg")

# Boucle du jeu principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Actualisation de la position du Boo en fonction de la position de la souris
        mouse_x, mouse_y = pygame.mouse.get_pos()
        App.update(100, 435, mouse_x, mouse_y)
            
    # Effacer l'écran
    SCREEN.fill((0, 0, 0))
    
    # Dessinez l'arrière-plan
    App.draw_background(SCREEN)
    
    # Dessine Mario et Boo
    App.draw(SCREEN)
    
    # Mise à jour de l'affichage
    pygame.display.flip()

# Sortir de pygame
pygame.quit()
