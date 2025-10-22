#Sean Gor
#Assignment 3: Part 2 to find differences in path diagrams between using a Greedy algorithm or A* algorithm
import tkinter as tk
from queue import PriorityQueue
import math
class Cell:
    def __init__(self, x, y, is_wall=False):
        self.x, self.y = x, y
        self.is_wall = is_wall
        self.g = float("inf")
        self.h = 0.0
        self.f = float("inf")
        self.parent = None
    def __lt__(self, other):
        return (self.f, self.g) < (other.f, other.g)

class MazeGame:
    """One pane (canvas) for one strategy."""
    def __init__(self, parent, maze, title, strategy):
        self.strategy = strategy.upper()   # "GREEDY" or "ASTAR"
        self.title = title
        self.maze = maze

        self.rows, self.cols = len(maze), len(maze[0])
        self.agent_pos = (0, 0)
        self.goal_pos  = (self.rows - 1, self.cols - 1)

        self.cells = [[Cell(r, c, maze[r][c] == 1) for c in range(self.cols)] for r in range(self.rows)]

        # UI
        self.cell_size = 60
        frame = tk.Frame(parent)
        tk.Label(frame, text=title, font=("Helvetica", 14, "bold")).pack(pady=(6,2))
        self.canvas = tk.Canvas(frame, width=self.cols*self.cell_size, height=self.rows*self.cell_size, bg="white")
        self.canvas.pack()
        self.metrics = tk.Label(frame, text="", font=("Helvetica", 10))
        self.metrics.pack(pady=(4,10))
        frame.pack(side=tk.LEFT, padx=10, pady=10)

        # run
        self.draw_maze()
        expanded, path_len = self.find_path()
        self.metrics.config(text=f"nodes expanded: {expanded}   path length: {path_len}")

    # ---------- GUI ----------
    def draw_maze(self):
        for x in range(self.rows):
            for y in range(self.cols):
                color = 'maroon' if self.maze[x][y] == 1 else 'white'
                x0, y0 = y*self.cell_size, x*self.cell_size
                x1, y1 = x0+self.cell_size, y0+self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#ddd")
                if not self.cells[x][y].is_wall:
                    txt = f"g={self.cells[x][y].g}\nh={self.cells[x][y].h}"
                    self.canvas.create_text((y+0.5)*self.cell_size, (x+0.5)*self.cell_size,
                                            font=("Purisa", 11), text=txt)
        # start/goal outlines
        sx0, sy0 = self.agent_pos[1]*self.cell_size, self.agent_pos[0]*self.cell_size
        gx0, gy0 = self.goal_pos[1]*self.cell_size,  self.goal_pos[0]*self.cell_size
        self.canvas.create_rectangle(sx0, sy0, sx0+self.cell_size, sy0+self.cell_size, outline="green", width=3)
        self.canvas.create_rectangle(gx0, gy0, gx0+self.cell_size, gy0+self.cell_size, outline="blue",  width=3)

    # ---------- Search helpers ----------
    def heuristic(self, pos):
        # Using Euclidean Distance for this part
        return math.sqrt(math.pow(self.goal_pos[0] - pos[0], 2) + math.pow(self.goal_pos[1] - pos[1], 2))
    def reconstruct_path(self):
        cur = self.cells[self.goal_pos[0]][self.goal_pos[1]]
        if cur.parent is None and self.agent_pos != self.goal_pos:
            return 0
        length = 0
        while cur.parent:
            x, y = cur.x, cur.y
            x0, y0 = y*self.cell_size+6, x*self.cell_size+6
            x1, y1 = (y+1)*self.cell_size-6, (x+1)*self.cell_size-6
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="skyblue", outline="")
            txt = f"g={round(self.cells[x][y].g,2)}\nh={round(self.cells[x][y].h,2)}"
            self.canvas.create_text((y+0.5)*self.cell_size, (x+0.5)*self.cell_size,
                                    font=("Purisa", 11), text=txt)
            cur = cur.parent
            length += 1
        # show length at start
        self.canvas.create_text(0.5*self.cell_size, 0.5*self.cell_size,
                                font=("Purisa", 12), text=f"len={length}")
        return length

    # ----------(Greedy or A*) Search ----------
    def find_path(self):
        # reset cells
        for r in range(self.rows):
            for c in range(self.cols):
                v = self.cells[r][c]
                v.g = float("inf"); v.h = 0.0; v.f = float("inf"); v.parent = None

        start = self.cells[self.agent_pos[0]][self.agent_pos[1]]
        goal  = self.cells[self.goal_pos[0]][self.goal_pos[1]]

        start.g = 0.0
        start.h = self.heuristic(self.agent_pos)
        start.f = start.h if self.strategy == "GREEDY" else (start.g + start.h)

        pq = PriorityQueue()
        pq.put((start.f, start))
        in_open = {(start.x, start.y)}
        expanded = 0

        while not pq.empty():
            _, u = pq.get()
            in_open.discard((u.x, u.y))
            expanded += 1

            if u is goal:
                path_len = self.reconstruct_path()
                return expanded, path_len

            #include diagonal directions for this part since the Euclidean Distance is being used
            for dx, dy in ((0,1),(0,-1),(1,0),(-1,0), (1, -1), (-1, 1), (1, 1), (-1, -1)):
                nx, ny = u.x + dx, u.y + dy
                if not (0 <= nx < self.rows and 0 <= ny < self.cols): continue
                v = self.cells[nx][ny]
                if v.is_wall: continue

                tentative_g = u.g + 1.0
                h = self.heuristic((nx, ny))

                if self.strategy == "ASTAR":
                    if tentative_g < v.g:                       # relax on g
                        v.g = tentative_g
                        v.h = h
                        v.f = v.g + v.h
                        v.parent = u
                        if (nx, ny) not in in_open:
                            pq.put((v.f, v)); in_open.add((nx, ny))
                else:  # GREEDY
                    improved_g = False
                    if tentative_g < v.g:
                        v.g = tentative_g
                        improved_g = True
                    new_f = h                                   # f = h
                    if new_f < v.f or improved_g:
                        v.h = h
                        v.f = new_f
                        v.parent = u
                        if (nx, ny) not in in_open:
                            pq.put((v.f, v)); in_open.add((nx, ny))

        return expanded, 0  # no path

# --------------------- Maze ---------------------
maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0]
]

# ------------------------- App: two panes -----------------------------
root = tk.Tk()
root.title("Part 2: Greedy Best-First vs A* (side-by-side) with the Euclidean Heuristic")

left  = MazeGame(root, maze, "Greedy Best-First (f = h)", strategy="GREEDY")
right = MazeGame(root, maze, "A* (f = g + h)",            strategy="ASTAR")

root.mainloop()