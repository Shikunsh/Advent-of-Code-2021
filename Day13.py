from typing import List, Tuple

class Dot:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, dot) -> bool:
        if isinstance(dot, self.__class__):
            for attr in self.__dict__.keys():
                if getattr(self, attr) != getattr(dot, attr):
                    return False
            return True
        else:
            raise TypeError('Comparison of a Dot object with other class objects is not supported.')
    
    def __hash__(self):
        return hash((self.x, self.y))

class Paper:
    
    def __init__(self, points, instructions):
        self.dots = [Dot(*point) for point in points]
        self.instructions = instructions
    
    def fold(self, attr, fpos):
        for dot in self.dots:
            pos = getattr(dot, attr)
            if pos > fpos:
                setattr(dot, attr, 2*fpos-pos)
                
    def count_visible_dots(self):
        return len(set(self.dots))

    def read_instructions(self) -> Tuple[str, int]:
        for instruction in self.instructions:
            self.fold(*instruction)
    
    def __str__(self):
        min_x, min_y, max_x, max_y = float('inf'), float('inf'), -float('inf'), -float('inf')
        for dot in set(self.dots):
            x, y = dot.x, dot.y
            min_x, min_y = min(min_x, x), min(min_y,y)
            max_x, max_y = max(max_x, x), max(max_y,y)
        m, n = max_x-min_x+1, max_y-min_y+1
        board = [[ '.' for x in range(m)] for y in range(n)]
        for dot in set(self.dots):
            x,y = dot.x-min_x, dot.y-min_y
            board[y][x] = '#'
        return '\n'.join([''.join(['{:2}'.format(item) for item in row]) for row in board])

if __name__ == '__main__':
    import os 
    with open(os.path.join(os.getcwd(),'inputs/D13_dots.txt'),'r') as fp:
        dots = fp.read().splitlines()
    dots = [list(map(int, dot.split(','))) for dot in dots]
    with open(os.path.join(os.getcwd(),'inputs/D13_instructions.txt'),'r') as fp:
        instructions = fp.read().splitlines()
    instructions = list(map(lambda x: [x[0],int(x[1])],[(line.split(' ')[-1]).split('=') for line in instructions]))

    paper = Paper(dots, instructions)
    paper.fold(*paper.instructions[0])
    print(paper.count_visible_dots())

    paper = Paper(dots, instructions)
    paper.read_instructions()
    print(paper)