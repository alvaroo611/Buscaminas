import pygame
import random
import time
from threading import Thread,Semaphore
import threading
import array

# Inicializar pygame
pygame.init()
lock = threading.Lock()
stop_threads = threading.Event()

# Variables de configuración
width = 495
height = 495
block_size = 45
#Colores
VERDE=0,255,0
ROJO=255, 0, 0
NEGRO=(0, 0, 0)
stop=False
cont=0
cont2=0
final_min = 0
final_s = 0
reloj=pygame.image.load("reloj.png")
i=0
r = []

cv=0
cv2=0
min=1
icronometro=0
ti=0
boton=pygame.image.load("botonSinapretar.png")
boton_apretado = False
sprites2=pygame.sprite.Group()
# Configuración de la ventana
screen = pygame.display.set_mode((width, height))
def contarMinas(sprites,block):
    num_mines = 0
    for sprite in sprites:
            if sprite.rect.colliderect(block.rect.inflate(block_size, block_size)):
                if sprite.mina:
                    num_mines += 1
    return num_mines
def cronometro(r, stop):
    s=121
    print("Hola")
    for i in range(120,-1,-1):
        
        r.append(i)
        time.sleep(1)
       
              
    
# Función para revelar un bloque
def revelarBloque(cv2,cv,cont2,cont,stop,running,block, sprites, event):
    # Establecer estado de revelación del bloque en verdadero
    block.revelar = True
    
    # Si el bloque contiene una mina
    if block.mina and block.minaVerde==False:
        if event.type == pygame.MOUSEBUTTONUP and event.button==3 and block.bandera==False:
            block.bloqueo=True
            block.bandera=True
            block.image=pygame.image.load("bandera.png")
            cont2=cont2+1
            print("2=",cont2)
            if cont==cont2:
                image=pygame.image.load("GameWinner.jpg")
                screen.blit(image,(0,0))
                pygame.display.flip()# actualizamos la pantalla
                time.sleep(4)
                running=False
            
        elif event.type == pygame.MOUSEBUTTONUP and event.button==1   :
                block.bloqueo=True
                # Establecer color rojo para el bloque
                block.image=pygame.image.load("mina.png")
                stop=True
    
                
    elif event.type == pygame.MOUSEBUTTONUP and event.button==3 :
        block.bloqueo=True
        block.image=pygame.image.load("bandera.png")
    elif event.type == pygame.MOUSEBUTTONUP and event.button==1 and block.comodin==True and block.minaVerde==False:
        block.bloqueo=True
        block.image=pygame.image.load("Estrella.png")
        for block in sprites:
            if block.mina==True:
                block.image=pygame.image.load("mina.png")
                sprites.draw(screen)
                
        pygame.display.flip()
        time.sleep(1)
        for block in sprites:
            if block.mina==True:
                block.image=pygame.image.load("Cuadrado.png")
                sprites.draw(screen)
                
    elif event.type == pygame.MOUSEBUTTONUP and event.button==1 and block.verde==True:
        block.bloqueo=True
        block.image=pygame.image.load("verde.png")
        for block in sprites:
            
            if block.mina==True :
                cv=cv+1
                if cv==1 or cv2==2 and cv==1:
                    block.minaVerde=True
                    block.bloqueo=True
                    block.image=pygame.image.load("mina.png")
    elif event.type == pygame.MOUSEBUTTONUP and event.button==1 and block.verde2==True:
        block.bloqueo=True
        block.image=pygame.image.load("verde.png")
        for block in sprites:
            
            if block.mina==True:
                cv2=cv2+1
                if cv2==2 or cv2==2 and cv==1:
                    block.bloqueo=True
                    block.minaVerde=True
                    block.image=pygame.image.load("mina.png")

            
    


    elif event.type == pygame.MOUSEBUTTONUP and event.button==1 and block.comodin==False and block.minaVerde==False:
        block.bloqueo=True
        # Establecer color verde para el bloque
        block.image=pygame.image.load("espacio.png")   
        # Contar el número de minas alrededor
        num_mines=contarMinas(sprites,block)
        
        # Mostrar el número de minas alrededor en el bloque
        if num_mines==1 and block.comodin==False and block.minaVerde==False :
            block.image=pygame.image.load("numero1.png")
        elif num_mines==2 and block.comodin==False and block.minaVerde==False:
            block.image=pygame.image.load("numero2.png")
        elif num_mines==3 and block.comodin==False and block.minaVerde==False:
            block.image=pygame.image.load("numero3.png")
        elif num_mines==4 and block.comodin==False and block.minaVerde==False:
            block.image=pygame.image.load("numero4.png")
        elif num_mines==5 and block.comodin==False and block.minaVerde==False:
            block.image=pygame.image.load("numero5.png")
        

        
        # Si no hay minas alrededor, revelar bloques adyacentes
        if num_mines == 0:
            for sprite in sprites:
                if sprite.rect.colliderect(block.rect.inflate(block_size, block_size)):
                    if not sprite.revelar:
                        revelarBloque(cv2,cv,cont2,cont,stop,running,sprite, sprites,event)
    return cont2,stop,running

