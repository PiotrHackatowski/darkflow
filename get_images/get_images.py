import re
import os
import requests
from bs4 import BeautifulSoup

i = 0
filename_index = 1
name = 'pers_'
dest_dir = 'C:\\Users\\Piotr\\Google Drive\\Colab\\CATS\\pers3\\'

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

for page in range(1, 2):
    #siam site = "https://www.shutterstock.com/search?searchterm=%22Siamese+cat%22+isolated&search_source=base_search_form&language=en&page=" + str(page) + "&sort=popular&image_type=photo&measurement=px&safe=true"
    site = "https://www.shutterstock.com/search?searchterm=%22Persian+cat%22+isolated&search_source=base_search_form&language=en&page=" + str(page) + "&sort=popular&image_type=photo&measurement=px&safe=true"
    response = requests.get(site)

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    urls = [img['src'] for img in img_tags]


    for url in urls:
        filename = re.search(r'/([\w_-]+[.](jpg|jpeg))$', url)
        if filename is not None:
            if 'pers' in filename.group(1):
                i += 1
                print('downloading from page ' + str(page) + ', image ' + str(i) + ' - ' + filename.group(1))
                with open(dest_dir + name + str(filename_index) + '.jpg', 'wb') as f:
                    if 'http' not in url:
                        url = '{}{}'.format(site, url)
                    response = requests.get(url)
                    f.write(response.content)
                    filename_index += 1