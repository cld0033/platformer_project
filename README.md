# Platformer Game for CPSC 4790 final project


### Key Sections:
1. **Game Description**: A brief overview of the game features and mechanics.
2. **Requirements**: Instructions to install Python, dependencies, and set up a virtual environment.
3. **How to Run**: Step-by-step guide to run the game after setting up the environment.
4. **Controls**: A list of game controls.
5. **Adjustable Difficulty**: Explanation of how the game difficulty affects the gameplay.
6. **Game Structure**: A brief description of the main files and their roles in the project.
7. **License**: You can include licensing information if applicable.
8. **Contributing**: A section for contributors if others want to collaborate.

Feel free to adjust the details based on your specific game implementation. Let me know if you'd like any changes or additions!


A 2D platformer game developed using Pygame, featuring dynamic difficulty options and enemy interactions. This game includes mechanics like player movement, bullet shooting, collision detection, and an adjustable difficulty system.

## Features

- **Player Movement**: Move the player character using keyboard inputs.
- **Shooting**: Shoot bullets at enemies with a simple shooting mechanic.
- **Enemies**: Includes enemy types (e.g., bees and worms) that spawn and interact with the player.
- **Difficulty Options**: Choose between "Easy" and "Hard" modes to adjust enemy speed, damage, and spawn rates.
- **Timers**: Dynamic game features like enemy spawning and bullet mechanics are controlled via timers.

## Requirements

To run this game, you'll need Python 3.x and Pygame installed.

### 1. Install Python 3.x
Make sure you have Python 3.x installed on your machine. You can download Python from the official website:  
[Download Python](https://www.python.org/downloads/)

### 2. Install Dependencies

Create a virtual environment and install the necessary dependencies by running:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
