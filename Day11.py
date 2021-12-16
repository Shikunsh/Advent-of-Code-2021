from typing import List

class NeighborOctos:
    """
    non overriding descriptor so that the neighbor attribute is only calculated once.
    """
    directions = set([(i,j) if i != 0 or j != 0 else (1,0) for i in range(-1,2) for j in range(-1,2) ])
    
    def __get__(self, instance, _):
        neighbors = set()
        r,c = instance.row, instance.col
        octosmap = instance.octosmap
        for direction in self.directions:
            nr, nc = r+direction[0], c+direction[1]
            if octosmap.in_grid(nr,nc):
                neighbors.add(octosmap.octos[nr][nc])
        instance.__dict__['neighbors'] = neighbors
        return instance.neighbors

class Octo:
    
    neighbors = NeighborOctos()
    
    def __init__(self, row: int, col: int, energy: int, octos) -> None:
        self.energy = energy
        self.row = row
        self.col = col
        self.octosmap = octos
        
    def energize(self) -> None:
        self.energy += 1  
    
    def flash(self) -> None:
        for neighbor in self.neighbors:
            neighbor.energize()
    
    def reset(self) -> None:
        self.energy = 0
        
class DumboOctos:
    
    def __init__(self, octos: List[List[int]]) -> None:
        self.m = len(octos)
        self.n =len(octos[0])
        self.octos = [[ Octo(r, c, octos[r][c], self) for c in range(self.n)] for r in range(self.m)]
        self.flash_count = 0
        self.sync = False
        
    def in_grid(self, r: int, c:int) -> bool:
        if r >= 0 and r < self.m and c >= 0 and c < self.n:
            return True
        return False
    
    def find_next(self, flashed : List[Octo]=set()) -> set:
        return set([octo  for line in self.octos for octo in line if octo.energy>9 and octo not in flashed])

    def one_step(self) -> None:
        for line in self.octos:
            for octo in line:
                octo.energize()
        to_flash = self.find_next()
                
        flashed = set()
        while to_flash:
            for octo in to_flash:
                octo.flash()
                flashed.add(octo)
            to_flash = self.find_next(flashed)
        for octo in flashed:
            octo.reset()
        self.flash_count += len(flashed)
        self.sync = len(flashed) == self.m*self.n
            
                    
    def __str__(self):
        return str([[ octo.energy for octo in line ] for line in self.octos])


if __name__ == "__main__":
    import os
    input_path = os.path.join(os.getcwd(),'inputs/D11.txt')
    with open(input_path,'r') as fp:
        octos = fp.read().splitlines()
    octos = [[int(octo) for octo in line] for line in octos]
    
    #partone
    dumboctos = DumboOctos(octos)
    for i in range(100):
        dumboctos.one_step()
    print(dumboctos.flash_count)
    #parttwo
    dumboctos2 = DumboOctos(octos)
    step_counter = 0
    while not dumboctos2.sync:
        dumboctos2.one_step()
        step_counter += 1
    print(step_counter)