import pygame
from queue import PriorityQueue

#calculates Heuristics
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw, start):
    stack = []

    #puts the path order in array
    while current in came_from:     
        stack.append(current)
        current = came_from[current]

    start.make_path()               

    #it draws the path from start to end until there is one element left
    #draws start then make it closed and jumps to the next-next cell to make it path
    while  len(stack) > 1:          #
        stack[-1].make_start()
        draw()

        # #to make dotted path
        # stack[-1].make_closed()
        # stack.pop()

        stack[-1].make_path()
        draw()
        
        # #for dotted
        # if len(stack) > 1:
        stack.pop()

    #colors the end the color of start
    stack[-1].make_start()          

    
  

def algorithm(draw, grid, start, end):
    #helps to decide which neighbor goes first if their g_score is equal
    #every cell has different count
    count = 0      
    #contains the cells that will be evaluated
    open_set = PriorityQueue()      
    open_set.put((0, count, start))

    #tracks the path from start to end
    came_from = {}
    
    #contains g scores
    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start] = 0

    #contains f scores
    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    #contains cell that have been looked at
    open_set_hash = {start} 
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()

        #takes the cell with lowest f score with help of priority queue
        current = open_set.get()[2] 
        #removes it, means that it has been checked
        open_set_hash.remove(current)

        #if it is the end contruct the path and return true
        if current == end:
            reconstruct_path(came_from, end, draw, start)
            return True

        #evaluate every neighbor of current
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            #if the g score of neighbor is less than what is already in the g score(of neighbor) in 
            # dictionary then replace old g score and f score with new scores
            #track who is the parent of neighbor
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                #if we looked at this neighbor first time,  record the count, place it in open_set
                #and open_set_hash, and make it open for the next evaluation as current
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        #if the current is not start make it closed, which means we evaluated his neighbors
        if current != start:
            current.make_closed()
    
    #if
    return False


def reconstruct_path_double(draw, came_from_start, came_from_end, current, start, end):
    stack = []

    #used to build a path from intection point to different directions
    #to start and to end
    current_end = current
    
    #used to animate path from intersection to end
    current_end1 = current

    while current in came_from_start or current_end in came_from_end:
        #intersection -> start
        if current in came_from_start: 
            current.make_path()
            stack.append(current)
            current = came_from_start[current]

        #intersection -> end
        if current_end in came_from_end and current_end != end:
            current_end.make_path()
            current_end = came_from_end[current_end]

        draw()


    start.make_path()     
    #moving of start towards -> intersection
    while  len(stack) > 1:
        #make it red
        stack[-1].make_start()
        draw()
        
        # #make it white and move to next-next
        # stack[-1].make_closed()
        # stack.pop()
        
        #make cell path color
        stack[-1].make_path()
        draw()

        stack.pop()
    
    #moving of start from intersection -> end
    i = 0
    while current_end1 in came_from_end:
        current_end1.make_path()
        
        # #to make dotted path
        # if i % 2 == 0:
        #     current_end1.make_closed()
        # i += 1

        current_end1 = came_from_end[current_end1]
        current_end1.make_start()
        draw()



#search path from both points
def double_algorithm(draw, grid, start, end):
    count_start = 0
    count_end = 0

    open_set_start = PriorityQueue()
    open_set_start.put((0, count_start, start))

    open_set_end = PriorityQueue()
    open_set_end.put((0, count_end, end))

    came_from_start = {}
    came_from_end = {}

    g_score_start = {cell: float("inf") for row in grid for cell in row}
    g_score_start[start] = 0

    f_score_start = {cell: float("inf") for row in grid for cell in row}
    f_score_start[start] = h(start.get_pos(), end.get_pos())

    g_score_end = {cell: float("inf") for row in grid for cell in row}
    g_score_end[end] = 0

    f_score_end = {cell: float("inf") for row in grid for cell in row}
    f_score_end[end] = h(end.get_pos(), start.get_pos())

    open_set_hash_start = {start}

    open_set_hash_end = {end} 

    while not open_set_start.empty() or not open_set_end.empty():

        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.QUIT
        
        cur_start = open_set_start.get()[2]
        open_set_hash_start.remove(cur_start)

        cur_end = open_set_end.get()[2]
        open_set_hash_end.remove(cur_end)


        if open_set_hash_start.__contains__(cur_end):
            reconstruct_path_double(draw, came_from_start, came_from_end, cur_end, start, end)
            return True
            

        for neighbor in cur_start.neighbors:
            g_score = g_score_start[cur_start] + 1

            if g_score < g_score_start[neighbor]:
                g_score_start[neighbor] = g_score
                f_score_start[neighbor] = g_score + h(neighbor.get_pos(), end.get_pos())
                came_from_start[neighbor] = cur_start

                if neighbor not in open_set_hash_start:
                    count_start += 1
                    open_set_hash_start.add(neighbor)
                    open_set_start.put((f_score_start[neighbor], count_start, neighbor))
                    neighbor.make_open_start()
                

        for neighbor in cur_end.neighbors:
            g_score = g_score_end[cur_end] + 1

            if g_score < g_score_end[neighbor]:
                g_score_end[neighbor] = g_score
                f_score_end[neighbor] = g_score + h(neighbor.get_pos(), start.get_pos())
                came_from_end[neighbor] = cur_end

                if neighbor not in open_set_hash_end:
                    count_end += 1
                    open_set_hash_end.add(neighbor)
                    open_set_end.put((f_score_end[neighbor], count_end, neighbor))
                    neighbor.make_open_end()
                
        draw()

        if cur_start != start:
            cur_start.make_closed_start()

        if cur_end != end:
            cur_end.make_closed_end()