from base64 import b64encode
from IPython.display import Image, display, HTML


def render_photo(path):
    try:
        img = open(path, 'rb').read()
    except:
        img = open('img/artifacts/key.png').read()
    data_url = 'data:image/jpeg;base64,' + b64encode(img).decode()
    return data_url

def go():
    display(HTML(f"<img src='{render_photo('img/artifacts/key.png')}' width='130'>"))