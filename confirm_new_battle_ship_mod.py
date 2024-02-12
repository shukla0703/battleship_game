#simple graphics battle ship program
#Using Pygames and random library
#pip3 install -m pygames
#modules used random and os

import pygame
import sys
import random
import os


pygame.init()
pygame.mixer.init()

# Set up display
width, height = 400, 400
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Battleship Game')

# Colors
white = (255, 255, 255)

# Load images
ocean_image = pygame.image.load(os.path.join('images', 'ocean.png'))
ship_image = pygame.image.load(os.path.join('images', 'ship.png'))
miss_image = pygame.image.load(os.path.join('images', 'miss.png'))
happy_animation_image = pygame.image.load(os.path.join('images', 'happy_animation_frame.png'))
sad_animation_image = pygame.image.load(os.path.join('images', 'animation_frame.png'))

# Load background music
pygame.mixer.music.load('your_music_file.mp3')

# Board attributes
board_size = 5
cell_size = width // board_size
board = [['O' for _ in range(board_size)] for _ in range(board_size)]
ship_row = random.randint(0, board_size - 1)
ship_col = random.randint(0, board_size - 1)

#Settings
time_limit = 10
music_enabled = True
show_ship_location = True

# Game loop
def game_loop():
    global start_time  

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()  

    # Start playing the music if music is enabled
    if music_enabled:
        pygame.mixer.music.play(-1) 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row = y // cell_size
                col = x // cell_size
                check_guess(row, col)

        display.fill(white)

        for row in range(board_size):
            for col in range(board_size):
                cell_value = board[row][col]
                if cell_value == 'O':
                    display.blit(ocean_image, (col * cell_size, row * cell_size))
                elif cell_value == 'X':
                    display.blit(miss_image, (col * cell_size, row * cell_size))
                elif cell_value == 'S' and show_ship_location:
                    display.blit(ship_image, (col * cell_size, row * cell_size))

        # Display elapsed time
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        remaining_time = max(0, time_limit - elapsed_time)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Time: {remaining_time}", True, (0, 0, 0))
        display.blit(text, (10, 10))

        # Check for time limit
        if elapsed_time >= time_limit:
            display_sad_animation()
            pygame.time.delay(2000)  # Additional delay after the animation
            print("Time's up! You didn't find the battleship.")
            pygame.quit()
            sys.exit()

        # Check for successful hit
        if any('S' in row for row in board):
            display_happy_animation()
            pygame.time.delay(2000)  # Additional delay after the animation
            print("Congratulations! You sunk my battleship!")
            pygame.quit()
            sys.exit()

        pygame.display.update()
        clock.tick(60)

# Function to display time-up animation with message
def display_sad_animation():
    global start_time

    frames = 60 
    animation_duration = 2000  

    for frame in range(frames):
        display.fill(white)

        # Display elapsed time
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = max(0, time_limit - elapsed_time // 1000)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Time: {remaining_time}", True, (0, 0, 0))
        display.blit(text, (10, 10))

        
        display.blit(sad_animation_image, (width // 2 - 100, height // 2 - 100))

        
        time_up_font = pygame.font.Font(None, 48)
        time_up_text = time_up_font.render("Time's up! You didn't find the battleship.", True, (255, 0, 0))
        display.blit(time_up_text, (width // 2 - 250, height // 2 + 50))

        pygame.display.update()
        pygame.time.delay(animation_duration // frames)

# Function to display happy animation with message
def display_happy_animation():
    global start_time
    frames = 60  
    animation_duration = 2000  

    for frame in range(frames):
        display.fill(white)

        # Display elapsed time
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = max(0, time_limit - elapsed_time // 1000)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Time: {remaining_time}", True, (0, 0, 0))
        display.blit(text, (10, 10))

        # Display happy animation image
        display.blit(happy_animation_image, (width // 2 - 100, height // 2 - 100))

        # Display congratulation message
        congratulation_font = pygame.font.Font(None, 48)
        congratulation_text = congratulation_font.render("Congratulations! You sunk my battleship!", True, (0, 255, 0))
        display.blit(congratulation_text, (width // 2 - 300, height // 2 + 50))

        pygame.display.update()
        pygame.time.delay(animation_duration // frames)

def check_guess(row, col):
    global board
    if row == ship_row and col == ship_col:
        board[row][col] = 'S'
        print("Congratulations! You sunk my battleship!")
        pygame.time.delay(1000)
        pygame.quit()
        sys.exit()
    else:
        board[row][col] = 'X'

def show_settings():
    global time_limit, music_enabled, show_ship_location
    print("Game Settings:")
    print(f"1. Time Limit: {time_limit} seconds")
    print(f"2. Music: {'Enabled' if music_enabled else 'Disabled'}")
    print(f"3. Show Ship Location: {'Enabled' if show_ship_location else 'Disabled'}")

    option = input("Enter the number of the setting to change (or press Enter to start the game): ")
    if option == '1':
        time_limit = int(input("Enter the new time limit in seconds: "))
    elif option == '2':
        music_enabled = not music_enabled
    elif option == '3':
        show_ship_location = not show_ship_location

if __name__ == "__main__":
    print("Welcome to Battleship!")

    # Check for settings
    if "--show-settings" in sys.argv:
        show_settings()
    else:
        print("Try to find the battleship by clicking on the cells.")
        game_loop()


#end of the program