# Import
from bs4 import BeautifulSoup
import urllib

# Class to get image from Google
class imageRequest:
    """Class to get image from pixabay. Made for the EARIA2016 hackathon."""
    # Constructor
    def getImage(self, query):

        # Get page content and parse
#         html = urllib.urlopen('https://pixabay.com/en/photos/?q=' + query + '&image_type=&cat=&min_width=&min_height=').read()
        html = urllib.urlopen('https://pixabay.com/en/photos/?q=' + query ).read()
        soup = BeautifulSoup(html, 'html.parser')

        # Get the first image's URL
        photo_grid = soup.find("div", { "id" : "photo_grid" })

        # Search images
        if photo_grid is not None:
            image_soup = BeautifulSoup(str(photo_grid), 'html.parser')
            images = image_soup.find("img");
            # return "http://pixabay.com/" + str(images['src'])
            return str(images['src'])
        else:
            return None

    #end getImage    