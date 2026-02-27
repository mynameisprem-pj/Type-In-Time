import pygame
import sys
from game_logic import GameLogic
from settings import SettingsScreen
from utils import resource_path
import sys

# Initialize pygame
pygame.init()

# Initialize window size
WIDTH, HEIGHT = 800, 600

# Create a resizable window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Welcome to Prem's Typing Game!")

# Initailize game logic
game = GameLogic(WIDTH, HEIGHT)
settings_screen = SettingsScreen(WIDTH, HEIGHT)
current_screen = "game"

# Settings icon
settings_icon = pygame.image.load(resource_path("assets/settings.png")).convert_alpha()
settings_icon = pygame.transform.smoothscale(settings_icon, (18, 18))

ICON_SIZE = 18
ICON_PADDING = 20

settings_rect = pygame.Rect(
    WIDTH - ICON_SIZE - ICON_PADDING,
    18,
    ICON_SIZE,
    ICON_SIZE
)

# Sky blue color (RGB)
SKY_BLUE = (255, 206, 235)

# Soft ui colors
WHITE = (255, 255, 255)
SOFT_GRAY = (190, 190, 190)
DARK_GRAY = (100, 100, 100)
BUTTON_BLUE = (100, 170, 220)
BUTTON_NORMAL = (100, 170, 220)
BUTTON_HOVER = (120, 190, 240)
BUTTON_PRESSED = (70, 140, 190)
RED = (200, 50, 50)
RESULT_BG = (245, 250, 255)
BORDER_COLOR = (150, 180, 210)
GREEN = (0, 180, 0)
LINE_COLOR = (170, 200, 220)        # soft blue gray
LINE_THICKNESS = 3

# Fonts
font_small = pygame.font.SysFont("arial", 20)
font_medium = pygame.font.SysFont("arial", 24)
font_large = pygame.font.SysFont("arial", 28)
font_result = pygame.font.SysFont("arial", 42, bold=True)
font_title = pygame.font.SysFont("arial", 32, bold=True)
font_speed = pygame.font.SysFont("arial", 44, bold=True)
font_hint = pygame.font.SysFont("arial", 18)

# Clock to control frame rate
clock = pygame.time.Clock()

# Button Creation
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40
BUTTON_GAP = 30

total_width = (BUTTON_WIDTH * 3) + (BUTTON_GAP * 2)
start_x = (WIDTH - total_width) // 2
button_y = HEIGHT - 60

