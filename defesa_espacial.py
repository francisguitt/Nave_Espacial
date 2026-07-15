import pygame
import sys
import random

# INIcialização
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Defesa Espacial")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 215, 0)  # Dourado Elegante
CYAN = (0, 255, 255)

# Fontes
def get_font(size):
    try:
        return pygame.font.Font("assets/fonts/press_start_2p.ttf", size)
    except:
        return pygame.font.SysFont("impact", size)

font_title = get_font(40)
font_text = get_font(16)
font_ui = get_font(20)
font_footer = get_font(10) # Rodapé reduzido

# Menu Principal
def show_menu():
    menu_bg = pygame.transform.scale(pygame.image.load("assets/images/menu_bg.png").convert(), (WIDTH, HEIGHT))

    waiting = True
    while waiting:
        screen.blit(menu_bg, (0, 0))

        title = font_title.render("DEFESA ESPACIAL", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        controls = [
            "CONTROLES:",
            "← Seta Esquerda - Mover Esquerda",
            "→ Seta Direita - Mover Direita",
            "Espaço - Atirar",
            "Pressione [ENTER] para Iniciar"
        ]

        for i, line in enumerate(controls):
            text = font_text.render(line, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 300 + (i * 40)))

        # Rodapé
        footer = font_footer.render("Desenvolvido por: JOSE FRANCISCO ALVES DE MOURA. RU: 5392746", True, WHITE)
        screen.blit(footer, (WIDTH // 2 - footer.get_width() // 2, HEIGHT - 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

# Fim de jogo / Vitoria ---
def show_game_over(msg, color):
    waiting = True
    while waiting:
        screen.fill(BLACK)
        text = font_title.render(msg, True, color)
        retry = font_ui.render("Pressione [R] para Reiniciar", True, GREEN)
        quit_txt = font_ui.render("Pressione [ESC] para Sair", True, WHITE)

        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(retry, (WIDTH // 2 - retry.get_width() // 2, HEIGHT // 2 + 20))
        screen.blit(quit_txt, (WIDTH // 2 - quit_txt.get_width() // 2, HEIGHT // 2 + 70))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return True
                if event.key == pygame.K_ESCAPE: return False

# Ciclo principal do jogo
def run_game():
    clock = pygame.time.Clock()
    frames = 0

    bg = pygame.transform.scale(pygame.image.load("assets/images/fundo.png").convert(), (WIDTH, HEIGHT))
    ship = pygame.transform.scale(pygame.image.load("assets/images/nave.png").convert_alpha(), (80, 80))
    enemy_img = pygame.transform.scale(pygame.image.load("assets/images/inimigo.png").convert_alpha(), (70, 70))
    expl_img = pygame.transform.scale(pygame.image.load("assets/images/explosao.png").convert_alpha(), (70, 70))

    sound_shoot = pygame.mixer.Sound("assets/sounds/tiro.mp3")
    sound_expl = pygame.mixer.Sound("assets/sounds/explosao.mp3")

    ship_x, ship_y = (WIDTH // 2 - 40), (HEIGHT - 100)
    bullets, enemies, e_bullets, explosions = [], [], [], []
    score = 0

    running = True
    while running:
        frames += 1
        timer = frames // 60

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullets.append([ship_x + 35, ship_y])
                sound_shoot.play()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and ship_x > 0: ship_x -= 6
        if keys[pygame.K_RIGHT] and ship_x < WIDTH - 80: ship_x += 6

        if random.randint(1, 45) == 1:
            enemies.append([random.randint(0, WIDTH - 70), -70])

        for e in enemies:
            e[1] += 3
            if random.randint(1, 100) <= 2: e_bullets.append([e[0] + 35, e[1] + 70])

        for b in bullets: b[1] -= 10
        for eb in e_bullets: eb[1] += 7

        ship_rect = pygame.Rect(ship_x, ship_y, 80, 80)
        for e in enemies[:]:
            if ship_rect.colliderect(pygame.Rect(e[0], e[1], 70, 70)):
                sound_expl.play()
                return show_game_over("GAME OVER!", RED)
            for b in bullets[:]:
                if pygame.Rect(b[0], b[1], 4, 15).colliderect(pygame.Rect(e[0], e[1], 70, 70)):
                    explosions.append([e[0], e[1], 15])
                    sound_expl.play()
                    enemies.remove(e)
                    bullets.remove(b)
                    score += 1

        screen.blit(bg, (0, 0))
        for b in bullets: pygame.draw.rect(screen, GREEN, (b[0], b[1], 6, 20))
        for eb in e_bullets: pygame.draw.rect(screen, RED, (eb[0], eb[1], 6, 20))
        for e in enemies: screen.blit(enemy_img, (e[0], e[1]))
        for exp in explosions:
            if exp[2] > 0: screen.blit(expl_img, (exp[0], exp[1])); exp[2] -= 1
        screen.blit(ship, (ship_x, ship_y))

        score_text = font_ui.render(f"PONTOS: {score} / 15", True, WHITE)
        time_text = font_ui.render(f"TEMPO: {timer}s", True, YELLOW)
        screen.blit(score_text, (20, 20))
        screen.blit(time_text, (WIDTH - 200, 20))

        if score >= 15: return show_game_over("VITÓRIA!", GREEN)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    show_menu()
    while run_game(): pass
    pygame.quit()
    sys.exit()