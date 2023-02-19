def scale(size):
    return str(round(abs(size[0][0] - size[1][0]), 4)), \
        str(round(abs(size[0][1] - size[1][1]), 4))