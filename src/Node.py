class Node:

    def __init__(self, n_id: int = 0, x: float = None, y: float = None):

        self.id = n_id
        self.weight = float('inf')
        self.x = x
        self.y = y
        self.edge_out = {}
        self.edge_in = {}
        self.father = None
        self.visited = False

    def __str__(self):
        return f'id: {self.id}, x: {self.x}, y: {self.y}.'

    def __lt__(self, other):
        return self.weight < other.weight
    #
    # def _repr_(self):
    #     return f'time: {self.time}, src: {self.src}, dst: {self.dst}, elev:{self.elev}, direction:{self.direction}.'
    #
    # def into_list(self):
    #     return ['Elevator call', f'{self.time}', f'{self.src}', f'{self.dst}', '0', f'{self.elev}']