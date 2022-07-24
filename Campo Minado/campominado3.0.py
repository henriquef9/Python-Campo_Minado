
import pygame
import random

from pygame.locals import *

from sys import exit


pygame.init()

tamanho_matriz = 20
tela_largura = tamanho_matriz*20
tela_altura =  80 + (tamanho_matriz*20)


tela = pygame.display.set_mode((tela_largura,tela_altura))

pygame.display.set_caption('Campo Minado')



bandeira1 = pygame.image.load('./img/bandeira32px.png').convert_alpha()
bandeira2 = pygame.image.load('./img/bandeira16px.png').convert_alpha()

bombear = pygame.image.load('./img/bombear.png').convert_alpha()

#numeros
numero1 = pygame.image.load('./img/1.png').convert_alpha()
numero2 = pygame.image.load('./img/2.png').convert_alpha()
numero3 = pygame.image.load('./img/3.png').convert_alpha()
numero4 = pygame.image.load('./img/4.png').convert_alpha()
numero5 = pygame.image.load('./img/5.png').convert_alpha()

circulo = pygame.image.load('./img/circle.png').convert_alpha()
circulo = pygame.transform.scale(circulo,(30,30))

fonte = pygame.font.SysFont('arial', 30, True, True) 

# matriz 

matriz_coordenadas = []
matriz_bombas = []
matriz_bandeiras = []
matriz_numeros = []
matriz_imgNumeros = []
matriz_quadradosRevelados = []

matriz_cor = [[16,54,168],[22,70,217],[215,184,153],[229,194,159]]

vetor_sequencia = []
vetor_sequencia2 = []

bombas = 40

# função 

def gerar_Matriz_Coord(tamanho):
    pos_quadrado_x = 0
    pos_quadrado_y = 80
    matriz = []
    for i in range(tamanho):
        linha = []
        for j in range(tamanho):
            cord =[]
            for f in range(tamanho):
                cord = []
                cord.append(pos_quadrado_x)
                cord.append(pos_quadrado_y)
            pos_quadrado_x+=20   
            linha.append(cord)                 
        matriz.append(linha)
        pos_quadrado_x =0
        pos_quadrado_y+=20
    return matriz        

def desenharQuadrados(matriz,matriz_cor):
    global vetor_sequencia
    cor1 = matriz_cor[0]
    cor2 = matriz_cor[1]
    cor3 = matriz_cor[2]
    cor4 = matriz_cor[3]
    for linha in matriz:
        for xey in linha:
            pygame.draw.rect(tela,(cor1),(xey[0],xey[1],20,20))
            vetor_sequencia.append(cor3)
            vetor_sequencia2.append(cor1)
            cor1,cor2 = cor2, cor1
            cor3,cor4 = cor4, cor3
        if len(matriz)%2==0:   
            cor1,cor2 = cor2, cor1
            cor3,cor4 = cor4, cor3  
              

# bombas        
def posicao_aleatoria():
        return random.randint(0,tamanho_matriz-1),random.randint(0,tamanho_matriz-1) 
    
def gerar_bombas(matriz):
    global tamanho_matriz, bombas
    matrizBombas = []
    # vai guarda linha e coluna da matriz aonde está localizadar a coordenadar, com objetivo de evitar 
    # reptição de posição x e y das bombas.
    guarda_LinhaeColuna = []
    c=0
    while c < bombas:
        linha,coluna = posicao_aleatoria()
        if not [linha,coluna] in guarda_LinhaeColuna:
            coord = matriz[linha][coluna]
            matrizBombas.append(coord)
        else:
            c-=1   
        guarda_LinhaeColuna.append([linha,coluna])    
        c+=1 
        
    return matrizBombas   

def imprimirBombas(matriz):
    for linha in matriz:
        tela.blit(bombear,(linha))   
       
        

# melhorar aqui              
def gerar_numeros(matriz_bombas):
    global tela_altura, tela_largura
    matriz_numeros = []
    for linha in matriz_bombas:
        matriz_aux = []
        matriz_aux.append([linha[0]-20,linha[1]-20])
        matriz_aux.append([linha[0]-20,linha[1]])
        matriz_aux.append([linha[0]-20,linha[1]+20])
        matriz_aux.append([linha[0],linha[1]-20])
        matriz_aux.append([linha[0],linha[1]+20])
        matriz_aux.append([linha[0]+20,linha[1]-20])
        matriz_aux.append([linha[0]+20,linha[1]])
        matriz_aux.append([linha[0]+20,linha[1]+20])
        for xey in matriz_aux:
            if 0 <= xey[0] < tela_largura and 80<= xey[1] < tela_altura:
                matriz_numeros.append(xey)

    # retirar coordenadas onde tem bombas
    for linha1 in matriz_bombas:
        for linha2 in matriz_numeros:
            if linha1 == linha2:
                matriz_numeros.remove(linha2)   
    return matriz_numeros                

