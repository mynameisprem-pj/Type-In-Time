# game_logic.py

DIFFICULTY_SETTINGS = {
    "easy": {
        "fall_speed": 1.5,
        "spawn_interval": 2.5
    },
    "medium": {
        "fall_speed": 2.5,
        "spawn_interval": 1.8
    },
    "hard": {
        "fall_speed": 3.5,
        "spawn_interval": 1.2
    }
}

MIN_WORD_GAP = 60
LEFT_MARGIN = 40
RIGHT_MARGIN = 40

import pygame
import time
import random
from words import get_random_word
import json
import os
from utils import resource_path

def user_data_path(filename):
    return os.path.join(os.path.expanduser("~"), ".type_in_time", filename)

def ensure_data_dir():
    path = os.path.join(os.path.expanduser("~"), ".type_in_time")
    os.makedirs(path, exist_ok=True)

class FallingWord:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.speed = 1
    
    def move(self, speed):
        self.y += speed

class GameLogic:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.words = []
        self.active_word = None     # word currently being typed

        self.started = False
        self.paused = False
        self.game_over = False

        self.load_high_score()
        self.new_high_score = False
        self.speed = 0

        self.words_typed = 0
        self.active = False
        self.start_time = None
        self.elapsed_time = 0.0
        self.last_update_time = None

        self.difficulty = "easy"    # default
        self.apply_difficulty()

        self.current_input = ""
        self.last_spawn_time = time.time()
        self.spawn_interval = 2     #seconds

        
        # Sound
        self.blast_sound = pygame.mixer.Sound(resource_path("assets/blast.wav"))
    
    def start(self):
        self.active = True
        self.paused = False
        
        self.start_time = time.time()
        self.words.clear()
        self.current_input = ""
        self.last_spawn_time = time.time()

        if self.started or self.game_over:
            return
        
        self.started = True
        
        self.paused = False
        self.last_update_time = pygame.time.get_ticks()
        
        self.apply_difficulty()
    
    def toggle_pause(self):
        if not self.started or self.game_over:
            return
        
        self.paused = not self.paused

        if not self.paused:
            self.last_update_time = pygame.time.get_ticks()

    
    def reset(self):
        self.words.clear()
        self.current_input = ""
        self.elapsed_time = 0.0
        self.active_word = None

        self.words_typed = 0
        self.game_over = False
        self.paused = False
        self.active = True
        self.started = False

        self.start_time = time.time()
        self.last_spawn_time = time.time()
        self.last_update_time = None

        self.apply_difficulty()
    
    
    def update(self):
        if not self.started or self.paused or self.game_over:
            return
        
        now = pygame.time.get_ticks()
        delta = (now - self.last_update_time) / 1000    # conver ms - seconds
        self.elapsed_time += delta
        self.last_update_time = now

        if not self.active or self.game_over or self.paused:
            return
        
        # Spawn word every two seconds
        now = time.time()
        if now - self.last_spawn_time >= self.spawn_interval:
            existing_words = [w.text for w in self.words]
            new_text = get_random_word(existing_words)

            x = self.get_safe_x(new_text)
            new_word = FallingWord(new_text, x, 70)
            
            self.words.append(new_word)
            self.last_spawn_time = now
        
        # Move words
        for word in self.words[:]:
            word.move(self.word_speed)

            # If words reaches bottom - game over
            if word.y >= self.height - 80:
                self.game_over = True
                self.calculate_speed()
                self.check_high_score()
                self.active = False
                self.elapsed_time = int(time.time() - self.start_time)
                self.current_input = ""
                self.active_word = None
                return  # STOP: update immediately
    
    def handle_typing(self, char):
        if not self.active or self.game_over:
            return

        # Handle backspace
        if char == "\b":
            self.current_input = self.current_input[:-1]
        else:
            self.current_input += char

        # If nothing typed, reset active word
        if self.current_input == "":
            self.active_word = None
            return

        # Find all matching words
        matching_words = [
            w for w in self.words
            if w.text.startswith(self.current_input)
        ]

        # No match → reset input and active word
        if not matching_words:
            self.current_input = ""
            self.active_word = None
            return

        # Select the TOP-MOST matching word
        self.active_word = min(matching_words, key=lambda w: w.y)

        # Full word typed
        if self.current_input == self.active_word.text:
            self.words.remove(self.active_word)
            self.words_typed += 1
            self.current_input = ""
            self.blast_sound.play()
            self.active_word = None
    
    def get_safe_x(self, word_text):
        word_width = len(word_text) * 14    # approximate width per length
        max_attempts = 20

        for _ in range(max_attempts):
            x = random.randint(
                LEFT_MARGIN,
                self.width - RIGHT_MARGIN - word_width
            )

            # Check spacing against existing words
            safe = True
            for w in self.words:
                if abs(w.x - x) < word_width + MIN_WORD_GAP:
                    safe = False
                    break
            
            if safe:
                return x
            
        # Fallback (rare)
        return LEFT_MARGIN
    
    def get_elapsed_time(self):
        if not self.active and not self.game_over:
            return 0
        
        if self.start_time is None:
            return 0
        
        if self.game_over:
            return self.elapsed_time
        
        return int(time.time() - self.start_time)
    
    def get_speed(self):
        elapsed = self.get_elapsed_time()

        if elapsed <= 0:
            return 0
        
        return int((self.words_typed / elapsed) * 60)
    
    def apply_difficulty(self):
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        self.word_speed = settings["fall_speed"]
        self.spawn_interval = settings["spawn_interval"]

        if self.difficulty == "Easy":
            self.word_speed = 60
            self.spawn_interval = 2000
        
        elif self.difficulty == "Medium":
            self.word_speed = 90
            self.spawn_interval = 1400
        
        elif self.difficulty == "Hard":
            self.word_speed = 130
            self.spawn_interval = 900
    
    def set_difficulty(self, difficulty):
        difficulty = difficulty.lower()

        if difficulty in DIFFICULTY_SETTINGS:
            self.difficulty = difficulty
            self.apply_difficulty()
        else:
            raise ValueError(f"Invalid difficulty: {difficulty}")
    
    def load_high_score(self):
        ensure_data_dir()
        path = user_data_path("highscore.json")

        if not os.path.exists(path):
            self.high_scores = {"easy": 0, "medium": 0, "hard": 0}
            self.save_high_scores()
            return
        
        with open(path, "r") as f:
            self.high_scores = json.load(f)
    
    def save_high_scores(self):
        ensure_data_dir()
        path = user_data_path("highscore.json")

        with open(path, "w") as f:
            json.dump(self.high_scores, f, indent=4)
    
    def get_current_high_score(self):
        return self.high_scores.get(self.difficulty, 0)
    
    def check_high_score(self):
        current_high = self.high_scores[self.difficulty]

        if self.speed > current_high:
            self.high_scores[self.difficulty] = self.speed
            self.save_high_scores()
            self.new_high_score = True
        else:
            self.new_high_score = False
    
    def calculate_speed(self):
        if self.elapsed_time > 0:
            self.speed = int((self.words_typed / self.elapsed_time) * 60)
        else:
            self.speed = 0


    


    

    
