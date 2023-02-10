from map_util import MAX_COOR, map_coor_2_normalized


class Node(object):

    def __init__(self, id, ug, og, srv, subsrv, x, y, z):
        self.id = int(id)
        self.srv = srv
        self.subsrv = subsrv

        if (ug == 'true'):
            self.surface = -1
        elif (og == 'true'):
            self.surface = 1
        else:
            self.surface = 0

        self.x, self.y, self.z = map_coor_2_normalized(float(x), float(y), float(z))

    