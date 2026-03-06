import heapq

def a_star(grid, start, target):
    rows, cols = len(grid), len(grid[0])
    frontier = []
    start_t, target_t = tuple(start), tuple(target)
    heapq.heappush(frontier, (0, start_t))
    came_from = {start_t: None}
    cost_so_far = {start_t: 0}

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == target_t: break
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
                next_node = (nr, nc)
                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + abs(nr - target[0]) + abs(nc - target[1])
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current
    
    if target_t not in came_from: return None
    path, curr = [], target_t
    while curr:
        path.append(list(curr))
        curr = came_from[curr]
    return path[::-1]

def solve_route(grid, start, targets):
    full_path, curr_start = [], start
    for i, t in enumerate(targets):
        segment = a_star(grid, curr_start, t)
        if segment is None: return None
        full_path.extend(segment if i == 0 else segment[1:])
        curr_start = t
    return full_path
