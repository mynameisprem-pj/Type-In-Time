import random

WORDS = [
    "python", "game", "keyboard", "speed", "typing", "logic", "screen",
    "window", "score", "timer", "function", "variable", "class", "object",
    "human", "people", "person", "cinema", "Hobby", "Ice-cream", "Harion",
    "Thousand", "Extraordinary", "Personality", "words", "Random", "Police"
]

def get_random_word(exclude=None):
    if exclude is None:
        exclude = []

    available = [w for w in WORDS if w not in exclude]

    if not available:
        return random.choice(WORDS)     #fallback (rare)
    
    return random.choice(available)
