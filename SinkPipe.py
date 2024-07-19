Debug = False
Debug_grid = False

def sinks_connected_to_source(file_path):
    import os
    
    # Read input file
    rows = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split()
            if len(parts) == 3:
                rows.append((parts[0], int(parts[1]), int(parts[2])))
    
    # Get grid dimensions
    max_x = max(obj[1] for obj in rows) + 1
    max_y = max(obj[2] for obj in rows) + 1
    
    # print(rows)
    if Debug:
        print('max_x=',max_x)
        print('max_y=',max_y)

    # grid to store the pipes
    grid = [[' ' for _ in range(max_y)] for _ in range(max_x)]
    
    # Save row data to grid
    source_pos = ' '
    sinks = []
    
    for obj, x, y in rows:
        if obj == '*':
            source_pos = (x, y)
            grid[x][y] = obj
        elif obj.isalpha():
            sinks.append((obj, x, y))
            grid[x][y] = obj
        else:
            grid[x][y] = obj
    
    if Debug:
        print('source_pos=',source_pos)
        print('sinks=',sinks)
        # print('grid=',grid)
    
    if Debug_grid:
        print('  :', end=' ')
        for x in (range(max_x)):
            print(x % 10, end=' ')
        print()
        for y in (reversed(range(max_y))):
            if y < 10: print(' ', end='')
            print(y, end=': ')
            for x in (range(max_x)):
                print(grid[x][y], end=' ')
            print()
    
    # directions for the pipes
    directions = {
        '═': ['E', 'W'],
        '║': ['N', 'S'],
        '╔': ['E', 'S'],
        '╗': ['W', 'S'],
        '╚': ['E', 'N'],
        '╝': ['W', 'N'],
        '╠': ['E', 'N', 'S'],
        '╣': ['W', 'N', 'S'],
        '╦': ['W', 'E', 'S'],
        '╩': ['E', 'N', 'W'],
        ' ': [],
        '*': ['N', 'S', 'E', 'W'],
    }
    
    # function to identify sinks that are connected to the source
    def get_sinks(x, y):
        to_visit = [(x, y)]
        sinks = set()
        if Debug: print(to_visit)
        
        while to_visit:
            cx, cy = to_visit.pop()
            
            if Debug:
                print('\nPopped (cx,cy)=(',cx,',', cy,')')
                print('grid[cx][cy]=',grid[cx][cy])
            
            this_cell = grid[cx][cy]
            # Mark this cell as visited
            grid[cx][cy] = ' '
            
            # Check all four directions
            for direction in ['N', 'S', 'E', 'W']:
                if Debug: print('direction: ', direction)
                nx, ny = cx, cy
                if direction == 'N':
                    this_direction = 'S'
                    ny -= 1
                elif direction == 'S':
                    this_direction = 'N'
                    ny += 1
                elif direction == 'E':
                    this_direction = 'W'
                    nx -= 1
                elif direction == 'W':
                    this_direction = 'E'
                    nx += 1
                
                if 0 <= nx < max_x and 0 <= ny < max_y:
                    
                    if Debug:
                        print('(nx,ny)=(',nx,',', ny,')')
                        print('grid[nx][ny]=',grid[nx][ny])
                
                    if grid[nx][ny] != ' ':
                        if grid[nx][ny] == '*':
                            sinks.add('*')
                        elif grid[nx][ny].isalpha():
                            sinks.add(grid[nx][ny])
                        else:
                            if Debug: print('this_direction=', this_direction, 'this_cell=', this_cell)
                            if (this_direction in directions[this_cell]) and (direction in directions[grid[nx][ny]]):
                                # if Debug: print('direction=',direction,', directions=',directions[grid[nx][ny]],' appending...')
                                to_visit.append((nx, ny))
        
        return sinks
    
    # from the source identify all connected sinks
    if source_pos:
        sinks = get_sinks(source_pos[0], source_pos[1])
    else:
        sinks = set()
    
    # Return result, sorted string of sink labels
    result = ''.join(sorted(sinks - {'*'}))
    return result


#
result = sinks_connected_to_source('coding_qual_input.txt')
print(result)
