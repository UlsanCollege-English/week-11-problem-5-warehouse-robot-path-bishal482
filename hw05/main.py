from collections import deque

def parse_grid(lines: list) -> tuple:
    """
    Parses a grid of strings into an adjacency list graph,
    identifies the start (S) and target (T) coordinates.

    :param lines: List of strings representing the grid.
    :return: (graph: dict, start_coord: str, target_coord: str)
    """
    R = len(lines)
    C = len(lines[0])
    
    graph = {}
    start_coord = None
    target_coord = None
    
    # Define movement directions (Up, Down, Left, Right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for r in range(R):
        for c in range(C):
            cell = lines[r][c]
            coord = f"{r},{c}"
            
            if cell == '#':
                continue # Blocked cells are not added as keys to the graph
            
            if cell == 'S':
                start_coord = coord
            elif cell == 'T':
                target_coord = coord
            
            # Build adjacency list for open cells (S, T, or .)
            neighbors = []
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                # Check boundaries
                if 0 <= nr < R and 0 <= nc < C:
                    neighbor_cell = lines[nr][nc]
                    if neighbor_cell != '#':
                        neighbors.append(f"{nr},{nc}")
            
            if neighbors:
                graph[coord] = neighbors
                
    return graph, start_coord, target_coord


def grid_shortest_path(lines: list) -> list or None:
    """
    Finds the shortest path from 'S' to 'T' in the grid using BFS.

    :param lines: List of strings representing the grid.
    :return: List of coordinates (strings) for the shortest path, or None.
    """
    graph, start_node, target_node = parse_grid(lines)

    if start_node is None or target_node is None:
        # Should not happen based on typical test structure, but good practice
        return None 
    
    # Handle the trivial case: S = T (Test: test_start_equals_target)
    if start_node == target_node:
        return [start_node]
    
    # Check if the start or target node exists in the graph (i.e., isn't blocked)
    if start_node not in graph and lines[0][0] != 'S': # Handle case like S#T where S is blocked
        return None

    # --- BFS Implementation ---
    
    # Queue for BFS (stores the node to visit)
    queue = deque([start_node])
    
    # Dictionary to store the parent of each node to reconstruct the path
    # {child_node: parent_node}
    parent = {start_node: None}
    
    while queue:
        u = queue.popleft()

        # Iterate over neighbors
        for v in graph.get(u, []):
            if v not in parent:
                parent[v] = u
                
                if v == target_node:
                    # Target found! Reconstruct the path.
                    path = []
                    curr = target_node
                    while curr is not None:
                        path.append(curr)
                        curr = parent.get(curr)
                    
                    path.reverse()
                    return path
                
                queue.append(v)

    # If the queue empties without finding the target
    return None