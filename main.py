class defaultdict(dict):
    def __init__(self, datatype):
        self.__datatype = datatype
    def __missing__(self, key):
        value = self.__datatype()
        self[key] = value
        return value

class Sudoku(dict):
    def __init__(self):
        self |= {(i, j): {"possible": set(range(1, 10)), "locked": 0} for i in range(1, 10) for j in range(1, 10)}
        self.__boxes: list[list[tuple[int, int]]] = [[(i, j) for i in range(r, r + 3) for j in range(c, c + 3)] for r in [1, 4, 7] for c in [1, 4, 7]]
    
    def __longitude(self, x: int) -> set[tuple[int, int]]:
        return set((x, i) for i in range(1, 10))
    def __lattitude(self, x: int) -> set[tuple[int, int]]:
        return set((i, x) for i in range(1, 10))
    
    def __missing__(self, key: tuple[int, int]) -> Exception:
        raise Exception(f'Sudoku puzzle is a 9 * 9 grid, therefore "{key}" is not a valid grid square')
    
    def __setitem__(self, key: tuple[int, int], value: int):
        if 10 > value > 0:
            #We fix a key to a specific location
            self[key]['locked'] = value
            self[key]['possible'] = set()
            row, column = key
            
            #Find the box that key is located in
            for _ in self.__boxes:
                if key in _:
                    box: set[tuple[int, int]] = set(_)
                    break
            
            #Remove key from possible in row, column and box
            for _ in self.__longitude(row) | self.__lattitude(column) | box:
                self[_]['possible'] -= {value}
            
            #Find the grid coordinates of each item in each box
            for box in self.__boxes:
                addresses: defaultdict = defaultdict(list)
                for _ in box:
                    for item in self[_]['possible']:
                        addresses[item] += [_]
                
                for key, value in addresses.items():
                    #If an item in the box only has one possible location, it belongs there
                    if len(value) == 1:
                        self[value[0]] = key
                    else:
                        #If an item in the box is fixed to a certain row or column, then it does not belong to any other box in that row or column
                        rows, columns = set(), set()
                        for address in value:
                            rows.add(address[0])
                            columns.add(address[1])
                        if len(rows) == 1:
                            for _ in self.__longitude(rows.pop()) - set(box):
                                self[_]['possible'] -= {key}
                        if len(columns) == 1:
                            for _ in self.__lattitude(columns.pop()) - set(box):
                                self[_]['possible'] -= {key}
            
            #If an item in a row or column has only one possible location, it belongs there
            for i in range(1, 10):
                addresses: defaultdict = defaultdict(list)
                for _ in self.__longitude(i):
                    for item in self[_]['possible']:
                        addresses[item] += [_]
                for key, value in addresses.items():
                    if len(value) == 1:
                        self[value[0]] = key
                addresses: defaultdict = defaultdict(list)
                for  _ in self.__lattitude(i):
                    for item in self[_]['possible']:
                        addresses[item] += [_]
                for key, value in addresses.items():
                    if len(value) == 1:
                        self[value[0]] = key
            
            #If a specific location has only one possible key, then it belongs there
            for _ in self.keys():
                possible: list[set[int]] = self[_]['possible']
                if len(possible) == 1:
                    self[_] = possible.pop()
        else:
            raise Exception('Value must be 1-9')
    
    def solved(self) -> bool:
        numbers: set[int] = set(range(1, 10))
        for box in self.__boxes:
            items: set[int] = set()
            for address in box:
                items.add(self[address]['locked'])
            if numbers != items:
                return False
        for i in range(1, 10):
            items: set[int] = set()
            for address in self.__longitude(i):
                items.add(self[address]['locked'])
            if numbers != items:
                return False
            items: set[int] = set()
            for address in self.__lattitude(i):
                items.add(self[address]['locked'])
            if numbers != items:
                return False
        return True


if __name__ == '__main__':
    puzzle = Sudoku()
    puzzle[(1, 1)] = 1
    puzzle[(1, 4)] = 4
    puzzle[(1, 5)] = 6
    puzzle[(1, 9)] = 3
    puzzle[(2, 6)] = 7
    puzzle[(2, 8)] = 5
    puzzle[(2, 9)] = 1
    puzzle[(3, 6)] = 3
    puzzle[(3, 7)] = 6
    puzzle[(4, 2)] = 7
    puzzle[(4, 4)] = 2
    puzzle[(4, 7)] = 5
    puzzle[(5, 3)] = 2
    puzzle[(5, 7)] = 9
    puzzle[(6, 3)] = 5
    puzzle[(6, 6)] = 1
    puzzle[(6, 8)] = 6
    puzzle[(7, 3)] = 3
    puzzle[(7, 4)] = 7
    puzzle[(8, 1)] = 5
    puzzle[(8, 2)] = 9
    puzzle[(8, 4)] = 1
    puzzle[(9, 1)] = 8
    puzzle[(9, 5)] = 3
    puzzle[(9, 6)] = 5
    puzzle[(9, 9)] = 7

    # puzzle[(1, 3)] = 8

    grid = defaultdict(list)
    possible: dict = dict()
    print('Solved' if puzzle.solved() else 'Not solved')
    for key, value in puzzle.items():
        if not value['locked']:
            if len(value['possible']) == 0:
                raise Exception('Contradiction')
            else:
                possible[key] = value['possible']
        grid[key[0]] += [value['locked']]

    for key, value in possible.items():
        print(f'{key}: {value}')

    for key, value in grid.items():
        print(f'{key}: {value}')
