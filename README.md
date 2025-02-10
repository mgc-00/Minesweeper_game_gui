https://github.com/mgc-00/

Minesweeper (Pygame Version)

Overview

This is a graphical Minesweeper game built using Pygame. The game features an interactive 10x10 grid where players can reveal cells, flag mines, undo moves, and save/load their progress. The game includes a clean user interface with buttons for managing gameplay actions.
________________________________________
Features

* Graphical Interface: Built using Pygame, featuring a visually appealing grid and buttons.
* 10x10 Grid with Random Mines: The board is generated dynamically with 10 mines placed randomly.
* Recursive Cell Reveal: Clicking an empty cell reveals surrounding cells recursively.
* Mine Detection: If a player clicks on a mine, the game ends.
* Undo Last Move: Players can undo their last move if they make a mistake.
* Save & Load Game: Players can save their progress and resume later.
* New Game Option: Players can restart the game at any time.
* Custom Borders & Button Design: Includes a striped yellow-black border and bold, easy-to-read buttons.
________________________________________
How to play the game

1.	Start the Game: Launch the game, and a 10x10 grid will be displayed.
2.	Click a Cell: 
o	If the cell contains a mine, the game ends.
o	If the cell is empty, adjacent cells will reveal recursively.
o	If the cell has a number, it indicates the count of nearby mines.
3.	Use the Buttons: 
o	New Game: Resets the board with a new mine placement.
o	Undo Move: Reverts the last move.
o	Save Game: Saves the current progress.
o	Load Game: Loads a previously saved game.
4.	Win Condition: The player wins by revealing all non-mine cells.
________________________________________
Game Controls

•	Left-click on a cell to reveal it.
•	Use buttons on the right panel to interact with the game.
•	Exit the game by closing the window.
________________________________________
Installation & Running the Game

1. Install Python and Pygame

Ensure you have Python 3.x installed. You can download it from:

https://www.python.org/downloads/

Then, install Pygame:

pip install pygame

2. Run the Game

Save the script as minesweeper.py and run:

python minesweeper.py

________________________________________
Executable file 

A compiled .exe of the game can be found in the dist folder.
________________________________________
Code Structure

1. Button Class
•	Handles button rendering and click detection.
2. Board Class
•	Generates the game grid.
•	Randomly places mines.
•	Calculates adjacent mine numbers.
•	Handles user moves, win conditions, and game history for undo functionality.
3. Game Loop
•	Handles user input (clicking cells, pressing buttons).
•	Updates the display after each action.
________________________________________
Game Algorithm

1. Initializing the Game
•	The game board is represented as a 10x10 grid.
•	10 mines are randomly placed on the grid.
•	Each non-mine cell is initialized as empty.
2. Handling Cell Selection
•	If a player clicks on a mine, the game ends.
•	If the selected cell is empty, it triggers a recursive reveal:
•	All adjacent empty cells are revealed until numbered cells are encountered.
•	If a numbered cell is clicked, only that cell is revealed.
3. Counting Adjacent Mines
•	For every numbered cell, the game calculates the number of surrounding mines.
•	The count is stored in the corresponding cell.
4. Undo Move Mechanism
•	Every move is stored in a history stack.
•	If the player clicks Undo Move, the previous board state is restored.
5. Win Condition
•	The game checks if all non-mine cells have been revealed.
•	If true, the player wins and a victory message is displayed.
________________________________________
Planned Improvements

* Adding a Timer to track how long a player takes to win.
* Implementing Flagging to mark suspected mines.
* Difficulty Selection (Easy, Medium, Hard).
* Better Game Over Screen with animations.
________________________________________
Acknowledgments

This project was built using Python & Pygame, with additional features for a better gameplay experience.
Let me know if you'd like further improvements or additional features!

