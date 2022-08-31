import math
from ar.constants import STAIRS_DOWN_DIR, STAIRS_UP_DIR
from wayfinding.rooms import Node, Room, get_nodes, get_rooms

NO_NODE = '-'

class Path:
    ''' class that describes the path, using the names of the nodes
    and the directions to get to the destination'''
    nodes = []
    directions = []

    def __init__(self, nodes, directions):
        self.nodes = nodes
        self.directions = directions

    def get_last_node(self):
        '''gets the last node'''
        return self.nodes[-1:][0]

    def get_penultimate_node(self):
        return self.nodes[-2:][0]

    def get_nodes(self):
        return self.nodes

    def get_directions(self):
        return self.directions

    def print(self):
        for node in self.nodes:
            print("Node " + node.name)
        
        print('######')
        for dir in self.directions:
            print("Direction " + str(dir))


def find_node_with_name(node_name):
    """ finds a node or room instance accordning to its name"""
    rooms = get_rooms()
    nodes = get_nodes()
    found_node = None
    for node in nodes:
        if node.name == node_name:
            found_node = node
    if found_node is None:
        for room in rooms:
            if room.name == node_name:
                found_node = room
    if found_node is None:
        return None
    else:
        return found_node

def bfs(start_node_name, dest_node_name):
    ''' calculates the path from startnode to end node with breadth first search'''
    visited = []
    start_node = find_node_with_name(start_node_name)
    dest_node = find_node_with_name(dest_node_name)

    if start_node is None or dest_node is None:
        print("One of these nodes " + start_node_name + "or " + dest_node_name + " does not exist")
        return None
    frontier = [Path([start_node], [])] #Frontier contains paths, not nodes

    #bfs frontier is a queue fifo, new elements last
    while len(frontier) > 0:
        path = frontier[0]
        frontier = frontier[1:] 

        if path.get_last_node().name == dest_node.name:
            return path
        visited.append(path.get_last_node().name)
        for neighbor_node_name, direction in Node.get_neighbors_as_list(path.get_last_node()):

            if  not neighbor_node_name is NO_NODE and not neighbor_node_name in visited:
                neighbor_node = find_node_with_name(neighbor_node_name)
                if not neighbor_node is None: 
                    frontier.append(Path(nodes=path.nodes + [neighbor_node],
                                    directions=path.get_directions() + [direction]))
            
    print("No Path could be found")
    frontier = []
    return None

def find_path(start_node, end_node):
    ''' uses breadth first search for path finding'''
    return bfs(start_node, end_node)

def calc_distance_to_end_of_hallway(node_name, looking_dir):
    ''' calculates the distance to the end of the hallway according the 
    users looking direction'''
    start_node = find_node_with_name(node_name)
    dir_idx = int(looking_dir) # used as index

    current_node = start_node
    dist = 0
    
    while current_node.get_neighbors_in_dir(dir_idx) != [] and current_node.get_neighbors_in_dir(dir_idx)[0] != NO_NODE:
        # is exactly one node in that direction, 
        # because it cant be a room (or multiple) since the
        # user is in a hallway and in looking direction there are no rooms
        # only left and right
        current_node = find_node_with_name(current_node.get_neighbors_in_dir(dir_idx)[0])
        dist += 1

    return dist


def calc_distance_to_door_if_visible(node_name, room_name, looking_dir):
    '''calculates the distance to the door if the door is in the same hallway in the
    direction the user looks (looking_dir)
    returns inf if the door is not visible
    '''
    start_node = find_node_with_name(node_name)

    current_node = start_node
    looking_dir = int(looking_dir)
    
    dist = 0
    while current_node.get_neighbors_in_dir(looking_dir) !=  [] and current_node.get_neighbors_in_dir(looking_dir)[0] != NO_NODE:
        for neighbor in current_node.get_neighbors_as_list():
            if neighbor[0] == room_name:
                return dist
        # going in looking dir means only one neighbor
        current_node = find_node_with_name(current_node.get_neighbors_in_dir(looking_dir)[0])
        dist += 1
    return math.inf


def calc_stairs_up_or_down(path):
    ''' Calculates if the next switch of the floor is up or down '''
    current_floor = int(path.nodes[0].name[1])
    i = 0
    while int(path.nodes[i].name[1]) == current_floor:
        i += 1

    if len(path.nodes) > i + 1:
        next_floor = int(path.nodes[i+1].name[1])

        if next_floor > current_floor: 
            return STAIRS_UP_DIR
        else:
            return STAIRS_DOWN_DIR