start_button = pygame.Rect(start_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
pause_button = pygame.Rect(start_x + BUTTON_WIDTH + BUTTON_GAP, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
reset_button = pygame.Rect(start_x + (BUTTON_WIDTH + BUTTON_GAP) * 2, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

pressed_button = None

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # --------------- SETTINGS SCREEN -----------
        if current_screen == "settings":
            action, value = settings_screen.handle_event(event)
            if action == "back":
                current_screen = "game"
                game.set_difficulty(value)
            elif action == "difficulty":
                game.set_difficulty(value)
        
        # --------------- KEYBOARD INPUT -------------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                game.handle_typing("\b")
            elif event.key == pygame.K_1:
                game.set_difficulty("easy")
            elif event.key == pygame.K_2:
                game.set_difficulty("medium")
            elif event.key == pygame.K_3:
                game.set_difficulty("hard")
            elif event.unicode and event.unicode.isprintable():
                game.handle_typing(event.unicode)
        
        # ------------- MOUSE INPUT -------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            if settings_rect.collidepoint(event.pos):
                current_screen = "settings"
            elif start_button.collidepoint(event.pos):
                pressed_button = "start"
            elif pause_button.collidepoint(event.pos):
                pressed_button = "pause"
            elif reset_button.collidepoint(event.pos):
                pressed_button = "reset"
        
        if event.type == pygame.MOUSEBUTTONUP:
            if pressed_button == "start" and start_button.collidepoint(event.pos):
                game.start()
            elif pressed_button == "pause" and pause_button.collidepoint(event.pos):
                game.toggle_pause()
            elif pressed_button == "reset" and reset_button.collidepoint(event.pos):
                game.reset()
        
            pressed_button = None
            
            
        # Handle window resize
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            settings_screen.resize(WIDTH, HEIGHT)

            game.width = WIDTH
            game.height = HEIGHT

            settings_screen.width = WIDTH
            settings_screen.height = HEIGHT

            settings_rect.x = WIDTH - ICON_SIZE - ICON_PADDING

            total_width = (BUTTON_WIDTH * 3) + (BUTTON_GAP * 2)
            start_x = (WIDTH - total_width) // 2
            button_y = HEIGHT - 60

            start_button.topleft = (start_x, button_y)
            pause_button.topleft = (start_x + BUTTON_WIDTH + BUTTON_GAP, button_y)
            reset_button.topleft = (start_x + (BUTTON_WIDTH + BUTTON_GAP) * 2, button_y)
    
    # Update game
    if current_screen == "game":
        game.update()
    
    # Fill background with sky blue color
    screen.fill(SKY_BLUE)

    # Top Divider line (below score, time, words)
    pygame.draw.line(
        screen,
        LINE_COLOR,
        (40, 65),
        (WIDTH - 40, 65),
        LINE_THICKNESS
    )

    # Horizontal divider line above buttons
    line_y = HEIGHT - 80
    pygame.draw.line(
        screen,
        LINE_COLOR,
        (40, line_y),
        (WIDTH - 40, line_y),
        LINE_THICKNESS
    )

    # Settings icon
    screen.blit(settings_icon, settings_rect.topleft)

    # Score , TIme, Words written (horizontal)
    total_seconds = int(game.elapsed_time)
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    speed_text = font_medium.render(f"Speed: {game.get_speed()} WPM", True, SOFT_GRAY)
    time_text = font_medium.render(f"Time: {minutes:02d}:{seconds:02d}", True, SOFT_GRAY)
    words_text = font_medium.render(f"Words: {game.words_typed}", True, SOFT_GRAY)
    
    high_value = game.get_current_high_score()
    high_text = font_medium.render(f"High: {high_value} WPM", True, SOFT_GRAY)

    top_texts = [
        speed_text,
        time_text,
        words_text,
        high_text
    ]

    padding_left = 40
    padding_right = 40

    available_width = WIDTH - padding_left - padding_right
    gap = available_width // len(top_texts)

    for i, text_surface in enumerate(top_texts):
        x = padding_left + i * gap + (gap - text_surface.get_width()) // 2
        y = 25
        screen.blit(text_surface, (x, y))

    # Draw falling words
    for word in game.words:
        x_offset = 0

        for i, letter in enumerate(word.text):
            # If typed letter matches this position, turn green
            if (
                word == game.active_word and
                i < len(game.current_input) and
                game.current_input[i] == letter
            ):
                color = GREEN    # green
            
            else:
                color = DARK_GRAY
            
            letter_surface = font_medium.render(letter, True, color)
            screen.blit(letter_surface, (word.x + x_offset, word.y))
            x_offset += letter_surface.get_width()

    # Typing input area box
    input_box_rect = pygame.Rect(40, HEIGHT - 140, WIDTH - 80, 40)
    pygame.draw.rect(screen, WHITE, input_box_rect, border_radius=8)
    pygame.draw.rect(screen, LINE_COLOR, input_box_rect, 2, border_radius=8)

    # Typed text display
    typed_surface = font_medium.render(game.current_input, True, DARK_GRAY)
    screen.blit(
        typed_surface,
        (input_box_rect.x + 10, input_box_rect.y + 8)
    )

    mouse_pos = pygame.mouse.get_pos()

    def draw_button(rect, label, name):
        if pressed_button == name:
            color = BUTTON_PRESSED
        elif rect.collidepoint(mouse_pos):
            color = BUTTON_HOVER
        else:
            color = BUTTON_NORMAL
        
        pygame.draw.rect(screen, color, rect, border_radius=8)
        text = font_small.render(label, True, WHITE)
        screen.blit(text, text.get_rect(center=rect.center))

    draw_button(start_button, "Start", "start")
    pause_label = "Resume" if game.paused else "Pause"
    draw_button(pause_button, pause_label, "Pause")
    draw_button(reset_button, "Reset", "reset")

    # Game over message
    if game.game_over:
        # Result panel size
        panel_width = 420
        panel_height = 260
        panel_x = (WIDTH - panel_width) // 2
        panel_y = (HEIGHT - panel_height) // 2

        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

        # pannel background
        pygame.draw.rect(
            screen,
            RESULT_BG,
            panel_rect,
            border_radius=12
        )

        # Panel border
        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            panel_rect,
            2,
            border_radius=12
        )

        # Text values
        speed = game.get_speed()
        words = game.words_typed
        elapsed = game.elapsed_time

        # Well played
        title_text = font_title.render("------ Game Over ------", True, DARK_GRAY)
        screen.blit(
            title_text,
            title_text.get_rect(center=(WIDTH // 2, panel_y + 35))
        )

        # Speed (big, red)
        speed_text = font_speed.render(f"{speed} WPM", True, RED)
        screen.blit(
            speed_text,
            speed_text.get_rect(center=(WIDTH // 2, panel_y + 90))
        )

        if game.new_high_score:
            congrats_text = font_large.render(
                "Congratulations! New High Score!",
                True,
                (235, 215, 0)   # gold
            )
            screen.blit(
                congrats_text,
                congrats_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
            )

        # WOrds and time
        stats_text = font_medium.render(
            f"Words: {words}    |   Time: {elapsed} sec",
            True,
            GREEN
        )
        screen.blit(
            stats_text,
            stats_text.get_rect(center=(WIDTH // 2, panel_y + 140))
        )

        # Reset hint box
        hint_rect = pygame.Rect(
            panel_x + 80,
            panel_y + panel_height - 55,
            panel_width - 160,
            30
        )

        pygame.draw.rect(
            screen,
            (230, 240, 250),
            hint_rect,
            border_radius=9
        )

        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            hint_rect,
            1,
            border_radius=6
        )

        hint_text = font_hint.render(
            "Click RESET to clear Screen",
            True,
            DARK_GRAY
        )
        
        screen.blit(
            hint_text,
            hint_text.get_rect(center=hint_rect.center)
        )

    elif current_screen == "settings":
        settings_screen.draw(screen)
     
    
    # Update the display
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(30)

pygame.quit()
sys.exit()
    
   
   
    




