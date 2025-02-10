"""
Minesweeper Game using Pygame and Tkinter

This script implements a Minesweeper game with a graphical interface.
It includes functionality for saving and loading the game state using Tkinter's file dialog.
There is also a function for to undo the last move made in the game.

Author: MGC https://github.com/mgc-00/ 07/02/2025
"""

import tkinter as tk
import pickle
import copy
import random
from tkinter import filedialog
import pygame


# Define button class for handling button behavior
class Button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont("Arial", 18, bold=True)  # Make text bold
        self.text_surface = self.font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Black border
        screen.blit(self.text_surface, self.text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)


def draw_striped_border(screen, width, height, stripe_width=10):
    for i in range(0, width, stripe_width * 2):
        pygame.draw.rect(screen, (255, 255, 0), (i, 0, stripe_width, stripe_width))  # Top yellow
        pygame.draw.rect(screen, (0, 0, 0), (i + stripe_width, 0, stripe_width, stripe_width))  # Top black

        pygame.draw.rect(screen, (255, 255, 0), (i, height - stripe_width, stripe_width, stripe_width))  # Bottom yellow
        pygame.draw.rect(screen, (0, 0, 0), (i + stripe_width, height - stripe_width, stripe_width, stripe_width))  # Bottom black

    for i in range(0, height, stripe_width * 2):
        pygame.draw.rect(screen, (255, 255, 0), (0, i, stripe_width, stripe_width))  # Left yellow
        pygame.draw.rect(screen, (0, 0, 0), (0, i + stripe_width, stripe_width, stripe_width))  # Left black

        pygame.draw.rect(screen, (255, 255, 0), (width - stripe_width, i, stripe_width, stripe_width))  # Right yellow
        pygame.draw.rect(screen, (0, 0, 0), (width - stripe_width, i + stripe_width, stripe_width, stripe_width))  # Right black


class Board:
    def __init__(self, board_size, num_mines):
        self.board_size = board_size
        self.num_mines = num_mines
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.selected = [[False for _ in range(board_size)] for _ in range(board_size)]
        self.mine_positions = []
        self.history = []  # To track game history for undo functionality
        self.place_mines()

    def place_mines(self):
        self.mine_positions = []
        mines_placed = 0
        while mines_placed < self.num_mines:
            x = random.randint(0, self.board_size - 1)
            y = random.randint(0, self.board_size - 1)
            if self.board[x][y] != -1:
                self.board[x][y] = -1
                self.mine_positions.append((x, y))
                mines_placed += 1
        self.update_adjacent_numbers()

    def update_adjacent_numbers(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == -1:
                    continue
                count = 0
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        if 0 <= i < self.board_size and 0 <= j < self.board_size:
                            if self.board[i][j] == -1:
                                count += 1
                self.board[x][y] = count

    def make_move(self, x, y):
        if not self.selected[x][y]:
            self.selected[x][y] = True
            self.history.append((copy.deepcopy(self.board), copy.deepcopy(self.selected)))  # Save both board and selected state
            return True
        return False

    def undo_move(self):
        if self.history:
            self.board, self.selected = self.history.pop()  # Restore both board and selected state

    def is_winner(self):
        return sum([sum(row) for row in self.selected]) == (self.board_size**2 - self.num_mines)

    def hit_mine(self, x, y):
        return self.board[x][y] == -1

    def new_game(self):
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.selected = [[False for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.history = []
        self.place_mines()

    def save_game(self, filename="savegame.pkl"):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_game(filename="savegame.pkl"):
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            print("No saved game found.")
            return None


def ask_save_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")])
    return file_path


def ask_load_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")])
    return file_path


pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Minesweeper Game")
font = pygame.font.SysFont("Arial", 24)

button_width, button_height = 100, 50
button_color = (255, 255, 0)  # Yellow color

# Further adjust vertical positions for buttons to move them down a bit more
button_margin_top = 150  # Move buttons down further
buttons = [
    Button(width - button_width - 20, button_margin_top, button_width, button_height, button_color, "New Game"),
    Button(width - button_width - 20, button_margin_top + 70, button_width, button_height, button_color, "Load Game"),
    Button(width - button_width - 20, button_margin_top + 140, button_width, button_height, button_color, "Save Game"),
    Button(width - button_width - 20, button_margin_top + 210, button_width, button_height, button_color, "Undo Move")
]

board = Board(10, 10)

cell_size = 40  # Size of each cell in the grid

# Adjust the available width and height for the game grid (leaving space for buttons)
grid_width = width - button_width - 60  # Increase space between grid and buttons
grid_height = height - 40  # Leave space for margin at the top and bottom
cols = board.board_size
rows = board.board_size

cell_width = grid_width // cols
cell_height = grid_height // rows

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check for button clicks
            for button in buttons:
                if button.is_hovered(mouse_pos):
                    print(f"Button {button.text} clicked!")
                    if button.text == "Undo Move":
                        board.undo_move()
                    elif button.text == "New Game":
                        board.new_game()
                    elif button.text == "Save Game":
                        save_path = ask_save_file()
                        if save_path:
                            board.save_game(save_path)
                            print(f"Game saved to {save_path}")
                    elif button.text == "Load Game":
                        load_path = ask_load_file()
                        if load_path:
                            loaded_board = Board.load_game(load_path)
                            if loaded_board:
                                board = loaded_board
                                print(f"Game loaded from {load_path}")

            # Check for grid cell clicks
            x = (mouse_pos[0] - 20) // cell_width
            y = (mouse_pos[1] - 20) // cell_height
            if 0 <= x < board.board_size and 0 <= y < board.board_size:
                if board.make_move(x, y):
                    print(f"Cell clicked at {x}, {y}")
                if board.hit_mine(x, y):
                    print("You hit a mine!")

        screen.fill((0, 0, 0))  # Black background for the entire screen
        draw_striped_border(screen, width, height)

        # Draw the game grid
        for x in range(board.board_size):
            for y in range(board.board_size):
                cell_rect = pygame.Rect(20 + x * cell_width, 20 + y * cell_height, cell_width, cell_height)
                if board.selected[x][y]:
                    if board.board[x][y] == -1:  # Mine
                        pygame.draw.rect(screen, (255, 0, 0), cell_rect)
                    else:  # Number
                        pygame.draw.rect(screen, (200, 200, 200), cell_rect)
                        number_text = font.render(str(board.board[x][y]), True, (0, 0, 0))
                        screen.blit(number_text, cell_rect.move((cell_width - number_text.get_width()) // 2, (cell_height - number_text.get_height()) // 2))
                else:
                    pygame.draw.rect(screen, (180, 180, 180), cell_rect)
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 2)  # Black border for cells

        # Draw the buttons
        for button in buttons:
            button.draw(screen)

        pygame.display.update()

pygame.quit()