def carregar_img_numeros(matriz,matrizBombas):
    matriz_img = []
    # pegar coordenadas x e y de matriz(matriz_numero)           
    for xey in matriz:
        numero =0
        # verificar ser tem bombas ao redor da posição do numero 
        for bombar in matrizBombas:
            if bombar == [xey[0]-20,xey[1]-20]:
                numero+=1
            elif bombar == [xey[0]-20,xey[1]]:
                numero+=1
            elif bombar ==[xey[0]-20,xey[1]+20]:
                numero+=1     
            elif bombar == [xey[0],xey[1]-20]:
                numero+=1   
            elif bombar == [xey[0],xey[1]+20]:
                numero+=1     
            elif bombar == [xey[0]+20,xey[1]-20]:
                numero+=1    
            elif bombar == [xey[0]+20,xey[1]]:
                numero+=1    
            elif bombar ==[xey[0]+20,xey[1]+20]:
                numero+=1 
        # codição de gerar um vetor com a coordenada do numero e valor do numero           
        if numero > 0:
            v = [xey,numero]  
            matriz_img.append(v)  # [[x,y],[numero]]   
    return matriz_img 
    
def imprimir_numero(x,y):
    global matriz_imgNumeros
    # matriz(matriz_img)
    for linha in matriz_imgNumeros: # pegar [x,y],[numero] 
        # verificar qual foi a posição do numero clicada
        if linha[0][0] <= x < linha[0][0]+20 and linha[0][1] <= y < linha[0][1]+20: 
            # verificar qual e o valor quer representar a posição do numero
            if linha[1] == 1:
                tela.blit(numero1,(linha[0][0],linha[0][1]))
                
            elif linha[1] == 2:
                tela.blit(numero2,(linha[0][0],linha[0][1]))   
                 
            elif linha[1] == 3:
                tela.blit(numero3,(linha[0][0],linha[0][1]))  
                       
            elif linha[1] == 4:
                tela.blit(numero4,(linha[0][0],linha[0][1]))
            
            elif linha[1] == 5:
                tela.blit(numero5,(linha[0][0],linha[0][1]))  
            

# bandeiras

def colocarBandeira(matriz,x,y):
    # buscar qual foi o quabrado selecionado
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
          v = matriz[i][j]
          # verificar se posição do mouse está dentro da área do quadrado 
          if v[0] <= x < v[0]+20 and v[1] <= y < v[1]+20:
              # colocar bandeira na tela na posição do quadrado
              tela.blit(bandeira2,(v[0],v[1]))
              return v

def buscarCor(x,y,sequencia_cor):
    global matriz_coordenadas
    c=0
    
    for i in range(len(matriz_coordenadas)):
        for j in range(len(matriz_coordenadas[0])):
            if matriz_coordenadas[i][j][0] <= x < matriz_coordenadas[i][j][0]+20 and  matriz_coordenadas[i][j][1] <= y < matriz_coordenadas[i][j][1]+20:
                cor = sequencia_cor[c]
                return cor
            c+=1    

def removeBandeira(x,y):
    global  matriz_coordenadas, vetor_sequencia2,matriz_bandeiras
    
    # percorre cada coordenada da matriz(matriz_bandeira)
    for i in range(len(matriz_bandeiras)):
        #condição de para verificar qual foi a bandeira selecionada
        if matriz_bandeiras[i][0] <= x < matriz_bandeiras[i][0]+20 and  matriz_bandeiras[i][1] <= y < matriz_bandeiras[i][1]+20:
            # faz uma função para cor 
            # aqui vamos buscar a cor do quadrado para desenha ele novamente por cima da bandeira
            cor = buscarCor(x,y,vetor_sequencia2)
            #desenha o quadrado novamente
            pygame.draw.rect(tela,(cor),(matriz_bandeiras[i][0],matriz_bandeiras[i][1],20,20))
            return i         

            
def verificar_objeto(matriz,x,y):
    if matriz != []:
       for i in range(len(matriz)):
           if matriz[i][0] <= x < matriz[i][0]+20 and matriz[i][1] <= y < matriz[i][1]+20:
               return True
    return False       
      
 
def quebraQuadrado(matriz,x,y):
    global vetor_sequencia
    contador = 0
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            v = matriz[i][j]
            cor = vetor_sequencia[contador]
            if v[0] <= x < v[0]+20 and v[1] <= y < v[1]+20:
                pygame.draw.rect(tela,(cor),(v[0],v[1],20,20)) 
                return v
            contador+=1    
 
