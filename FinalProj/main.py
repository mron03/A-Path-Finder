import math
from grid import *
from algorithms import *


def main(win, width, ROWS):
    
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True

    b1 = button(win, (math.floor(WIN_WIDTH * 0.315), GRID_WIDTH + (WIN_WIDTH - GRID_WIDTH) // 4), "Single")
    b2 = button(win, (math.floor(WIN_WIDTH * 0.465), GRID_WIDTH + (WIN_WIDTH - GRID_WIDTH) // 4), "Double")
    b3 = button(win, (math.floor(WIN_WIDTH * 0.615), GRID_WIDTH + (WIN_WIDTH - GRID_WIDTH) // 4), "Reset")
    
    #TEXT
    font = pygame.font.Font('freesansbold.ttf', WIN_WIDTH // 40)
    text = font.render('Blue is start    Red is target    Black is barrier    Right Click to Reset Cell', True, WHITE, BLACK)
    textRect = text.get_rect()
    textRect.center = (WIN_WIDTH // 2, WIN_WIDTH * 0.95)

    while run:
        #update the display every loop
        draw(win, grid, ROWS, GRID_WIDTH)
        
        #update for text
        win.blit(text, textRect)

        #if QUIT then quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            #if buttons have been clicked and we dont have start or end being none
            if event.type == pygame.MOUSEBUTTONDOWN and (b1.collidepoint(pygame.mouse.get_pos()) or b2.collidepoint(pygame.mouse.get_pos())) and start and end:
                
                #update neighbors for every cell
                for row in grid:
                    for cell in row:
                        cell.update_neighbors(grid)
                        #reset color for every cell except start, end , barrier
                        if not cell == start and not cell == end and not cell.is_barrier():
                            cell.reset_color()

                #if it first button, lauch algorithm
                if b1.collidepoint(pygame.mouse.get_pos()):
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                
                #if second button launch double algorithms
                elif b2.collidepoint(pygame.mouse.get_pos()):
                    double_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                
                #set end to none, to make other cell an end
                start = end
                end = None
            
            #if it is Reset button, resets the grid
            if event.type == pygame.MOUSEBUTTONDOWN and b3.collidepoint(pygame.mouse.get_pos()):
                start = None
                end = None
                grid = make_grid(ROWS, width)

            #if left mouse click on grid    
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)

                #checks if negative values have been returned by get_clicked_pos
                if row < 0:
                    continue
                cell = grid[row][col]
                
                #if start is none and cell is not start
                if not start and cell != end:
                    start = cell
                    start.make_start()
                #if end is none and cell is not start
                elif not end and cell != start:
                    end = cell
                    end.make_end()
                #if cell is not start and not end
                elif cell != start and cell != end:
                    cell.make_barrier()

            #if right mouse click, basically resets any clicked cell
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                if row < 0:
                    continue
                cell = grid[row][col]
                
                
                if cell == start:
                    start = None
                elif cell == end:
                    end = None
            
                cell.reset_color()
            
            #same as button section, to calculate the path, but instead of button, if 
            #you click on keyboard 'S' then algorithm, if 'D' then double_algorithm, if 
            #ENTER then resets the grid
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_s or event.key == pygame.K_d) and start and end:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                            if not cell.is_start() and not cell.is_end() and not cell.is_barrier():
                                cell.reset_color()
                    
                    if event.key == pygame.K_s:
                        algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                    if event.key == pygame.K_d:
                        double_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                    start = end
                    end = None
            
                if event.key == pygame.K_RETURN:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, GRID_WIDTH, ROWS)