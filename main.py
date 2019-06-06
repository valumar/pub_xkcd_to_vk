import logging
import os
import random
import requests
from dotenv import load_dotenv

load_dotenv()

base_api_url = "https://api.vk.com/method/"

logging.basicConfig(
    format='%(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.DEBUG,
    # filename='log.log'
)


def get_image(url):
    filename = url.split("/")[-1]
    response = requests.get(url)
    logging.info(f'Getting image: {filename}')
    return response.content


def get_last_image_num():
    url = f"http://xkcd.com/info.0.json"

    response = requests.get(url)
    if response.ok:
        last_image_num = response.json()["num"]
        return last_image_num


def get_image_url(image_num):
    url = f"http://xkcd.com/{image_num}/info.0.json"

    response = requests.get(url)
    if response.ok:
        image_url = response.json()['img']
        image_alt = response.json()['alt']
        return image_url, image_alt


def get_upload_url(group_id):
    api_method = "photos.getWallUploadServer"
    payload = {
        "access_token": os.getenv("VK_ACCESS_TOKEN"),
        "v": "5.95",
        "group_id": group_id
    }
    try:
        response = requests.get(f"{base_api_url}{api_method}", params=payload)
        response.raise_for_status()
        return response.json()["response"]["upload_url"]
    except Exception:
        logging.exception(f"Exception in `get_upload_url`:\n {response.json()}")


def upload_photo(image, upload_url):
    try:
        files = {'photo': ('img.png',image,'multipart/form-data',{'Expires': '0'}) }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        return response.json()
    except Exception:
        logging.exception("Exception in `upload_photo`")


def save_photo(data):
    server = data["server"]
    hash = data["hash"]
    photo = data["photo"]
    method = "photos.saveWallPhoto"
    payload = {
        "group_id": os.getenv("VK_GROUP_ID"),
        "photo": photo,
        "server": server,
        "hash": hash,
        "access_token": os.getenv("VK_ACCESS_TOKEN"),
        "v": "5.95"
    }
    try:
        response = requests.post(f"{base_api_url}{method}", params=payload)
        response.raise_for_status()
        return response.json()
    except Exception:
        logging.exception("Exception in `save_photo`")


def post_photo(data, image_alt):

    group_id = os.getenv("VK_GROUP_ID")
    media_id = data["response"][0]["id"]
    owner_id = data["response"][0]["owner_id"]

    api_method = "wall.post"
    payload = {
        "access_token": os.getenv("VK_ACCESS_TOKEN"),
        "v": "5.95",
        "owner_id": - int(group_id),
        "from_group": 1,
        "attachments": f"photo{owner_id}_{media_id}",
        "message": f"{image_alt}"
    }
    try:
        response = requests.post(f"{base_api_url}{api_method}", params=payload)
        response.raise_for_status()
        return response
    except Exception:
        logging.exception("Exception in `post_photo`")


def get_posted_pics():
    try:
        with open('posted_pics.txt', 'r', encoding='utf8') as f:
            posted_pics = set(f.read().splitlines())
    except FileNotFoundError:
        logging.exception('`posted_pics.txt` not found')
        posted_pics = set()
    return posted_pics


def write_posted_pic(image_num):
    with open('posted_pics.txt', 'a', encoding='utf8') as f:
        f.write(f"{image_num}\n")


def get_random_image_num():
    last_image_num = get_last_image_num()
    not_posted_images = set(range(1, last_image_num + 1)) - get_posted_pics()
    return random.choice(list(not_posted_images))


def main():
    image_num = get_random_image_num()
    image = get_image(get_image_url(image_num)[0])
    image_alt = get_image_url(image_num)[1]
    upload = upload_photo(image, get_upload_url(os.getenv("VK_GROUP_ID")))
    save = save_photo(upload)
    if post_photo(save, image_alt).ok:
        write_posted_pic(image_num)


if __name__ == '__main__':
    main()
