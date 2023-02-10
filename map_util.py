
MAX_COOR = 8648


# map x and z from original map coordinate 
# to relitive coordinate from 0 to 1
def map_coor_2_normalized(x, y, z):
    x_out = (x + MAX_COOR) / (MAX_COOR * 2)
    z_out = (z - MAX_COOR) / (MAX_COOR * 2)
    y_out = y
    return x_out, y_out, z_out