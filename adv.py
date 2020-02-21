import random
from ast import literal_eval

from player import Player
from room import Room
from world import World

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = []

# # create Stack constructor
# class Stack():
#     def __init__(self):
#         self.stack = []
#     def push(self, value):
#         self.stack.append(value)
#     def pop(self):
#         if self.size() > 0:
#             return self.stack.pop()
#         else:
#             return None
#     def size(self):
#         return len(self.stack)

# def get_neighbors(vertex_id):
#     # get all neighboring edges of vertex (rooms)
#     return room_graph[vertex_id][1]

# def maze_traversal(beginning_room):
#     # Create a path of all rooms traversed in DFT order
#     # create an empty stack
#     s = Stack()

#     # push the starting vertex into the stack
#     for i, j in room_graph[beginning_room][1].items():
#         s.push((str(i), j))
#     # s.push(beginning_room)

#     # create an empty set to store visited rooms
#     visited = set()

#     # while stack not empty...
#     while s.size() > 0:
#         # pop first vertex
#         v = s.pop()
#         #print(v)
#         # grab the cardinal direction
#         directions = v[0]
#         #print(directions)

#         # add room to traversal path
#         traversal_path.append(directions)

#         # grab room id
#         room_id = v[1]

#         # check if it's been visited
#         if room_id not in visited:
#             # if not visited, add to visited list
#             visited.add(room_id)
#             # print(visited)
#             # then push all neighbors to the top of the stack
#             for i, j in get_neighbors(room_id).items():
#                 # traversal_path.append()
#                 s.push((str(i), j))


def flip_dir(dir):
    if dir == "n":
        return "s"
    if dir == "s":
        return "n"
    if dir == "w":
        return "e"
    if dir == "e":
        return "w"
    else:
        return "error"


def maze_traversal():

    # initiliaze visited dictionary
    visited = {}

    # put the first room in the dictionary
    visited[player.current_room.id] = {}

    while len(visited) < len(room_graph):
        # places ? on unexplored direction
        for direction in player.current_room.get_exits():
            if direction not in visited[player.current_room.id]:
                # if direction not in visited, add ? value
                visited[player.current_room.id][direction] = "?"

        # if there are not unexplored rooms
        if "?" not in visited[player.current_room.id].values():
            # keep slicing off end of traversal_path until you get to a room with unexplored exits
            path_copy = traversal_path.copy()
            while "?" not in visited[player.current_room.id].values():
                backtrack = flip_dir(path_copy.pop())
                player.travel(backtrack)
                traversal_path.append(backtrack)

        else:
            # if there are unexplored rooms
            # picks an unexplored room and travels to it, updates the traversal path and updates visited
            exits = player.current_room.get_exits()
            random.shuffle(exits)
            dir = exits[-1]

            if visited[player.current_room.id][dir] == "?":
                # remember the prev room id
                prev_room_id = player.current_room.id
                # travel to the new room
                player.travel(dir)
                # log the direction in traversal path
                traversal_path.append(dir)
                # update the entry in visited ditionary
                # in the previous room id, set the direction we traveled to the new room id
                visited[prev_room_id][dir] = player.current_room.id
                # # make sure you're not overwriting an existing room you've looped back around to...
                if player.current_room.id not in visited:
                    visited[player.current_room.id] = {}
                # in the current room, set the flipped direction to the previous room id
                visited[player.current_room.id][flip_dir(dir)] = prev_room_id


maze_traversal()


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
