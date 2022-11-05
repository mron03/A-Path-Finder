import pygame
from queue import PriorityQueue
import math
from algorithms import algorithm, double_algorithm

ROWS = 50
GRID_WIDTH = 700
WIN_WIDTH = 900
#Values that help to place elements to certain position 
#on display
RELOCATION_X = (WIN_WIDTH - GRID_WIDTH) // 2
RElOCATION_Y = math.floor((WIN_WIDTH - GRID_WIDTH) * 0.05)

pygame.init()
WIN = pygame.display.set_mode((WIN_WIDTH,WIN_WIDTH))
pygame.display.set_caption('A* Path Finder')

RED = (255, 0, 0 )
LIGHT_RED = (241, 148, 138 )

BLUE = (0, 0, 255)
LIGHT_BLUE = (112, 188, 249 )
DARK_BLUE = (0, 1, 255)

WHITE = (245, 245, 220)
BLACK = (0, 0, 0)

PURPLE = (142, 68, 173 )
ORANGE = (255, 77, 2)

DARK_GREY = (100, 100, 100)

CELL_COLOR = WHITE
GRID_COLOR = DARK_GREY
START_COLOR = BLUE
END_COLOR = RED
BARRIER_COLOR = BLACK
OPEN_COLOR = PURPLE
CLOSED_COLOR = (174, 214, 241 )
PATH_COLOR = LIGHT_BLUE

class Cell:
    def __init__(self, row, col, width, total_rows ):
        self.row = row
        self.col = col
        self.x = row * width    
        self.y = col * width
        self.color = CELL_COLOR
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == CLOSED_COLOR
    
    def is_open(self):
        return self.color == OPEN_COLOR
    
    def is_barrier(self):
        return self.color == BARRIER_COLOR

    def is_start(self):
        return self.color == START_COLOR
    
    def is_end(self):
        return self.color == END_COLOR

    def reset_color(self):
        self.color = CELL_COLOR

    def make_closed(self):
        self.color = CLOSED_COLOR
    
    def make_open(self):
        self.color = OPEN_COLOR

    def make_barrier(self):
        self.color = BARRIER_COLOR
    
    def make_start(self):
        self.color = START_COLOR
    
    def make_end(self):
        self.color = END_COLOR

    def make_path(self):
        self.color = PATH_COLOR
    
    #for animation of double algorithm
    def make_open_start(self):
        self.color = OPEN_COLOR
    def make_closed_start(self):
        self.color = CLOSED_COLOR

    #for animation of double algorithm
    def make_open_end(self):
        self.color = ORANGE
    def make_closed_end(self):
        self.color = LIGHT_RED
    
    #draws cells of grid
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x + RELOCATION_X, self.y + RElOCATION_Y, self.width, self.width))

    #adds neighbors around the cell
    def update_neighbors(self, grid):
        self.neighbors = []

        #up
        if self.row - 1 >= 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        
        #down
        if self.row + 1 < self.total_rows and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        
        #left
        if self.col - 1 >= 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
        
        #right
        if self.col + 1 < self.total_rows and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        

    
#creates a single list(grid) and then adds lists of cells
def make_grid(rows, width):
    grid =[]

    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i, j, gap, rows)
            grid[i].append(cell)

    return grid

#draws grid lines, gap used to identify x, y coordinates
# gap = width of one cell
def draw_grid(win, rows, width):
    gap = width // rows

    for i in range(rows + 1):
        #horizontal line, starting point is (RELOCX, ...) ending point (Width + RELOCX, ...)
        pygame.draw.line(win, GRID_COLOR, (RELOCATION_X, i * gap + RElOCATION_Y), (width + RELOCATION_X, i * gap + RElOCATION_Y))
        
        for j in range(rows + 1):
            #vertical line
            pygame.draw.line(win, GRID_COLOR, (j * gap + RELOCATION_X, RElOCATION_Y), (j * gap + RELOCATION_X, width + RElOCATION_Y))


#actually makes all grid, cells to display on screen, severally used in other functions
def draw(win,grid, rows, width):
    for row in grid:
        for cell in row:
            cell.draw(win)

    draw_grid(win, rows, width)

    pygame.display.update()


#turns the x, y position obtained by mouse to represent as row and col of values of grid
def get_clicked_pos(pos, rows, width):
    #gap = width of one cell
    gap = width // rows

    x, y = pos
    #if mouse clicked outside of grid, return negative, which then will be checked after return
    if x < RELOCATION_X or x >= width + RELOCATION_X or y < RElOCATION_Y or y >= width + RElOCATION_Y:
        return -1, -1

    #gets rid of relocation values to get the actual results for calc
    x = x - RELOCATION_X
    y = y - RElOCATION_Y
    
    row = (x // gap)  
    col = y // gap 

    return row, col

    
def button(screen, position, text):
    #text settings
    font = pygame.font.SysFont("freesansbold.ttf", WIN_WIDTH // 20)
    text_render = font.render(text, 1, (255, 255, 255))
    x, y, w , h = text_render.get_rect()
    
    #setting the sizes and location of buttons
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w , h))

    return screen.blit(text_render, (x, y))
 



       


