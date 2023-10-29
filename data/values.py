import base64
from urllib.request import urlopen

from data.data import *

sommets_df, aretes_df = get_data()
graph = get_graph()
station_coordinates = get_station_coordinates()

decalage_y = 34
circle_radius = 4

bg_color = "#4BC0AD"
fg_color = "#004FA3"
light_color = "#FFFDE8"


# Images :
def fetch_image_from_url(url: str) -> base64:
    """
    Récupère une image à partir d'une URL et la convertit en base64.

    Parameters:
        url (str): L'URL de l'image à récupérer.

    Returns:
        None: L'image en base 64.
    """
    u = urlopen(url)
    raw_data = u.read()
    u.close()

    return raw_data


image_urls = {
    "logo_ratp" : r"https://github.com/Swiiiip/Projet_RATP/blob/a76dce810b7a3a8074abd5e3ff4780d1b02780f5/data/assets/logo_ratp.png?raw=true",
    "arrow" : r"https://github.com/Swiiiip/Projet_RATP/blob/a76dce810b7a3a8074abd5e3ff4780d1b02780f5/data/assets/arrow.png?raw=true",
    "metrof_r" : r"https://github.com/Swiiiip/Projet_RATP/blob/a76dce810b7a3a8074abd5e3ff4780d1b02780f5/data/assets/metrof_r.png?raw=true",
    }

images_base64 = dict()
for name, url in image_urls.items():
    images_base64[name] = fetch_image_from_url(url)
