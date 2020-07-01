from PIL import Image

class ImageObj(object):
    """description of class"""
    def __init__(self):
        pass

    def resize(file, width, height):
        image = Image.open(file)
        new_image = image.resize((int(width), int(height)))
        new_image.save(file)