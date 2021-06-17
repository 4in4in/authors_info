
# парсинг страницы поиска по изображениям google

from typing import Type
from bs4 import BeautifulSoup
import base64
from binascii import Error as binascii_Error
import os

from face_detection import is_image_contains_face

def get_images_and_urls(img_tags_list):
    results = []

    for img_tag in img_tags_list:
        # if img_tag.has_attr('jsname') and img_tag.has_attr('src'):
        img_b64 = img_tag['src']
        url_tags = [tag for tag in img_tag.parent.parent.parent.findAll('a') if tag.has_attr('href')]
        print(url_tags)
        url = [tag['href'] for tag in url_tags][0]
        # url = [x for x in url_tags if (x.has_attr('href') and 'google.com/url' in x['href'])][0]['href']
        results.append({ 'img_b64' : img_b64, 'url' : url })
    
    return results

def parse_page(html_data, out_folder_name, name_url_part):
    html_doc = BeautifulSoup(html_data, features='html.parser')
    html_imgs = html_doc.findAll('img')
    total_imgs = 1
    # base64_imgs = [ img['src'] for img in html_imgs \
    #     if (img.has_attr('jsname') and img.has_attr('src')) ][:total_imgs]
    people_imgs = [ img for img in html_imgs \
        if (img.has_attr('jsname') and img.has_attr('src')) ][:total_imgs]
    img_objects = get_images_and_urls(people_imgs)

    if not os.path.isdir(f'./img_out/'):
        os.mkdir(f'./img_out/')

    for i in range(len(img_objects)):
        image = b64str_to_img(img_objects[i]['img_b64'])
        url = img_objects[i]['url']
        img_extension = image['extension']
        img_bytes = base64.b64decode(image['img_string'])
        if is_image_contains_face(img_bytes):
            if not os.path.isdir(f'./img_out/{out_folder_name}'):
                os.mkdir(f'./img_out/{out_folder_name}')

            path_to_save_img = f'./img_out/{out_folder_name}/{str(i)}_{name_url_part}.{img_extension}'
            path_to_save_txt = f'./img_out/{out_folder_name}/{str(i)}_{name_url_part}.txt'
            
            save_image_from_b64(path_to_save_img, img_bytes)
            save_txt_url(path_to_save_txt, url)

    # for i in range(len(base64_imgs)):
    #     image = b64str_to_img(base64_imgs[i])
    #     img_str = image['img_string']
    #     extension = image['extension']
    #     img_bytes = base64.b64decode(img_str)
        
    #     if is_image_contains_face(img_bytes):
    #         if not os.path.isdir(f'./img_out/{out_folder_name}'):
    #             os.mkdir(f'./img_out/{out_folder_name}')

    #         path_to_save = f'./img_out/{out_folder_name}/{str(i)}_{name_url_part}.{extension}'
            
    #         save_image_from_b64(path_to_save, img_bytes)


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

def save_txt_url(path, url):
    with open(path, 'w') as f:
        f.write(url)
