import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame

class MazeGameEnv(gym.Env):
    def __init__(self, maze):
        super(MazeGameEnv, self).__init__()
        self.maze = np.array(maze) #Maze represented as a 2D numpy array
        self.start_pos = np.where(self.maze == 'S') #Starting position
        self.goal_pos = np.where(self.maze == 'G') #Goal position
        self.current_pos = self.start_pos #Starting position is current position
        self.num_rows, self.num_cols = self.maze.shape

        # 4 possible actions: 0=up, 1=down, 2=left, 3=right
        self.action_space = spaces.Discrete(4)

        # Observation space is grid of size: rows x columns
        self.observation_space = spaces.Tuple((spaces.Discrete(self.num_rows), spaces.Discrete(self.num_cols)))

        #Initialize Pygame
        pygame.init()
        self.cell_size = 125

        # Setting display size
        self.screen = pygame.display.set_mode((self.num_cols*self.cell_size, self.num_rows*self.cell_size))
    
	def reset(self, options={}, seed=None):
		super().reset(seed=seed)
		self.current_pos = self.start_pos
		return self.current_pos, {}
    
    def step(self, action):
        # Move the agent based on the selected action
        new_pos = np.array(self.current_pos)
        if action == 0: # Up
            new_pos[0] -=1
        elif action == 1: # Down
            new_pos[0] +=1
        elif action == 2: # Left
            new_pos[1] -=1
        elif action == 3: # Right
            new_pos[1] +=1
        
        #Check if new position is valid
        if self._is_valid_position(new_pos):
            self.current_pos = new_pos

        # Reward function
        if np.array_equal(self.current_pos, self.goal_pos):
            reward = 1.0
            done = True
        else:
            reward = 0.0
            done = False
        
        return self.current_pos, reward, done, False, {}
    
    def _is_valid_position(self, pos):
        row, col = pos 

        # If agent goes out of the grid
        if row < 0 or col < 0 or row >= self.num_rows or col >= self.num_cols:
            return False
        
        # If agent hits an obstacle
        if self.maze[row, col] == "#":
            return False
        
        return True
    
    def render(self):
        #Clear the screen
        self.screen.fill((255, 255, 255))

        # Draw env elements one cell at a time
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_left = col*self.cell_size
                cell_top = row*self.cell_size

                try:
                    print(np.array(self.current_pos)==np.array([row,col]).reshape(-1,1))
                except Exception as e:
                    print('Initial state')

                if self.maze[row, col] == "#": #Obstacle
                    pygame.draw.rect(self.screen, (0,0,0), (cell_left, cell_top, self.cell_size, self.cell_size))
                elif self.maze[row, col] == "S": #Starting position
                    pygame.draw.rect(self.screen, (0,255,0), (cell_left, cell_top, self.cell_size, self.cell_size))
                elif self.maze[row, col] == "G": #Goal positon    
                    pygame.draw.rect(self.screen, (255, 0, 0), (cell_left, cell_top, self.cell_size, self.cell_size))

                if np.array_equal(np.array(self.current_pos), np.array([row, col]).reshape(-1,1)): #Agent position
                    pygame.draw.rect(self.screen, (0,0,255), (cell_left, cell_top, self.cell_size, self.cell_size))

        pygame.display.update() #Update the display    

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()