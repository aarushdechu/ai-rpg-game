import pygame
from ai_rpg_game.ui.fonts import WINDOW_WIDTH, WINDOW_HEIGHT, BLACK
from ai_rpg_game.ui.layout import draw_player_stats, draw_story_box
from ai_rpg_game.ui.buttons import Button
from ai_rpg_game.ui.events import handle_events
from ai_rpg_game.game_logic.memory import load_progress, save_progress
from ai_rpg_game.game_logic.main import game_loop, load_or_start_game


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("AI Dungeon Master RPG")

clock = pygame.time.Clock()

# Load game state
game_state = load_or_start_game()

# Story text to display
current_story = "🗺️ Your adventure begins..."

# --- Create Buttons ---
buttons = [
    Button(50, 400, 150, 50, "Attack", "attack"),
    Button(250, 400, 150, 50, "Explore", "explore"),
    Button(450, 400, 150, 50, "Talk", "talk"),
    Button(50, 480, 150, 50, "Inventory", "inventory"),
    Button(250, 480, 150, 50, "Shop", "shop"),
    Button(450, 480, 150, 50, "Quit", "quit")
]

# --- Main Game Loop ---
running = True
while running:
    screen.fill(BLACK)

    # Draw everything
    draw_player_stats(screen, game_state)
    draw_story_box(screen, current_story)

    mouse_pos = pygame.mouse.get_pos()
    for button in buttons:
        button.draw(screen, mouse_pos)

    # Handle events
    action = handle_events(buttons)

    if action:
        if action == "quit":
            running = False
        else:
            # Call backend game logic
            game_state, output = game_loop(game_state, player_action=action)

            # Update current story if new story came back
            if output.get("story"):
                current_story = output["story"]

            # If found gold while exploring
            if output.get("gold_found"):
                current_story = f"💰 You found {output['gold_found']} gold!"

            # If combat happened
            if output.get("combat_result"):
                if output["combat_result"]["result"] == "victory":
                    current_story = f"⚔️ You defeated {output['combat_result']['monster']['name']}!"
                else:
                    current_story = "💀 You have been defeated..."

    pygame.display.update()
    clock.tick(30)  # 30 FPS

save_progress(game_state)
pygame.quit()
