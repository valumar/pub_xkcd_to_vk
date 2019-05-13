import logging
import os
import pathlib
import requests


IMAGE_FOLDER = 'images'

logging.basicConfig(
    format='%(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.DEBUG,
    filename='log.log'
)


def get_image(url):
    pathlib.Path(
        os.path.join(IMAGE_FOLDER)
    ).mkdir(parents=True, exist_ok=True)
    filename = url.split("/")[-1]
    response = requests.get(url)
    logging.info(f'Getting image: {os.path.join(IMAGE_FOLDER, filename)}')
    with open(os.path.join(IMAGE_FOLDER, filename), 'wb') as file:
        file.write(response.content)


def get_image_url(image_num):
    url = f"http://xkcd.com/{image_num}/info.0.json"

    response = requests.get(url)
    if response.ok:
        image_url = response.json()['img']
        image_alt = response.json()['alt']
        return image_url, image_alt


if __name__ == '__main__':
    get_image(get_image_url(615)[0])
