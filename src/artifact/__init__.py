import os


class Artifact:
    def __init__(self, description=None, image=None, alias=None):
        self.description = description
        self.img_path = image
        self.alias = alias

    def get_description(self):
        return self.description

    def get_image(self):
        if os.path.exists(self.img_path):
            return open(self.img_path, 'rb')
        return None