def crearBloque(x, y, mina):
    block = pygame.sprite.Sprite()
    block.image = pygame.Surface((block_size, block_size))
    # Establecer color blanco para el bloque
    block.image=pygame.image.load("Cuadrado.png")
    block.rect = block.image.get_rect()
    block.rect.x = x
    block.rect.y = y
    block.mina = mina
    # Establecer estado de revelación del bloque en falso
    block.revelar = False
    block.bandera=False
    block.comodin=False
    block.verde=False
    block.verde1=False
    block.verde2=False
    block.espacio=False
    block.bloqueo=False
    block.minaVerde=False
    return block

# Función para contar las minas alrededor de un bloque

# Crear un grupo de sprites
sprites = pygame.sprite.Group()
c=0
aleatorio = random.randint(1, 121)
aleatorio2 = random.randint(1, 121)
print("Aleatorio2",aleatorio2)
aleatorio3 = random.randint(1, 121)
print("Aleatorio3",aleatorio3)
# Crear bloques con minas aleatorias
for x in range(0, width, block_size):
    
    for y in range(0, height-50, block_size):
        
        c=c+1
        # Generar una mina aleatoria con una probabilidad del 20%
        mina = random.random() < 0.10
        
        if mina==True:
            cont=cont+1
        print(cont)
        
        block = crearBloque(x, y, mina)
        if aleatorio==c:
            block.comodin=True
            
        elif block.comodin==True and block.mina==True :
            block.mina=False
        elif aleatorio2==c:
            block.verde2=True
            if block.mina:
                block.mina=False
        elif aleatorio3==c:
            block.verde=True
            if block.mina:
                block.mina=False
        elif aleatorio2==aleatorio3:
            print("IGUALES")
            
        
        
        
            
        sprites.add(block)

# Bucle de juego
thread1 = Thread(target=cronometro ,args=(r,stop))
running = True

thread1.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                i=i+1
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Entrra",i)
                if mouse_x>=47 and mouse_x<=70 and mouse_y>=445 and mouse_y <=470 :
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    boton=pygame.image.load("botonApretar.png")
                    screen.blit(boton,(10,455))
                    sprites2=sprites.copy()
                    for block in sprites:
                        
                        num_mines=contarMinas(sprites,block)
                        if num_mines==1 and block.mina==False:
                            block.image=pygame.image.load("numero1.png")
                        elif num_mines==2 and block.mina==False:
                            block.image=pygame.image.load("numero2.png")
                        elif num_mines==3 and block.mina==False:
                            block.image=pygame.image.load("numero3.png")
                        elif num_mines==4 and block.mina==False:
                            block.image=pygame.image.load("numero4.png")
                        elif num_mines==5 and block.mina==False:
                            block.image=pygame.image.load("numero5.png")
                        elif block.mina==True:
                            block.image=pygame.image.load("mina.png")
                        elif block.comodin==True:
                            block.image=pygame.image.load("Estrella.png")
                        
                        else:
                            block.image=pygame.image.load("espacio.png")
                        if block.verde==True:
                            block.image=pygame.image.load("verde.png")
                        if block.verde2==True:
                            block.image=pygame.image.load("verde.png")
                    
                    
                    
        elif event.type == pygame.MOUSEBUTTONUP and event.button==1:
                

                if mouse_x>=47 and mouse_x<=70 and mouse_y>=445 and mouse_y <=470 :
                    boton=pygame.image.load("botonSinapretar.png")
                    screen.blit(boton,(10,460))
                    for block in sprites:
                        if block.bloqueo==False:
                            block.image=pygame.image.load("cuadrado.png")
                        elif block.bandera==True and block.bloqueo==True:
                            block.image=pygame.image.load("bandera.png")
                        
    
        if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONUP and (event.button==1 or event.button==3) and block.bandera==False:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print(mouse_x," e ",mouse_y)
            clicked_blocks = [b for b in sprites if b.rect.collidepoint(mouse_x, mouse_y) ]
            if clicked_blocks :
                cont2,stop,running=revelarBloque(cv2,cv,cont2,cont,stop,running,clicked_blocks[0],sprites,event)
            
                    
                    
                    
            
    screen.fill((0, 0, 0))
    screen.blit(reloj,(0,445))
    screen.blit(boton,(10,450))
    pygame.font.init()
    
    with lock:
        if icronometro <len(r):
            ti=r[icronometro]
            fuente = pygame.font.Font(None, 20).render(str(r[icronometro]), True, (255, 0, 0))
            screen.blit(fuente, (415, 462))
            icronometro += 1
            
            sprites.draw(screen)
            pygame.display.flip()
            if ti==0:
                stop=True
   
           
    if stop==True:
        
        
        for block in sprites:
            if block.mina==True:
                block.image=pygame.image.load("mina.png")
                sprites.draw(screen)
                pygame.display.flip()
        screen.blit(reloj,[0,445])

        screen.blit(boton,(10,455))
                
        pygame.display.flip()
        time.sleep(3)
        image=pygame.image.load("GameOver.jpg")
        screen.blit(image,(0,0))
        pygame.display.flip()
        time.sleep(2)
        running=False
        


# Salir de pygame
pygame.quit()