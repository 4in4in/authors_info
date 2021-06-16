
# парсинг страницы поиска по изображениям google и сохранение первых 20 картинок

from typing import Type
from bs4 import BeautifulSoup
import base64
from binascii import Error as binascii_Error
import os

from face_detection import is_image_contains_face


def parse_page(html_data, out_folder_name, name_url_part):
    html_doc = BeautifulSoup(html_data, features='html.parser')
    html_imgs = html_doc.findAll('img')
    total_imgs = 1
    base64_imgs = [ img['src'] for img in html_imgs \
        if (img.has_attr('jsname') and img.has_attr('src')) ][:total_imgs]

    if not os.path.isdir(f'./img_out/'):
        os.mkdir(f'./img_out/')

    for i in range(len(base64_imgs)):
        image = b64str_to_img(base64_imgs[i])
        img_str = image['img_string']
        extension = image['extension']
        img_bytes = base64.b64decode(img_str)
        
        if is_image_contains_face(img_bytes):
            if not os.path.isdir(f'./img_out/{out_folder_name}'):
                os.mkdir(f'./img_out/{out_folder_name}')

            path_to_save = f'./img_out/{out_folder_name}/{str(i)}_{name_url_part}.{extension}'
            
            save_image_from_b64(path_to_save, img_bytes)


def b64str_to_img(img_base64str):
    header_end_pos = img_base64str.find(',')
    img_str = img_base64str[header_end_pos+1 : ]
    extension = img_base64str[img_base64str.find('/') + 1 :img_base64str.find(';')]
    return { 'img_string': img_str, 'extension': extension }

def save_image_from_b64(path, img_bytes):
    with open(path, 'wb') as f:
        try:
            f.write(img_bytes)
        except binascii_Error as e:
            print(e)
