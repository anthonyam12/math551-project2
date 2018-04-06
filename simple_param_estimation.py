import random as rand
import copy
import os


COL_ROW_COUNT = 15


def print_grid(grid):
    for row in grid:
        print(row)


def populate_grid(grid, humans, zombies, stunned):
    for i in range(humans):
        row = rand.randint(0, 9)
        col = rand.randint(0, 9)
        while grid[row][col] != 'e':
            row = rand.randint(0, 9)
            col = rand.randint(0, 9)
        grid[row][col] = 'h'
    for i in range(zombies - stunned):
        row = rand.randint(0, 9)
        col = rand.randint(0, 9)
        while grid[row][col] != 'e':
            row = rand.randint(0, 9)
            col = rand.randint(0, 9)
        grid[row][col] = 'z'


def apply_rules(grid, humans, zombies, removed):
    ijs = []
    g_occur = False
    k_occur = False
    for i in range(len(grid)):
        row = grid[i]
        for j in range(len(row)):
            if row[j] == 'z':
                h_count = check_neighbors(grid, i, j)
                if h_count in [5]:
                    ijs.append([i,j])
                elif h_count in [1, 2, 3, 4]:
                    zombies += h_count
                    humans -= h_count
                    if humans < 0:
                        zombies -= abs(humans)
                        humans = 0
                    k_occur = True
                elif h_count in [6, 7, 8]:
                    zombies -= 1
                    removed += 1
                    g_occur = True
    for ij in ijs:
        grid[ij[0]][ij[1]] = 's'
    return humans, zombies, removed, k_occur, g_occur


def check_neighbors(grid, row, col):
    # highly inelegant
    count = 0
    if grid[row-1][col-1] == 'h':
        if row - 1 > 0 and col - 1 > 0:
            count += 1
    if grid[row-1][col] == 'h':
        if row - 1 > 0:
            count += 1
    if grid[row-1][(col+1) % COL_ROW_COUNT] == 'h':
        if row - 1 > 0 and col + 1 < COL_ROW_COUNT:
            count += 1
    if grid[row][col-1] == 'h':
        if col - 1 > 0:
            count += 1
    if grid[row][(col+1) % COL_ROW_COUNT] == 'h':
        if col + 1 < COL_ROW_COUNT:
            count += 1
    if grid[(row+1) % COL_ROW_COUNT][col-1] == 'h':
        if row + 1 < COL_ROW_COUNT and col - 1 > 0:
            count += 1
    if grid[(row+1) % COL_ROW_COUNT][col] == 'h':
        if row + 1 < COL_ROW_COUNT:
            count += 1
    if grid[(row+1) % COL_ROW_COUNT][(col+1) % COL_ROW_COUNT] == 'h':
        if row + 1 < COL_ROW_COUNT and col + 1 < COL_ROW_COUNT:
            count += 1
    return count


def reset_grid(grid):
    stunned = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 's':
                grid[i][j] = 'z'
                stunned += 1
            else:
                grid[i][j] = 'e'
    return stunned


def count_populations(grid):
    z, r, h = 0, 0, 0
    for row in grid:
        for col in row:
            if col == 'h':
                h += 1
            elif col == 'z' or col == 's':
                z += 1
    r = 50 - z - h
    return h, z, r


if __name__ == '__main__':
    game_file_name = 'out/population_changes.csv'
    params_file_name = 'out/param_counts.csv'

    game = open(game_file_name, 'a')
    params = open(params_file_name, 'a')

    for run in range(0, 10000):
        grid = [['e' for i in range(COL_ROW_COUNT)] for j in range(COL_ROW_COUNT)]
        humans = 49
        zombies = 1
        removed = 0
        stunned = 0

        turns = 0
        g_count = 0
        k_count = 0
        populate_grid(grid, humans, zombies, stunned)
        while humans > 0 and zombies > 0:
            game.write(str(run) + ', ' + str(turns) + ', ' + str(humans) +
                         ', ' + str(zombies) + ', ' + str(removed) + '\n')
            humans, zombies, removed, k, g = apply_rules(grid, humans, zombies, removed)
            # gather stats
            if k:
                k_count += 1
            if g:
                g_count += 1
            stunned = reset_grid(grid)
            populate_grid(grid, humans, zombies, stunned)
            turns += 1
        game.write(str(run) + ', ' + str(turns) + ', ' + str(humans) +
                     ', ' + str(zombies) + ', ' + str(removed) + '\n')
        print(humans, zombies, removed)
        print(turns, k_count, g_count)
        params.write(str(run) + ', ' + str(turns) + ', ' + str(k_count) + ', '
                     + str(g_count) + '\n')
    game.close()
    params.close()