def bombas_AoRedor(x,y):
    x = (x//20)*20
    y = (y//20)*20
    
    global matriz_bombas
    
    for bombas in matriz_bombas:
        if bombas[0] == x-20 and bombas[1] == y-20:
            return True
        if bombas[0] == x-20 and bombas[1] == y:
            return True
        if bombas[0] == x-20 and bombas[1] == y+20:
            return True
        if bombas[0] == x and bombas[1] == y-20:
            return True
        if bombas[0] == x and bombas[1] == y+20:
            return True
        if bombas[0] == x+20 and bombas[1] == y-20:
            return True
        if bombas[0] == x+20 and bombas[1] == y:
            return True
        if bombas[0] == x+20 and bombas[1] == y+20:
            return True
    return False

def quebra_area(x,y):
    global matriz_numeros, matriz_quadradosRevelados, matriz_coordenadas, tela_largura, tela_altura,matriz_bandeiras, total_de_bandeiras
    if 0<= x < tela_largura and 80 <= y < tela_altura:
        
        if verificar_objeto(matriz_bandeiras,x,y):
            i = removeBandeira(x,y)
            # remove a coordenada da bandeira retirada da matriz_bandeiras
            matriz_bandeiras.pop(i)
            total_de_bandeiras+=1
        
        if verificar_objeto(matriz_quadradosRevelados,x,y):
            return 
        
        v = quebraQuadrado(matriz_coordenadas,x,y)
        matriz_quadradosRevelados.append(v)
        
        # imprimir os numeros
        if bombas_AoRedor(x,y):
            imprimir_numero(x,y)
            return 
                
        quebra_area(x-20,y)
        quebra_area(x+20,y)
        quebra_area(x,y-20)
        quebra_area(x,y+20)
        quebra_area(x-20,y-20)
        quebra_area(x-20,y+20)
        quebra_area(x+20,y-20)
        quebra_area(x+20,y+20)

def vitoria():
    global matriz_coordenadas, matriz_bombas,matriz_quadradosRevelados,tamanho_matriz
    
    # verificar ser todos os quadrados sem bombas foram quebrados
    if len(matriz_quadradosRevelados) ==  (tamanho_matriz*tamanho_matriz)-len(matriz_bombas): 
        return True
    return False 
            
    
def reiniciar_jogo():
    global flag, derrota, total_de_bandeiras, matriz_coordenadas, matriz_bombas, matriz_numeros, matriz_imgNumeros, matriz_bandeiras, matriz_quadradosRevelados, tempoInicial, tempoFinal
    derrota = False
    total_de_bandeiras = bombas
    flag = True
    matriz_coordenadas = gerar_Matriz_Coord(tamanho_matriz)
    matriz_bombas = gerar_bombas(matriz_coordenadas)
    matriz_numeros = gerar_numeros(matriz_bombas)
    matriz_imgNumeros = carregar_img_numeros(matriz_numeros,matriz_bombas)  
    matriz_bandeiras = []
    matriz_quadradosRevelados = []  
    tempoFinal =  pygame.time.get_ticks()//1000
    
    
    

matriz_coordenadas = gerar_Matriz_Coord(tamanho_matriz)
matriz_bombas = gerar_bombas(matriz_coordenadas)
matriz_numeros = gerar_numeros(matriz_bombas)
matriz_imgNumeros = carregar_img_numeros(matriz_numeros,matriz_bombas)


flag = True
derrota = False
total_de_bandeiras = bombas
tempoFinal = 0

while True:
    tempo = pygame.time.get_ticks()//1000
    min = (tempo-tempoFinal)//60
    seg = (tempo-tempoFinal) - min*60
    if tempo-tempoFinal > 60:
        texto3 = f"{min:02}:{seg:02}"
    else:
        texto3 = f"0:{tempo-tempoFinal:02}"    
        
       
    # criando os textos basicos do jogo
    texto1 = 'Tempo'
    texto2 = f'{total_de_bandeiras}'
    
    # formatando os textos
    texto_f1 = fonte.render(texto1,True, (255,255,255))
    texto_f2 = fonte.render(texto2,True, (255,255,255))
    texto_f3 = fonte.render(texto3,True, (255,255,255))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                posx, posy = event.pos # posição do mouse
                # verificar ser quadrado foi quebrado
                if not verificar_objeto(matriz_quadradosRevelados,posx,posy):
                    # verificar ser tem bandeira no quadrado
                    if not verificar_objeto(matriz_bandeiras,posx,posy):
                        # verificar ser tem bombar no quadrado    
                        if not verificar_objeto(matriz_bombas,posx,posy):    
                            quebra_area(posx,posy)    
                        else:
                        # caso tenha bombar vai imprimir todas as bombas    
                            imprimirBombas(matriz_bombas)
                            # declarar derrota com verdadeiro para entra condição posterior
                            derrota = True    
                
            if event.button == 3:
                posx, posy = event.pos
                #verificar ser ja foi quebrado o quadrado
                if not verificar_objeto(matriz_quadradosRevelados,posx,posy):
                    # verificar ser ja tem bandeira
                    if not verificar_objeto(matriz_bandeiras,posx,posy):
                        # verificar ser ja foi colocadar todas bandeiras disponiveis
                        if total_de_bandeiras > 0 and 0<= posx < tela_largura and 80<= posy <tela_altura:
                            matriz_bandeiras.append(colocarBandeira(matriz_coordenadas,posx,posy))
                            total_de_bandeiras-=1
                    # caso tenha bandeira vai remover ela        
                    else:
                        i = removeBandeira(posx,posy)
                        # remove a coordenada da bandeira da matriz_bandeiras
                        matriz_bandeiras.pop(i)
                        total_de_bandeiras+=1
                        
    
                        
    # desenha o quadrado principal     
    pygame.draw.rect(tela, (9,29,89),(0,0,tela_largura,80))
    # Bandeira Maior 32pix
    tela.blit(bandeira1,(280,20))
    # imprimir textos nas posições
    tela.blit(texto_f1,(38,20))
    tela.blit(texto_f2,(328,22))
    tela.blit(texto_f3,(150,22))

    
    # desenhar os quadrados do jogo uma vez apenas
    if flag:
        desenharQuadrados(matriz_coordenadas,matriz_cor)
        flag = False
    
    if vitoria():
        font2 = pygame.font.SysFont('arial',30,True,True)
        font4 = pygame.font.SysFont('arial',45,True,True)
        font3 = pygame.font.SysFont('arial',15,True,True)
        mensagem1 = "Parabéns! Você ganhou"
        mensagem2 = f"{texto3}"
        mensagem3 = "Jogar Novamente"
        texto_formatado1 = font2.render(mensagem1,True,(255,255,255))
        texto_formatado2 = font4.render(mensagem2,True,(255,255,255))
        texto_formatado3 = font3.render(mensagem3,True,(255,255,255))
        rect_texto1 = texto_formatado1.get_rect()
        rect_texto2 = texto_formatado2.get_rect()
        rect_texto3 = texto_formatado3.get_rect()
        
        while vitoria():
            for event in pygame.event.get():
              if event.type == QUIT: # condiçao para finalizar jogo
                pygame.quit()
                exit()
              if event.type == MOUSEBUTTONDOWN:
                  if event.button == 1:
                      x,y = event.pos
                      if tela_largura//2 -90 <=x <= tela_largura//2 +90 and tela_altura//2+50 <= y <= tela_altura//2+100:
                        reiniciar_jogo()
                        
            rect_texto1.center = (tela_largura//2,tela_altura//2-60)
            rect_texto2.center = (tela_largura//2,tela_altura//2)
            rect_texto3.center = (tela_largura//2+20,tela_altura//2+74)  
            
            pygame.draw.rect(tela,(0,0,255),(tela_largura//2 -90,tela_altura//2+50,180,50),0,10)   
           
            tela.blit(circulo,(tela_largura//2 -80,tela_altura//2+60)) 
            tela.blit(texto_formatado1,rect_texto1)
            tela.blit(texto_formatado2,rect_texto2)
            tela.blit(texto_formatado3,rect_texto3)              
            pygame.display.update()       
          
        
    # condição para derrota    
    if derrota:
        font2 = pygame.font.SysFont('arial',45,True,True)
        font3 = pygame.font.SysFont('arial',15,True,True) 
        mensagem1 = "Game over!"
        mensagem2 = "Jogar Novamente"
    
        texto_formatado1 = font2.render(mensagem1,False,(255,255,255))
        texto_formatado2 = font3.render(mensagem2,True,(255,255,255))
        rect_texto1 = texto_formatado1.get_rect()
        rect_texto2 = texto_formatado2.get_rect()
        
        # vai ficar lanço para repitir o texto ate o jogar reniciar o jogo ou para a execução do programa
        while derrota:
            for event in pygame.event.get():
              if event.type == QUIT: # condiçao para finalizar jogo
                pygame.quit()
                exit()
              if event.type == MOUSEBUTTONDOWN:
                  if event.button == 1:
                      x,y = event.pos
                      if tela_largura//2 -90 <=x <= tela_largura//2 +90 and tela_altura//2-25 <= y <= tela_altura//2+25:
                        reiniciar_jogo()
            rect_texto1.center = (tela_largura//2,tela_altura//2-80)
            rect_texto2.center = (tela_largura//2+20,tela_altura//2)    
            # button para reniciar(jogar novamente)
            pygame.draw.rect(tela,(0,0,255),(tela_largura//2 -90,tela_altura//2-25,180,50),0,10)
            tela.blit(circulo,(tela_largura//2 -80,tela_altura//2-15))
            # texto gamer over
            tela.blit(texto_formatado1,rect_texto1)     
            tela.blit(texto_formatado2,rect_texto2)    
                 
            pygame.display.update()       
          
    pygame.display.update()         


