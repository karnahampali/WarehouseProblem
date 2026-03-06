from collections import deque

def get_shortest_path(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(tuple(start), [tuple(start)])])
    visited = {tuple(start)}
    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == tuple(end): return path
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    return None

def solve_route(grid, start, targets):
    current_pos = tuple(start)
    remaining_targets = [tuple(t) for t in targets]
    full_path = [current_pos]
    total_steps = 0
    if not remaining_targets: return {"status": "error", "message": "No targets set"}
    for target in remaining_targets:
        path = get_shortest_path(grid, current_pos, target)
        if path is None: return {"status": "impossible", "message": "Impossible to approach target"}
        full_path.extend(path[1:])
        total_steps += len(path) - 1
        current_pos = target
    return {"status": "success", "total_steps": total_steps, "path": [list(p) for p in full_path], "targets_collected": len(targets)}