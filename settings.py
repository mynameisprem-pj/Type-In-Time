DIFFICULTIES = ["Easy", "Medium", "Hard"]

import pygame

class SettingsScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bg_color = (0, 0, 0)
        self.text_color = (255, 255, 255)

        self.font_title = pygame.font.SysFont("arial", 32, bold=True)
        self.font_hint = pygame.font.SysFont("arial", 18)

        # Difficulty
        self.selected_difficulty = "Easy"   #default

        self.diff_buttons = {}
        start_y = 180
        for i, diff in enumerate(DIFFICULTIES):
            self.diff_buttons[diff] = pygame.Rect(
                self.width // 2 - 90,
                start_y + i * 60,
                180,
                40
            )

        # Back button
        self.back_rect = pygame.Rect(30, 30, 80, 35)
    
    def draw(self, screen):
        screen.fill(self.bg_color)

        # Title
        title = self.font_title.render("Settings", True, self.text_color)
        screen.blit(
            title,
            title.get_rect(center=(self.width // 2, 80))
        )

        # Difficulty ui
        label = self.font_hint.render("Select Difficulty", True, (200, 200, 200))
        screen.blit(label, label.get_rect(center=(self.width // 2, 140)))

        for diff, rect in self.diff_buttons.items():
            if diff == self.selected_difficulty:
                color = (80, 160, 220)  # active
            else:
                color = (60, 60, 60)    # inactive
            
            pygame.draw.rect(screen, color, rect, border_radius=8)

            text = self.font_hint.render(diff, True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=rect.center))

        # Back button
        pygame.draw.rect(screen, (60, 60, 60), self.back_rect, border_radius=6)
        back_text = self.font_hint.render("Back", True, self.text_color)
        screen.blit(
            back_text,
            back_text.get_rect(center=self.back_rect.center)
        )
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                return ("back", self.selected_difficulty)
            
            for diff, rect in self.diff_buttons.items():
                if rect.collidepoint(event.pos):
                    self.selected_difficulty = diff
                    return ("difficulty", diff)
        
        return (None, None)
    
    def resize(self, width, height):
        self.width = width
        self.height = height

        # Recalculate difficulty buttons
        start_y = self.height // 2 - 60
        for i, diff in enumerate(self.diff_buttons):
            self.diff_buttons[diff].x = self.width // 2 - 90
            self.diff_buttons[diff].y = start_y + i * 60
