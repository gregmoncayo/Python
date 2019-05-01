"""Generation - Dominick Aiudi
Procedurally generate the islands in the game"""

import random


class Generation(object):
    def __init__(self, num_rows=3, num_columns=3):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.max_rooms = (num_rows * num_columns)

        self.path = []
        self.rows = []
        self.completed = False

    class Room(object):
        def __init__(self, exits=0, max_exits=4):
            self.max_exits = max_exits
            self.exits = exits
            self.neighbors = dict() # 1 = top; 2 = right; 3 = bottom; 4 = left
            self.status = 0 # 1 = start; 2 = end
            self.visited = False
            # debug
            self.iter_num = 0

    def make(self):
        # Create set of blank rooms
        # Assign max number of exits based on position
        for i in range(self.num_rows):
            rooms = []
            for j in range(self.num_columns):
                new_room = self.Room()
                if i == 0 or i == (self.num_rows - 1):
                    new_room.max_exits -= 1
                if j == 0 or j == (self.num_columns - 1):
                    new_room.max_exits -= 1
                rooms.append(new_room)
            self.rows.append(rooms)


        # Link rooms together horizontally
        for row in self.rows:
            for i in range((len(row) - 1)):
                row[i].neighbors[2] = row[(i + 1)]
                row[(i + 1)].neighbors[4] = row[i]

        # Link rooms together vertically
        for i in range(len(self.rows) - 1):
            row = self.rows[i]
            next_row = self.rows[(i + 1)]
            for j in range(len(row)):
                row[j].neighbors[3] = next_row[j]
                next_row[j].neighbors[1] = row[j]

        # Ending room selection
        row = random.choice(self.rows)
        last_room = random.choice(row)
        # Pick random neighbor, eliminate others
        last_key, last_entry = random.choice(list(last_room.neighbors.items()))
        for i in range(1, 5):
            if i == last_key:
                continue
            if i not in last_room.neighbors:
                continue
            self.disconnectRooms(last_room, last_room.neighbors[i], i)
        last_room.visited = True
        last_room.iter_num = 1

        # Begin the fun
        self.makePath(last_room, last_room.neighbors[last_key], 2)

    # Recursive(I guess?) function for generation
    def makePath(self, parent_room, current_room, num_vistited):
        if current_room.visited: return
        else:
            current_room.visited = True
            current_room.iter_num = num_vistited

        # Run if not a dead end
        if len(current_room.neighbors) is not 1:
            # Pick number of removed exits based on number of neighbors
            current_room.exits = random.randint(2, len(current_room.neighbors))
            # Remove that number of exits
            for i in range(2, current_room.exits):
                # Pick random room
                remove_key = random.choice(list(current_room.neighbors.keys()))
                # Don't remove the parent (previous) room
                while current_room.neighbors[remove_key] is parent_room:
                    remove_key = random.choice(list(current_room.neighbors.keys()))
                # Don't remove a visited room
                if not current_room.neighbors[remove_key].visited:
                    # Don't remove a dead end
                    if not len(current_room.neighbors[remove_key].neighbors) is 1:
                        self.disconnectRooms(current_room, current_room.neighbors[remove_key], remove_key)
        # Return if dead end
        else: return

        # Iterate + generate through availible rooms
        for key in list(current_room.neighbors.keys()):
            self.makePath(current_room, current_room.neighbors[key], num_vistited + 1)

    # Check if all rooms have been visited
    def isComplete(self):
        for row in self.rows:
            for room in row:
                if not room.visited:
                    return False
        return True

    # Connects two rooms using loc for orientation
    def connectRooms(self, room1, room2, loc):
        room1.neighbors[loc] = room2
        if (loc < 3):
            room2.neighbors[(loc+2)] = room1
        else:
            room2.neighbors[(loc-2)] = room1

    # Disconnects two rooms using loc for orientation
    def disconnectRooms(self, room1, room2, loc):
        del room1.neighbors[loc]
        if (loc < 3):
            del room2.neighbors[(loc+2)]
        else:
            del room2.neighbors[(loc-2)]


    # Prints the set of Rooms
    # to the interpreter
    def printRooms(self):
        for row in self.rows:
            str_row = ""
            # First row of text
            for room in row:
                if 1 in room.neighbors:
                    str_row += "= =   = = "
                else:
                    str_row += "= = = = = "
            print(str_row)
            # Second row of text
            str_row = ""
            for room in row:
                str_row += "=       = "
            print(str_row)
            # Third row of text
            str_row = ""
            for room in row:
                if 4 in room.neighbors:
                    str_row += "  "
                else:
                    str_row += "= "
                str_row += "  "
                str_row += str(room.iter_num)
                if room.iter_num > 9:
                    str_row += "  "
                else:
                    str_row += "   "
                if 2 in room.neighbors:
                    str_row += "  "
                else:
                    str_row += "= "
            print(str_row)
            # Fourth row of text
            str_row = ""
            for room in row:
                str_row += "=       = "
            print(str_row)
            # Fifth row of text
            str_row = ""
            for room in row:
                if 3 in room.neighbors:
                    str_row += "= =   = = "
                else:
                    str_row += "= = = = = "
            print(str_row)
        print()


# # Simulates usage in the Game code
# def main():
#     gen = Generation()
#     gen.make()
#     while not gen.isComplete():
#         del gen
#         print("Generation failed, remaking...")
#         gen = Generation()
#         gen.make()
#     gen.printRooms()


# if __name__ == "__main__": main()
