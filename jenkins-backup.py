#!/usr/bin/env python3

import logging
import os

import requests

from config import *

logging.captureWarnings(True)


def get_config_xml(url):
    """
    Выполняется запрос к API Jenkins и получает файл в формате XML,
    который записывается на диск
    """
    dir_name = JOBS_DIR + url.split('/')[-4] + '/'
    url += 'config.xml'
    response = requests.get(url, auth=(USER, API_TOKEN))
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    f_name = url.split('/')[-2]
    if not response.ok:
        print('error %d getting job config: %s' % (response.status_code, url))
    else:
        with open(dir_name + f_name + '.xml', 'w') as output:
            output.write(response.content.decode())

        print(f_name)


def get_directory_list():
    """
    Получает список job'ов с главной страницы, 
    Данные job'ы должны быть типа Folder и содержать в себе все остальные job'ы
    """
    url_list = []
    response = requests.get(BASE_URL, auth=(USER, API_TOKEN))
    data = response.json()
    for job in data['jobs']:
        url_list.append(job['url'])
    return url_list


def get_job_list(urls):
    """
    Получает список url'ов на job'ы внутри Folder'а
    """
    job_url_list = []
    for url in urls:
        ur = url + 'api/json?pretty=true'
        response = requests.get(ur, auth=(USER, API_TOKEN))
        data = [response.json()]
        for inner_job in data:
            for job in inner_job['jobs']:
                job_url_list.append(job['url'])

    return job_url_list


def main():
    # Получаем список URL'ов на все вложенные job'ы
    urls = get_job_list(get_directory_list())
    for url in urls:
        # Проходимся по списку, получаем XML и сохраняем его на диск
        get_config_xml(url)


if __name__ == '__main__':
    main()
