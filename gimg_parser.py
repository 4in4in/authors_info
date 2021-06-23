
# парсинг страницы поиска по изображениям google

from typing import Type
from bs4 import BeautifulSoup
import base64
from binascii import Error as binascii_Error
import os

from face_detection import FaceDetector
from info_parser import AuthorInfoParser

class GoogleImgParser:

    @classmethod
    def get_images_and_urls(cls, img_tags_list): 
        '''
        получить список словарей вида 
        {
            'img_b64': изображение в формате base64,
            'url': ссылка, откуда взято изображение
        }
        '''
        results = []

        for img_tag in img_tags_list:
            img_b64 = img_tag['src']
            url_tags = [tag for tag in img_tag.parent.parent.parent.findAll('a') if tag.has_attr('href')]
            url = [tag['href'] for tag in url_tags][0]
            results.append({ 'img_b64' : img_b64, 'url' : url })
        
        return results

    @classmethod
    def get_html_imgs(cls, img_tags, total_imgs):
        # отобрать все img-теги, которые соответствуют найденным изображениям
        result_imgs = [tag for tag in img_tags if (tag.has_attr('jsname') and tag.has_attr('src'))]
        return result_imgs[:total_imgs]

    @classmethod
    def process_image(cls, img_object, out_folder_name, name_url_part, img_num):
            image = cls.b64str_to_img(img_object['img_b64'])
            url = img_object['url']
            img_extension = image['extension']
            img_bytes = base64.b64decode(image['img_string'])
            if FaceDetector.is_image_contains_face(img_bytes):

                cls.create_folder_if_not_exist('./img_out')
                cls.create_folder_if_not_exist(f'./img_out/{out_folder_name}')

                path_to_save_img = f'./img_out/{out_folder_name}/{img_num}_{name_url_part}.{img_extension}'
                path_to_save_txt = f'./img_out/{out_folder_name}/{img_num}_{name_url_part}.txt'
                cls.save_image_from_b64(path_to_save_img, img_bytes)
                info = AuthorInfoParser.get_info(url)
                if info is not None:
                    cls.save_info_text(path_to_save_txt, info)

    @classmethod
    def parse_page(cls, html_data, out_folder_name, name_url_part):
        html_doc = BeautifulSoup(html_data, features='html.parser')
        total_imgs = 1
        html_imgs = cls.get_html_imgs(html_doc.findAll('img'), total_imgs)
        img_objects = cls.get_images_and_urls(html_imgs)

        for i in range(len(img_objects)):
            cls.process_image(img_objects[i], out_folder_name, name_url_part, i)

    @classmethod
    def b64str_to_img(cls, img_base64str):
        '''
        удалить из base64-строки изображения ненужную информацию о mime-типе.
        возвращает словарь со строкой изображения base64, пригодной для сохранения,
        и его расширение из mime-типа
        '''
        header_end_pos = img_base64str.find(',')
        img_str = img_base64str[header_end_pos+1 : ]
        extension = img_base64str[img_base64str.find('/') + 1 :img_base64str.find(';')]
        return { 'img_string': img_str, 'extension': extension }

    @classmethod
    def save_image_from_b64(cls, path, img_bytes):
        # сохранить изображение из массива байтов
        with open(path, 'wb') as f:
            try:
                f.write(img_bytes)
            except binascii_Error as e:
                print(e)

    @classmethod
    def save_info_text(cls, path, info_text):
        # сохранить найденную информацию о человеке
        with open(path, 'w') as f:
            f.write(info_text)

    @classmethod
    def create_folder_if_not_exist(cls, path):
        if not os.path.isdir(path):
            os.mkdir(path)
