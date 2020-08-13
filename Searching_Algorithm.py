import math
import os
import queue

# Breadth first search
def BFS(adjacency_list, begin, food_position):
    expand_nodes = []
    parent = []
    pathtoexit = []

    parent = []
    for i in range(len(adjacency_list)):
        parent.append(-1)
    if begin == food_position:
        return 0, expand_nodes, pathtoexit
    qu = queue.Queue()
    qu.put(begin)

    while (qu.empty() == False):
        current_n = qu.get()
        expand_nodes.append(current_n)

        for adjacency_node in adjacency_list[current_n]:
            if adjacency_node[0] not in expand_nodes:
                qu.put(adjacency_node[0])
                parent[adjacency_node[0]] = current_n
        
        if (current_n == food_position):
            while parent[current_n] != -1:
                pathtoexit.append(current_n)
                current_n = parent[current_n]
            pathtoexit.append(current_n)
            pathtoexit.reverse()
            esc_time = 0
            for l in  range(len(pathtoexit)):
                esc_time += l
            return esc_time, expand_nodes, pathtoexit
    return "", "", ""
# Depth First Search
def DFS(adjacency_list, begin, food_position):
    expand_nodes = []
    parent = []
    pathtoexit = []

    parent = []
    for i in range(len(adjacency_list)):
        parent.append(-1)
    if begin == food_position:
        return 0, expand_nodes, pathtoexit
    stack = []
    stack.append(begin)

    while (stack):
        current_n = stack.pop()
        expand_nodes.append(current_n)

        for adjacency_node in adjacency_list[current_n]:
            if adjacency_node[0] not in expand_nodes:
                stack.append(adjacency_node[0])
                parent[adjacency_node[0]] = current_n
        
        if (current_n == food_position):
            while parent[current_n] != -1:
                pathtoexit.append(current_n)
                current_n = parent[current_n]
            pathtoexit.append(current_n)
            pathtoexit.reverse()
            esc_time = 0
            for l in  range(len(pathtoexit)):
                esc_time += l
            return esc_time, expand_nodes, pathtoexit
    return "", "", ""      
### Iterative deepening search
# Depth-limited search
def DLS(adjacency_list, food_pos, explored, parent, current_path, depth):
    if current_path[-1] == food_pos:
        return True
    elif depth == 0: 
        return False
    
    for adjacency_node in adjacency_list[current_path[-1]]:
        if adjacency_node[0] not in current_path:
            parent[adjacency_node[0]] = current_path[-1]
            current_path.append(adjacency_node[0])
            explored.append(adjacency_node[0])
            result = DLS(adjacency_list, food_pos, explored, parent, current_path, depth - 1)
            if result == True:
                return True
            current_path.pop()
    return False
        

# Iterative deepning search
def IDS(adjacency_list, current_position, food_position, max_depth):
    explored_ns = [] # List of explored nodes
    path_fd = [] # List of nodes on the path found

    if current_position == food_position:
        return 0, explored_ns, path_fd

    for depth in range(max_depth - 1):
        parent = [-1] * len(adjacency_list)
        explored = [current_position]
        current_path = [current_position]
        result = DLS(adjacency_list, food_position, explored, parent, current_path, depth)
        explored_ns.append(explored)
        if result == True:
            cur_node = current_path[-1]
            while parent[cur_node] != -1:
                path_fd.append(cur_node)
                cur_node = parent[cur_node]
            path_fd.append(cur_node)
            path_fd.reverse()
            esc_time = 0
            for l in explored_ns:
                esc_time += len(l)
            return esc_time, explored_ns, path_fd

    return "", "", ""

#calculate the manhattan heuristic from current position to food position
def get_manhattan_heuristic(current_position, food_position, maze_size):    
    cur_x, cur_y = divmod(current_position, maze_size)    
    exit_x, exit_y = divmod(food_position, maze_size)    
    x_delta = abs(cur_x - exit_x)    
    y_delta = abs(cur_y - exit_y)    
    
    manhattan_dist = x_delta + y_delta    
    return manhattan_dist 

