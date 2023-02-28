def scale(size):
    longitude = round(abs(size[0][0] - size[1][0]) , 4)
    latitude = round(abs(size[0][1] - size[1][1]), 4)
    return str(longitude), str(latitude)
