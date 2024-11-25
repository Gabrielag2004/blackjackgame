import copy
import random
import pygame

pygame.init()

# Variables

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
WIDTH = 800
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Blackjack')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
active = False

# Victoria, Derrota, Empate
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
results = ['', 'Jugador eliminado', 'El jugador gana :)', 'La casa gana :(', 'Empate...']


# Repartir las cartas seleccionándolas al azar de la baraja, y hacer función de carta en carta
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
    return current_hand, current_deck


# Dibujar las puntuaciones del jugador y del crupier en la pantalla
def draw_scores(player, dealer):
    screen.blit(font.render(f'Puntaje[{player}]', True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Puntaje[{dealer}]', True, 'white'), (350, 100))


# Dibujar cartas visualmente en la pantalla
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 465 + 5 * i))
        screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 635 + 5 * i))
        pygame.draw.rect(screen, '#d36e70', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)

    # Si el jugador no ha terminado su turno, la banca esconderá una carta
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 335 + 5 * i))
        else:
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 335 + 5 * i))
        pygame.draw.rect(screen, '#7fb5b5', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)


# Pasar en la mano del jugador o de la banca y obtener la mejor puntuación posible
def calculate_score(hand):
    # Calcular la puntuación de la mano fresca cada vez, comprobar cuántos ases tenemos
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        # Para 2,3,4,5,6,7,8,9 - basta con sumar el número al total
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        # Para cartas de 10 y caras, añada 10
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # Para los ases empezar sumando 11, comprobaremos si necesitamos reducir después
        elif hand[i] == 'A':
            hand_score += 11
    # Determinar cuántos ases deben ser 1 en lugar de 11 para bajar de 21 si es posible
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score


# Dibujar condiciones de juego y botones
def draw_game(act, record, result):
    button_list = []
    # Inicialmente al arrancar (no activo) la única opción es repartir nueva mano
    if not act:
        deal = pygame.draw.rect(screen, 'black', [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 3, 5)
        deal_text = font.render('Repartir', True, 'white')
        screen.blit(deal_text, (165, 50))
        button_list.append(deal)
    # Una vez iniciado el juego, botones de disparo y parada y registros de victorias/derrotas
    else:
        hit = pygame.draw.rect(screen, 'black', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 3, 5)
        hit_text = font.render('Pedir', True, 'white')
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)
        stand = pygame.draw.rect(screen, 'black', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 3, 5)
        stand_text = font.render('Quedarse', True, 'white')
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)
        score_text = smaller_font.render(f'Ganadas: {record[0]}   Perdidas: {record[1]}   Empate: {record[2]}', True, 'white')
        screen.blit(score_text, (15, 840))
    # Si hay un resultado para la mano que se ha jugado, mostrar un botón de reinicio e informar al usuario de lo sucedido
    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5)
        pygame.draw.rect(screen, '#89d07e', [150, 220, 300, 100], 5, 6)
        #pygame.draw.rect(screen, 'white', [153, 223, 294, 94], 3, 6)
        deal_text = font.render('Nueva Mano', True, 'black')
        screen.blit(deal_text, (165, 250))
        button_list.append(deal)
    return button_list


# Función de comprobación de las condiciones de final de partida
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    # Comprobar los escenarios de final de partida si el jugador se ha plantado, se ha pasado o ha hecho blackjack
    # Resultado 1- jugador reventado, 2-ganado, 3-perdido, 4-empujado
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add


# Juego principal
run = True
while run:
    # Ejecutar el juego a nuestra velocidad de fotogramas y llenar la pantalla con el color bg
    timer.tick(fps)
    screen.fill('black')
    # Reparto inicial al jugador y al crupier
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
    # Una vez activado el juego y repartido, calcular las puntuaciones y mostrar las cartas
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)
    buttons = draw_game(active, records, outcome)

    # Manejo de eventos, si se pulsa quit, entonces salir del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True
            else:
                # Si el jugador puede tomar, permitirle robar una carta
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                # Permitir al jugador terminar el turno 
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0


    # Si el jugador se pasa, finaliza automáticamente el turno - se trata como una parada
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

    pygame.display.flip()
pygame.quit()
