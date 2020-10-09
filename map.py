import matplotlib.pyplot as plt
import numpy as np
import random

curr_map = np.empty((160, 120))
rough_terrain_centers = None
highways = None


# 0 - Blocked Cell
# 1 - Unblocked Cell
# 2 - Rough Terrain Cell
# 3 - Unblocked Cell w/ Highway
# 4 - Rough Terrain Cell w/ Highway


def rand_x():
    """ Returns a value within the x domain - 0 to 160"""
    x = random.randint(0, 159)
    return x


def rand_y():
    """ Returns a value within the y domain - 0 to 120"""
    y = random.randint(0, 119)
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
            while next_x_val != 160:
                if rand_sixty_forty() == 1:
                    next_point = [next_x_val, next_y_val]
                    current_highway_path.append(next_point)
                    next_x_val += 1

                elif rand_sixty_forty() == 0:
                    coin = rand_coin_flip()
                    if coin == 0:
                        if next_y_val < 120:
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
            while next_y_val != 120:
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
        bool_val = 0
        for h in highways:
            for i in h:
                if x_val == i[0] and y_val == i[1]:
                    bool_val = 1

        if bool_val == 1:
            k -= 1
        elif bool_val == 0:
            point = [x_val, y_val]
            block_cells.append(point)
    return block_cells


def gen_map(centers, highway_paths, block_cells):
    # Creates 2-D array size 160x120 and sets all the values to 1 - Unblocked Cells
    a = np.empty((160, 120))
    a.fill(1)

    for point_set in centers:
        x_value = point_set[0]
        y_value = point_set[1]

        left_x_bound = 0
        right_x_bound = 160
        upper_y_bound = 0
        lower_y_bound = 120

        if x_value - 15 > 0:
            left_x_bound = x_value - 15
        if x_value + 15 < 160:
            right_x_bound = x_value + 15
        if y_value - 15 > 0:
            upper_y_bound = y_value - 15
        if y_value + 15 < 120:
            lower_y_bound = y_value + 15

        for y_point in range(upper_y_bound, lower_y_bound):
            for x_point in range(left_x_bound, right_x_bound):
                coin = rand_coin_flip()
                if coin == 0:
                    a.itemset((x_point, y_point), 2)
                elif coin == 1:
                    a.itemset((x_point, y_point), 1)

    for i in highway_paths:
        for k in i:
            x_val = k[0]
            y_val = k[1]
            if a.item(x_val, y_val) == 1:
                a.itemset((x_val, y_val), 3)
            elif a.item(x_val, y_val) == 2:
                a.itemset((x_val, y_val), 4)

    for p in block_cells:
        x_val = p[0]
        y_val = p[1]
        a.itemset((x_val, y_val), 0)

    plt.imshow(a, cmap='Paired', interpolation='nearest')
    plt.show()


# Main
rough_terrain_centers = ter_center()
highways = highway_gen()
blocked_cells = block_cell_gen()

gen_map(rough_terrain_centers, highways, blocked_cells)
