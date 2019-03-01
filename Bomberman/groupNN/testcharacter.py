# This is necessary to find the main code
import sys
import heapq
import math
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def empty(self):
        return len(self.queue) == 0

    def put(self, item, priority):
        heapq.heappush(self.queue, (priority, item))

    def get(self):
        return heapq.heappop(self.queue)[1]

# Node class for A* to keep track of score
class Node:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score


class TestCharacter1(CharacterEntity):

    # constructs a grid that is equivalent to the current world state
    def constructGrid(self, wrld):
        i = 0
        j = 0
        width = wrld.width()
        height = wrld.height()
        grid = [[0 for i in range(width)] for j in range(height)]

        while i < height:
            while j < width:
                if wrld.empty_at(j, i):
                    grid[i][j] = 0
                elif wrld.exit_at(j, i):
                    grid[i][j] = 1
                elif wrld.wall_at(j, i):
                    grid[i][j] = 2
                elif wrld.bomb_at(j, i):
                    grid[i][j] = 3
                elif wrld.explosion_at(j, i):
                    grid[i][j] = 4
                elif wrld.monsters_at(j, i):
                    grid[i][j] = 5
                elif wrld.characters_at(j, i):
                    grid[i][j] = 6
                j += 1
            j = 0
            i += 1
        return grid

    # prints out the given grid
    def printGrid(self, wrld, grid):
        i = 0
        j = 0
        width = wrld.width()
        height = wrld.height()

        while i < height:
            while j < width:
                print(grid[i][j], end='')
                j += 1
            j = 0
            i += 1
            print("\n")

    # checks for type of cell in surrounding, giving the list direction tuples as a return
    # type 1 is exit
    # type 2 is monster
    # checks for type of cell in surrounding
    # checks for type of cell in surrounding

    def check_surroundings(self, wrld, thisx, thisy):
        # First check if exit is 1 move away\
        finds = dict([(i, []) for i in range(7)])

        for dx in [-1, 0, 1]:

            x = thisx + dx

            # Avoid out-of-bound indexing
            if (x >= 0) and (x < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    y = thisy + dy
                    # Skip current cell
                    if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                        if (y >= 0) and (y < wrld.height()):
                            # Check cases
                            if (wrld.empty_at(x, y)):
                                ls = finds[0]
                                ls.append((dx, dy))
                                finds[0] = ls
                            elif (wrld.exit_at(x, y)):
                                ls = finds[1]

                                ls.append((dx, dy))
                                finds[1] = ls
                            elif (wrld.wall_at(x, y)):
                                ls = finds[2]
                                ls.append((dx, dy))

                                ls.append((dx, dy))
                                finds[1] = ls
                            elif (wrld.wall_at(x, y)):
                                ls = finds[2]
                                ls.append((dx, dy))
                                finds[2] = ls
                            elif (wrld.bomb_at(x, y)):
                                ls = finds[3]
                                ls.append((dx, dy))
                                finds[3] = ls
                            elif (wrld.explosion_at(x, y)):
                                ls = finds[4]
                                ls.append((dx, dy))
                                finds[4] = ls
                            elif (wrld.monsters_at(x, y)):
                                ls = finds[5]
                                ls.append((dx, dy))
                                finds[5] = ls
                            elif (wrld.characters_at(x, y)):
                                ls = finds[6]
                                ls.append((dx, dy))
                                finds[6] = ls
        return finds

    # returns nodes surrounding the current position of the character
    def get_neighbors(self, wrld, thisx, thisy):
        # First check if exit is 1 move away\
        finds = [Node(-1, -1, -1)] * 8
        count = 0
        danger = 0
        monsterLoc = self.find_monsters(wrld)

        for dx in [-1, 0, 1]:
            x = thisx + dx
            # Avoid out-of-bound indexing
            if (x >= 0) and (x < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    y = thisy + dy
                    # Skip current cell
                    if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                        if (y >= 0) and (y < wrld.height()):
                            for pos in monsterLoc:
                                coord = pos[0], pos[1]
                                currentcoord = wrld.me(self).x, wrld.me(self).y
                                dist = abs(self.manhattan_distance(coord, currentcoord))
                                if dist <= 4:
                                    print("DANGER", dist)
                                    danger = True

                            if danger:
                                finds[count] = (Node(x, y, 100))
                            elif wrld.empty_at(x, y):
                                finds[count] = (Node(x, y, 1))
                            elif wrld.exit_at(x, y):
                                finds[count] = (Node(x, y, 1))
                            elif wrld.wall_at(x, y):
                                finds[count] = (Node(x, y, 100))
                            elif wrld.bomb_at(x, y):
                                finds[count] = (Node(x, y, 300))
                            elif wrld.explosion_at(x, y):
                                finds[count] = (Node(x, y, 300))
                            elif wrld.monsters_at(x, y):
                                finds[count] = (Node(x, y, 100))
                            elif wrld.characters_at(x, y):
                                finds[count] = (Node(x, y, 1))
                            count += 1
                            danger = False
        return finds

    # Manhattan distance
    def manhattan_distance(self, x1y1, x2y2):
        return abs(x1y1[0] - x2y2[0]) + abs(x1y1[1] - x2y2[1])

    # returns a tuple of the exit. If no exit is found returns (0,0)
    def find_exit(self, wrld):
        w = 0
        h = 0

        while w < wrld.width():
            while h < wrld.height():
                if wrld.exit_at(w, h):
                    return w, h
                h += 1
            w += 1
            h = 0
        return 0, 0

    # heuristic function for A*
    def heuristic(self, a, b):
        (x1, y1) = a[0], a[1]
        (x2, y2) = b[0], b[1]
        return abs(x1 - x2) + abs(y1 - y2)

    # A* implementation
    def astar(self, wrld, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)

        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current[0] == -1 or current[1] == -1:
                continue

            if current == goal:
                break

            # just finished making the check get_neighbors, now time to change this part to the new method and make it work
            i = 0
            neighbors = self.get_neighbors(wrld, current[0], current[1])

            for node in neighbors:
                new_cost = cost_so_far[current] + node.score
                if node.x == -1 or node.y == -1:
                    continue
                if (node.x, node.y) not in cost_so_far or new_cost < cost_so_far[(node.x, node.y)]:
                    cost_so_far[(node.x, node.y)] = new_cost
                    priority = new_cost + self.heuristic(goal, current)
                    frontier.put((node.x, node.y), priority)
                    came_from[(node.x, node.y)] = current
                i += 1

        path = came_from, cost_so_far
        newpath = self.make_sense_of_path(path, start, goal)
        return newpath

    # returns the path from goal node to start node
    def make_sense_of_path(self, path, start, goal):
        current = path[0][goal]
        newpath = [goal]

        while current != start:
            newpath.append(current)
            current = path[0][current]

        return newpath

    def getMove(self, path, wrld):
        pathLength = len(path) - 1
        nextMove = path[pathLength]

        newMove = nextMove[0] - wrld.me(self).x, nextMove[1] - wrld.me(self).y

        return newMove

    def get_safe_moves(self, wrld, surroundings, me):
        ww = wrld.width()
        wh = wrld.height()
        safe = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if me.x + dx in range(0, ww) and me.y in range(0, wh):
                    safe.append((dx, dy))
        # Bomb, monster, explosion and character check
        if wrld.bomb_at(me.x, me.y):
            safe.remove((0, 0))
        for dir in surroundings[3]:
            safe.remove(dir)
        for dir in surroundings[4]:
            safe.remove(dir)
        for dir in surroundings[5]:
            safe.remove(dir)
        for dir in surroundings[6]:
            safe.remove(dir)
        # Check for bomb range
        bomb_range = wrld.expl_range
        for (dx, dy) in safe:
            # x direction
            for i in range(-bomb_range, bomb_range + 1):
                if i != 0 and me.x + i in range(0, wrld.width()) and wrld.bomb_at(me.x + i, me.y):
                    safe.remove((dx, dy))
                    break
        for (dx, dy) in safe:
            # y direction
            for j in range(-bomb_range, bomb_range + 1):
                if j != 0 and me.y + j in range(0, wrld.height()) and wrld.bomb_at(me.x, me.y + j):
                    safe.remove((dx, dy))
                    break;

        # Check cells near monster
        monst_range = 2
        for (dx, dy) in safe:
            for i in range(-monst_range, monst_range + 1):
                for j in range(-monst_range, monst_range + 1):
                    check_x = me.x + dx + i
                    check_y = me.y + dy + j
                    if check_x > 0 and check_x < wrld.width() and check_x != me.x:
                        if check_y > 0 and check_y < wrld.height() and check_y != me.y:
                            if wrld.monsters_at(check_x, check_y):
                                safe.remove((dx, dy))
        return safe

    def getSafe(self, wrld, x, y):
        unsafe = []
        safe = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                current = (dx, dy)
                if x + dx < wrld.width() and y + dy < wrld.height():
                    if wrld.wall_at(x + dx, y + dy):
                        if current in safe:
                            unsafe.append(current)
                            safe.remove(current)
                # check for monsters
                for i in range(-3, 3):
                    for j in range(-3, 3):
                        if x + dx + i < wrld.width():
                            if y + dy + j < wrld.height():
                                if wrld.monsters_at(x + dx + i, y + dy + j) and i in range(-2, 2) and j in range(-2, 2):
                                    if current in safe:
                                        unsafe.append(current)
                                        safe.remove(current)
                                if wrld.bomb_at(x + dx + i, y + dy + j) and i in range(-3, 3) and j in range(-3, 3):
                                    if current in safe:
                                        unsafe.append(current)
                                        safe.remove(current)
                                if wrld.explosion_at(x + dx + i, y + dy + j) and i in range(-1, 1) and j in range(-1,
                                                                                                                  1):
                                    if current in safe:
                                        unsafe.append(current)
                                        safe.remove(current)

        return safe

    def find_monsters(self, wrld):
        i = 0
        j = 0
        monsterpos = []

        while i < wrld.width():
            while j < wrld.height():
                if wrld.monsters_at(i, j):
                    monster = (i, j)
                    monsterpos.append(monster)
                j += 1
            i += 1
            j = 0
        return monsterpos

    def monsterNear(self, wrld, x, y):

        for r in range(-4, 4):
            for c in range(-4, 4):
                if r + x < wrld.width():
                    if y + c < wrld.height():
                        if wrld.monsters_at(r + x, y + c):
                            return True
        return False

    def do(self, wrld):
        # Your code here

        me = wrld.me(self)
        currentQValue = 0
        newQValue = 0
        bestQValue = 0
        bestQMove = (0, 0)

        surroundings = self.check_surroundings(wrld, me.x, me.y)
        # First check if exit is 1 move away
        if len(surroundings[1]) > 0:
            self.move(surroundings[1][0][0], surroundings[1][0][1])
        start = me.x, me.y
        goal = self.find_exit(wrld)
        safe_moves = self.get_safe_moves(wrld, surroundings, me)

        path = self.astar(wrld, start, goal)
        move = self.getMove(path, wrld)

        self.move(move[0], move[1])


class TestCharacter2(CharacterEntity):

    # constructs a grid that is equivalent to the current world state
    def constructGrid(self, wrld):
        i = 0
        j = 0
        width = wrld.width()
        height = wrld.height()
        grid = [[0 for i in range(width)] for j in range(height)]

        while i < height:
            while j < width:
                if wrld.empty_at(j, i):
                    grid[i][j] = 0
                elif wrld.exit_at(j, i):
                    grid[i][j] = 1
                elif wrld.wall_at(j, i):
                    grid[i][j] = 2
                elif wrld.bomb_at(j, i):
                    grid[i][j] = 3
                elif wrld.explosion_at(j, i):
                    grid[i][j] = 4
                elif wrld.monsters_at(j, i):
                    grid[i][j] = 5
                elif wrld.characters_at(j, i):
                    grid[i][j] = 6
                j += 1
            j = 0
            i += 1
        return grid

    # prints out the given grid
    def printGrid(self, wrld, grid):
        i = 0
        j = 0
        width = wrld.width()
        height = wrld.height()

        while i < height:
            while j < width:
                print(grid[i][j], end='')
                j += 1
            j = 0
            i += 1
            print("\n")

    # checks for type of cell in surrounding, giving the list direction tuples as a return
    # type 1 is exit
    # type 2 is monster
    # checks for type of cell in surrounding
    # checks for type of cell in surrounding

    def check_surroundings(self, wrld, thisx, thisy):
        # First check if exit is 1 move away\
        finds = dict([(i, []) for i in range(7)])

        for dx in [-1, 0, 1]:

            x = thisx + dx

            # Avoid out-of-bound indexing
            if (x >= 0) and (x < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    y = thisy + dy
                    # Skip current cell
                    if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                        if (y >= 0) and (y < wrld.height()):
                            # Check cases
                            if (wrld.empty_at(x, y)):
                                ls = finds[0]
                                ls.append((dx, dy))
                                finds[0] = ls
                            elif (wrld.exit_at(x, y)):
                                ls = finds[1]
                                ls.append((dx, dy))
                                finds[1] = ls
                            elif (wrld.wall_at(x, y)):
                                ls = finds[2]
                                ls.append((dx, dy))
                                finds[2] = ls
                            elif (wrld.bomb_at(x, y)):
                                ls = finds[3]
                                ls.append((dx, dy))
                                finds[3] = ls
                            elif (wrld.explosion_at(x, y)):
                                ls = finds[4]
                                ls.append((dx, dy))
                                finds[4] = ls
                            elif (wrld.monsters_at(x, y)):
                                ls = finds[5]
                                ls.append((dx, dy))
                                finds[5] = ls
                            elif (wrld.characters_at(x, y)):
                                ls = finds[6]
                                ls.append((dx, dy))
                                finds[6] = ls
        return finds

    # returns nodes surrounding the current position of the character
    def get_neighbors(self, wrld, thisx, thisy):
        # First check if exit is 1 move away\
        finds = [Node(-1, -1, -1)] * 8
        count = 0
        danger = 0
        monsterLoc = self.find_monsters(wrld)

        for dx in [-1, 0, 1]:
            x = thisx + dx
            # Avoid out-of-bound indexing
            if (x >= 0) and (x < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    y = thisy + dy
                    # Skip current cell
                    if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                        if (y >= 0) and (y < wrld.height()):
                            for pos in monsterLoc:
                                coord = pos[0], pos[1]
                                currentcoord = wrld.me(self).x, wrld.me(self).y
                                dist = abs(self.manhattan_distance(coord, currentcoord))
                                if dist <= 4:
                                    print("DANGER", dist)
                                    danger = True

                            if danger:
                                finds[count] = (Node(x, y, 100))
                            elif wrld.empty_at(x, y):
                                finds[count] = (Node(x, y, 1))
                            elif wrld.exit_at(x, y):
                                finds[count] = (Node(x, y, 1))
                            elif wrld.wall_at(x, y):
                                finds[count] = (Node(x, y, 100))
                            elif wrld.bomb_at(x, y):
                                finds[count] = (Node(x, y, 300))
                            elif wrld.explosion_at(x, y):
                                finds[count] = (Node(x, y, 300))
                            elif wrld.monsters_at(x, y):
                                finds[count] = (Node(x, y, 100))
                            elif wrld.characters_at(x, y):
                                finds[count] = (Node(x, y, 1))
                            count += 1
                            danger = False
        return finds

    # Manhattan distance
    def manhattan_distance(self, x1y1, x2y2):
        return abs(x1y1[0] - x2y2[0]) + abs(x1y1[1] - x2y2[1])

    # returns a tuple of the exit. If no exit is found returns (0,0)
    def find_exit(self, wrld):
        w = 0
        h = 0

        while w < wrld.width():
            while h < wrld.height():
                if wrld.exit_at(w, h):
                    return w, h
                h += 1
            w += 1
            h = 0
        return 0, 0

    # heuristic function for A*
    def heuristic(self, a, b):
        (x1, y1) = a[0], a[1]
        (x2, y2) = b[0], b[1]
        return abs(x1 - x2) + abs(y1 - y2)

    # A* implementation
    def astar(self, wrld, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)

        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current[0] == -1 or current[1] == -1:
                continue

            if current == goal:
                break

            # just finished making the check get_neighbors, now time to change this part to the new method and make it work
            i = 0
            neighbors = self.get_neighbors(wrld, current[0], current[1])

            for node in neighbors:
                new_cost = cost_so_far[current] + node.score
                if node.x == -1 or node.y == -1:
                    continue
                if (node.x, node.y) not in cost_so_far or new_cost < cost_so_far[(node.x, node.y)]:
                    cost_so_far[(node.x, node.y)] = new_cost
                    priority = new_cost + self.heuristic(goal, current)
                    frontier.put((node.x, node.y), priority)
                    came_from[(node.x, node.y)] = current
                i += 1

        path = came_from, cost_so_far
        newpath = self.make_sense_of_path(path, start, goal)
        return newpath

    # returns the path from goal node to start node
    def make_sense_of_path(self, path, start, goal):
        current = path[0][goal]
        newpath = [goal]

        while current != start:
            newpath.append(current)
            current = path[0][current]

        return newpath

    def getMove(self, path, wrld):
        pathLength = len(path) - 1
        nextMove = path[pathLength]

        newMove = nextMove[0] - wrld.me(self).x, nextMove[1] - wrld.me(self).y

        return newMove

    def get_safe_moves(self, wrld, surroundings, me):
        ww = wrld.width()
        wh = wrld.height()
        safe = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if me.x + dx in range(0, ww) and me.y in range(0, wh):
                    safe.append((dx, dy))
        # Bomb, monster, explosion and character check
        if wrld.bomb_at(me.x, me.y):
            safe.remove((0, 0))
        for dir in surroundings[3]:
            safe.remove(dir)
        for dir in surroundings[4]:
            safe.remove(dir)
        for dir in surroundings[5]:
            safe.remove(dir)
        for dir in surroundings[6]:
            safe.remove(dir)
        # Check for bomb range
        bomb_range = wrld.expl_range
        for (dx, dy) in safe:
            # x direction
            for i in range(-bomb_range, bomb_range + 1):
                if i != 0 and me.x + i in range(0, wrld.width()) and wrld.bomb_at(me.x + i, me.y):
                    safe.remove((dx, dy))
                    break
        for (dx, dy) in safe:
            # y direction
            for j in range(-bomb_range, bomb_range + 1):
                if j != 0 and me.y + j in range(0, wrld.height()) and wrld.bomb_at(me.x, me.y + j):
                    safe.remove((dx, dy))
                    break;

        # Check cells near monster
        monst_range = 2
        for (dx, dy) in safe:
            for i in range(-monst_range, monst_range + 1):
                for j in range(-monst_range, monst_range + 1):
                    check_x = me.x + dx + i
                    check_y = me.y + dy + j
                    if check_x > 0 and check_x < wrld.width() and check_x != me.x:
                        if check_y > 0 and check_y < wrld.height() and check_y != me.y:
                            if wrld.monsters_at(check_x, check_y):
                                safe.remove((dx, dy))
        return safe

    def getSafe(self, wrld, x, y):
        unsafe = []
        safe = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                current = (dx, dy)
                if x + dx < wrld.width() and y + dy < wrld.height():
                    if wrld.wall_at(x + dx, y + dy):
                        if current in safe:
                            unsafe.append(current)
                            safe.remove(current)
                # check for monsters
                for i in range(-3, 3):
                    for j in range(-3, 3):
                        if x + dx + i < wrld.width():
                            if y + dy + j < wrld.height():
                                if wrld.monsters_at(x + dx + i, y + dy + j) and i in range(-2, 2) and j in range(-2, 2):
                                    if current in safe:
                                        unsafe.append(current)
                                        safe.remove(current)
                                if wrld.bomb_at(x + dx + i, y + dy + j) and i in range(-3, 3) and j in range(-3, 3):
                                    if current in safe:
                                        unsafe.append(current)
                                        safe.remove(current)
                                if wrld.explosion_at(x + dx + i, y + dy + j) and i in range(-1, 1) and j in range(-1,
                                                                                                                  1):
                                    if current in safe:
                                        unsafe.append(current)
                                        safe.remove(current)

        return safe

    def ft_monster_distance(self, wrld, x, y):
        closestMonster = -1
        i = 0
        monsters = self.find_monsters(wrld)
        for pos in monsters:
            current = abs(pos[0] - x) + abs(pos[1] - y)
            if current < closestMonster or closestMonster == -1:
                closestMonster = current

        if closestMonster == -1:
            return 0

        return 1 / (1 + closestMonster)

    def find_monsters(self, wrld):
        i = 0
        j = 0
        monsterpos = []

        while i < wrld.width():
            while j < wrld.height():
                if wrld.monsters_at(i, j):
                    monster = (i, j)
                    monsterpos.append(monster)
                j += 1
            i += 1
            j = 0
        return monsterpos

    def monsterNear(self, wrld, x, y):

        for r in range(-4, 4):
            for c in range(-4, 4):
                if r + x < wrld.width():
                    if y + c < wrld.height():
                        if wrld.monsters_at(r + x, y + c):
                            return True
        return False

    def do(self, wrld):
        # Your code here

        me = wrld.me(self)
        currentQValue = 0
        newQValue = 0
        bestQValue = 0
        bestQMove = (0, 0)

        surroundings = self.check_surroundings(wrld, me.x, me.y)
        # First check if exit is 1 move away
        if len(surroundings[1]) > 0:
            self.move(surroundings[1][0][0], surroundings[1][0][1])
        start = me.x, me.y
        goal = self.find_exit(wrld)
        safe_moves = self.get_safe_moves(wrld, surroundings, me)

        path = self.astar(wrld, start, goal)
        move = self.getMove(path, wrld)

        if_bomb_goal = 1, 1
        if_bomb_path = self.astar(wrld, start, if_bomb_goal)
        if_bomb_move = self.getMove(if_bomb_path, wrld)

        bomb = False
        for i in range(0, wrld.width()):
            for j in range(0, wrld.height()):
                if wrld.bomb_at(i,j) or wrld.explosion_at(i,j) is not None:
                    bomb = True
        if bomb == True and not wrld.bomb_at(me.x, me.y):
            self.move(0,0)
            # self.move(if_bomb_move[0], if_bomb_move[1])
        elif wrld.wall_at(me.x+move[0], me.y+move[1]):
            self.place_bomb()
            best_so_far = (-1,-1)
            best_run_so_far = 1000
            for dx in [-1, 1]:
                for dy in [-1, 1]:
                    if me.x+dx in range(0, wrld.width()):
                        if me.y+ dy in range(0, wrld.height()):
                            wrld.me(self).move(dx,dy)
                            w2, ev = wrld.next()
                            dist = self.ft_monster_distance(w2,me.x+dx, me.y+ dy)
                            if best_run_so_far < dist:
                                best_run_so_far = dist
                                best_so_far = (dx,dy)
                                print("this is the move")
            self.move(best_so_far[0],best_so_far[1])
        else:
            self.move(move[0], move[1])
