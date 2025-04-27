import pygame
from ai_rpg_game.ui.fonts import WHITE, GOLD, RED, GREEN, BLUE, STATS_FONT, STORY_FONT, WINDOW_WIDTH


def draw_player_stats(screen, game_state):
    """Draw HP, Damage, Defense, Gold, Inventory on the left side."""
    x = 20
    y = 20
    line_spacing = 30

    stats = [
        f"❤️ Health: {game_state['health']}",
        f"⚔️ Damage: {game_state['damage']}",
        f"🛡️ Defence: {game_state['defence']}",
        f"💰 Gold: {game_state['gold']}",
        f"🎯 Goal: {game_state.get('current_goal', 'Wander freely')}",
    ]

    for stat in stats:
        text_surface = STATS_FONT.render(stat, True, WHITE)
        screen.blit(text_surface, (x, y))
        y += line_spacing

def draw_story_box(screen, story_text):
    """Draw the story narration area."""
    story_box_rect = pygame.Rect(250, 20, WINDOW_WIDTH - 270, 300)
    pygame.draw.rect(screen, (30, 30, 30), story_box_rect)  # Dark grey background
    pygame.draw.rect(screen, WHITE, story_box_rect, 2)  # White border

    # Render story text inside the box
    wrapped_text = wrap_text(story_text, STORY_FONT, story_box_rect.width - 20)
    text_y = story_box_rect.top + 10

    for line in wrapped_text:
        line_surface = STORY_FONT.render(line, True, WHITE)
        screen.blit(line_surface, (story_box_rect.left + 10, text_y))
        text_y += 25  # Line spacing

def wrap_text(text, font, max_width):
    """Helper to wrap long text into multiple lines."""
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines
