import matplotlib.pyplot as plt
import numpy as np
import random
import math
import functools
import operator

curr_map = np.empty((120, 160))
rough_terrain_centers = None
highways = None


# 0 - Blocked Cell
# 1 - Unblocked Cell
# 2 - Rough Terrain Cell
# 3 - Unblocked Cell w/ Highway
# 4 - Rough Terrain Cell w/ Highway


def rand_x():
    """ Returns a value within the x domain - 0 to 160"""
    x = random.randint(0, 119)
    return x


def rand_y():
    """ Returns a value within the y domain - 0 to 120"""
    y = random.randint(0, 159)
    return y


def rand_coin_flip():
    """ Returns a value based on 50% probability"""
    coin = random.randint(0, 1)
    return coin


def rand_sixty_forty():
    """ Returns a value within the y domain - 0 to 120"""
    val = random.randint(1, 10)
    if val <= 6:
        return 1
    elif val >= 7:
        return 0


def save_map(map, s_start, s_goal, rtc, file_name):
    f = open(file_name, "w")
    start_p = '(' + str(s_start[0]) + ', ' + str(s_start[1]) + ')'
    end_p = '(' + str(s_goal[0]) + ', ' + str(s_goal[1]) + ')'
    f.write(start_p + '\n')
    f.write(end_p + '\n')
    for i in rtc:
        p = '(' + str(i[0]) + ', ' + str(i[1]) + ')'
        f.write(p + '\n')
    for x in range(120):
        for y in range(160):
            f.write(str(int(map.item((x, y)))) + " ")
        f.write('\n')


def highway_gen():
    all_highway_paths = []
    for k in range(4):
        current_highway_path = []
        h_or_v = rand_coin_flip()

        # Horizontal
        if h_or_v == 0:
            y_val = rand_y()
            starting_point = [0, y_val]
            current_highway_path.append(starting_point)
            next_x_val = 1
            next_y_val = y_val
            while next_x_val != 120:
                if rand_sixty_forty() == 1:
                    next_point = [next_x_val, next_y_val]
                    current_highway_path.append(next_point)
                    next_x_val += 1

                elif rand_sixty_forty() == 0:
                    coin = rand_coin_flip()
                    if coin == 0:
                        if next_y_val < 160:
                            next_y_val += 1
                        next_point = [next_x_val, next_y_val]
                        current_highway_path.append(next_point)
                        next_x_val += 1
                    if coin == 1:
                        if next_y_val > 0:
                            next_y_val -= 1
                        next_point = [next_x_val, next_y_val]
                        current_highway_path.append(next_point)
                        next_x_val += 1

        # Vertical
        elif h_or_v == 1:
            x_val = rand_x()
            starting_point = [x_val, 0]
            current_highway_path.append(starting_point)
            next_y_val = 1
            next_x_val = x_val
            while next_y_val != 160:
                if rand_sixty_forty() == 1:
                    next_point = [next_x_val, next_y_val]
                    current_highway_path.append(next_point)
                    next_y_val += 1

                elif rand_sixty_forty() == 0:
                    coin = rand_coin_flip()
                    if coin == 0:
                        if next_x_val < 120:
                            next_x_val += 1
                        next_point = [next_x_val, next_y_val]
                        current_highway_path.append(next_point)
                        next_y_val += 1
                    if coin == 1:
                        if next_x_val > 0:
                            next_x_val -= 1
                        next_point = [next_x_val, next_y_val]
                        current_highway_path.append(next_point)
                        next_y_val += 1
        all_highway_paths.append(current_highway_path)
    return all_highway_paths


def ter_center():
    """
    Generates the 8 points to be used for the centers of the 31x31 terrain generation

    :return:
    center - Array of 8 points ex.[[0,0], [1,1], etc...]
    """
    centers = []
    for i in range(8):
        x = rand_x()
        y = rand_y()
        points_arr = [x, y]
        centers.append(points_arr)
        print(centers[i])
    return centers


def block_cell_gen():
    block_cells = []
    for k in range(3840):
        x_val = rand_x()
        y_val = rand_y()
        point = [x_val, y_val]
        bool_val = 0
        for h in highways:
            for i in h:
                if x_val == i[0] and y_val == i[1]:
                    bool_val = 1

        if bool_val == 1 or point in block_cells:
            k -= 1
        elif bool_val == 0:

            block_cells.append(point)
    return block_cells


def generate_h(start_point, end_point, map):
    sp_cell_type = map.item(start_point[0], start_point[1])
    ep_cell_type = map.item(end_point[0], end_point[1])

    if sp_cell_type == 0 or ep_cell_type == 0:
        return -1

    # UnB to UnB
    if sp_cell_type == 1 and ep_cell_type == 1:
        # Diag Check
        if (start_point[0] + 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] - 1 == end_point[1]):
            return math.sqrt(2)
        # V & H Check
        elif (start_point[0] == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] == end_point[1]):
            return 1

    # R to R
    if sp_cell_type == 2 and ep_cell_type == 2:
        # Diag Check
        if (start_point[0] + 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] - 1 == end_point[1]):
            return math.sqrt(8)
        # V & H Check
        elif (start_point[0] == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] == end_point[1]):
            return 2

    # UnB to R
    if (sp_cell_type == 1 and ep_cell_type == 2) or (sp_cell_type == 2 and ep_cell_type == 1):
        # Diag Check
        if (start_point[0] + 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] - 1 == end_point[1]):
            return (math.sqrt(2) + math.sqrt(8)) / 2
        # V & H Check
        elif (start_point[0] == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] == end_point[1]):
            return 1.5

    # UnB-HW to UnB-HW
    if sp_cell_type == 3 and ep_cell_type == 3:
        # Diag Check
        if (start_point[0] + 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] - 1 == end_point[1]):
            return math.sqrt(2) / 4
        # V & H Check
        elif (start_point[0] == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] == end_point[1]):
            return 1 / 4

    # Rough-HW to Rough-HW
    if sp_cell_type == 4 and ep_cell_type == 4:
        # Diag Check
        if (start_point[0] + 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] - 1 == end_point[1]):
            return math.sqrt(8) / 4
        # V & H Check
        elif (start_point[0] == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] == end_point[1]):
            return 2 / 4

    # UnB-HW to R-HW
    if (sp_cell_type == 3 and ep_cell_type == 4) or (sp_cell_type == 4 and ep_cell_type == 3):
        # Diag Check
        if (start_point[0] + 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] - 1 == end_point[1]):
            return ((math.sqrt(2) + math.sqrt(8)) / 2) / 4
        # V & H Check
        elif (start_point[0] == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] == end_point[1]):
            return 1.5 / 4

    # UnB to UnB-HW
    if (sp_cell_type == 1 and ep_cell_type == 3) or (sp_cell_type == 3 and ep_cell_type == 1):
        # Diag Check
        if (start_point[0] + 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] - 1 == end_point[1]):
            return (math.sqrt(2) + (math.sqrt(2) / 4)) / 2
        # V & H Check
        elif (start_point[0] == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] == end_point[1]):
            return (1 + (1 / 4)) / 2

    # UnB to R-HW
    if (sp_cell_type == 1 and ep_cell_type == 4) or (sp_cell_type == 4 and ep_cell_type == 1):
        # Diag Check
        if (start_point[0] + 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] - 1 == end_point[1]):
            return (math.sqrt(2) + (math.sqrt(8) / 4)) / 2
        # V & H Check
        elif (start_point[0] == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] == end_point[1]):
            return (1 + (2 / 4)) / 2

    # R to UnB-HW
    if (sp_cell_type == 2 and ep_cell_type == 3) or (sp_cell_type == 3 and ep_cell_type == 2):
        # Diag Check
        if (start_point[0] + 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] - 1 == end_point[1]):
            return (math.sqrt(8) + (math.sqrt(2) / 4)) / 2
        # V & H Check
        elif (start_point[0] == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] == end_point[1]):
            return (2 + (1 / 4)) / 2

    # R to R-HW
    if (sp_cell_type == 2 and ep_cell_type == 4) or (sp_cell_type == 4 and ep_cell_type == 2):
        # Diag Check
        if (start_point[0] + 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] - 1 == end_point[1]):
            return (math.sqrt(8) + (math.sqrt(8) / 4)) / 2
        # V & H Check
        elif (start_point[0] == end_point[0] and start_point[1] + 1 == end_point[1]) or\
                (start_point[0] == end_point[0] and start_point[1] - 1 == end_point[1]) or\
                (start_point[0] + 1 == end_point[0] and start_point[1] == end_point[1]) or\
                (start_point[0] - 1 == end_point[0] and start_point[1] == end_point[1]):
            return (2 + (2 / 4)) / 2


def gen_map(centers, highway_paths, block_cells):
    # Creates 2-D array size 160x120 and sets all the values to 1 - Unblocked Cells
    a = np.empty((120, 160))
    a.fill(1)

    # Generates rough terrain
    for point_set in centers:
        x_value = point_set[0]
        y_value = point_set[1]

        left_x_bound = 0
        right_x_bound = 119
        upper_y_bound = 0
        lower_y_bound = 159

        if x_value - 15 > 0:
            left_x_bound = x_value - 15
        if x_value + 15 < 120:
            right_x_bound = x_value + 15
        if y_value - 15 > 0:
            upper_y_bound = y_value - 15
        if y_value + 15 < 160:
            lower_y_bound = y_value + 15

        for y_point in range(upper_y_bound, lower_y_bound):
            for x_point in range(left_x_bound, right_x_bound):
                coin = rand_coin_flip()
                if coin == 0:
                    a.itemset((x_point, y_point), 2)
                elif coin == 1:
                    a.itemset((x_point, y_point), 1)

    # Generates highways
    for i in highway_paths:
        for k in i:
            x_val = k[0]
            y_val = k[1]
            if a.item(x_val, y_val) == 1:
                a.itemset((x_val, y_val), 3)
            elif a.item(x_val, y_val) == 2:
                a.itemset((x_val, y_val), 4)

    # Generates blocked cells
    for p in block_cells:
        x_val = p[0]
        y_val = p[1]
        a.itemset((x_val, y_val), 0)

    return a



# Main


menu = True
while (menu):
    print("Please make a selection: ")
    selection = input()
    if selection == "g" or selection == "G":
        rough_terrain_centers = ter_center()
        highways = highway_gen()
        blocked_cells = block_cell_gen()
        curr_map = gen_map(rough_terrain_centers, highways, blocked_cells)
        print("New Map Generated!")
    elif selection == "show" or selection == "sh":
        plt.imshow(curr_map, cmap='Paired', interpolation='nearest')
        plt.show()
    elif selection == "save" or selection == "s":
        print("Please enter file name (.txt):")
        f_name = input()
        save_map(curr_map, [1, 2], [1, 1], rough_terrain_centers, f_name + ".txt")
    elif selection == "end" or selection == "e":
        menu = False
