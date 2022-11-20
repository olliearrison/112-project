# calculate the hex from RGBA with a white background
# partially adopted from class website
def rgbaString(r, g, b, a=255):
    a = a/255
    R,G,B = (255,255,255)
    # three lines adjusted from StackOverflow:
    r2 = int(r * a + (1.0 - a) * R)
    g2 = int(g * a + (1.0 - a) * G)
    b2 = int(b * a + (1.0 - a) * B)
    return f'#{r2:02x}{g2:02x}{b2:02x}'