# A* Search
def A_Star(adjacency_list, current_position, food_position, maze_size):
    explored_nodes = []
    frontier = []
    p_found = []
    if current_position == food_position:
        return len(explored_nodes), explored_nodes, p_found, 0

    parent_list = [-1]*len(adjacency_list)
    frontier.append((0,current_position))

    while len(frontier) != 0:
        out_node = frontier.pop(0)
        node_fcost = out_node[0]    # cost
        node_value = out_node[1]    # index
        node_hcost = get_manhattan_heuristic(node_value, food_position, maze_size)
        node_gcost = node_fcost - node_hcost

        explored_nodes.append(node_value)

        if food_position == node_value:
            while parent_list[node_value] != -1:
                p_found.append(node_value)
                node_value = parent_list[node_value]
            p_found.append(node_value)
            p_found.reverse()            
            time_to_escape = len(explored_nodes)
            return time_to_escape, explored_nodes, p_found, node_fcost
        
        else:
            for node in adjacency_list[node_value]:
                if node[0] not in explored_nodes:
                    node_list = []
                    for i in frontier:
                        node_list.append(i[1])
                    if node[0] not in node_list:
                        if node[1] == 2:
                            frontier.append((node_gcost + 1 + get_manhattan_heuristic(node[0], food_position, maze_size) + 20, node[0]))
                        else:
                            frontier.append((node_gcost + 1 + get_manhattan_heuristic(node[0], food_position, maze_size) + node[0], node[0]))
                        parent_list[node[0]] = node_value
                        frontier.sort()
                    if node in node_list:
                        index = node_list.index(node)
                        cost = frontier[index][0]
                        if cost > node_gcost + 1 + get_manhattan_heuristic(frontier[index][1], food_position, maze_size):
                            frontier.pop(frontier[index])
                            if node[1] == 2:
                                frontier.append((node_gcost + 1 + get_manhattan_heuristic(node[0], food_position, maze_size) + 20, node[0]))
                            else:
                                frontier.append((node_gcost + 1 + get_manhattan_heuristic(node[0], food_position, maze_size) + node[0], node[0]))
                            frontier.sort()
                            parent_list[node[0]] = node_value
    return "", "", [], 0

def updateFrontier(front, tpl):
    for i in range(len(front)):
        if front[i][1] == tpl[1] and tpl[0] <= front[i][0]:
            front[i] = tpl
            return
    front.append(tpl)

def reverse_A_Star(adjacency_list, current_position, food_position, maze_size, ghost_list, food_list):

    flag = [False for _ in adjacency_list]
    visitedParent = [(i, i) for i in range(len(adjacency_list))]
    path = []
    frontier = []
    visitedList = []
    frontier.append((get_manhattan_heuristic(current_position, food_position, maze_size), current_position))

    visitedParent[current_position] = (current_position, -1)

    flag[current_position] = True

    while frontier[0][1] != food_position:
        node = frontier.pop(0)  
        # node = (cost, index)

        visitedList.append(node[1])
        flag[node[1]] = True

        for x in adjacency_list[node[1]]:
            # x = (index, type)
            fl = False
            for g in ghost_list:
                if g.index == x[0]:
                    fl = True
                    break 

            if not flag[x[0]] and not fl:

                fl = False
                for food in food_list:
                    if x[0] == food.index:
                        fl = True
                        break

                if fl: # food
                    updateFrontier(frontier, (20 + node[0], x[0]))
                else:
                    updateFrontier(frontier, (node[0] - 1, x[0]))
                visitedParent[x[0]] = (x[0], node[1])

        frontier.sort(key = lambda alpha:alpha[0], reverse = True)

        if len(frontier) == 0:
            return 0,[],[],0

    # pop goal node
    goal = frontier[0][1]
    visitedList.append(frontier[0][1])
    node = frontier.pop(0)

    fcost = node[0]

    while visitedParent[goal][1] != -1:
        path = [goal] + path
        goal = visitedParent[goal][1]

    #begin node
    path = [goal] + path

    return len(visitedList), visitedList, path, fcost


def swap (a, b):
    temp = a
    a = b
    b = temp