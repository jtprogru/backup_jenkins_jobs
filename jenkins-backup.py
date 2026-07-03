#!/usr/bin/env python3

import logging
import os
import sys

import requests

logging.captureWarnings(True)

# Конфигурация через переменные окружения
SERVER = os.environ.get("JENKINS_SERVER")
API_TOKEN = os.environ.get("JENKINS_API_KEY")
USER = os.environ.get("JENKINS_USER")
JOBS_DIR = os.environ.get("JENKINS_JOBS_DIR", "jenkins_jobs/")
BASE_URL = f"https://{SERVER}/api/json?pretty=true"

REQUEST_TIMEOUT = 30


def get_config_xml(url):
    """
    Выполняется запрос к API Jenkins и получает файл в формате XML,
    который записывается на диск
    """
    dir_name = os.path.join(JOBS_DIR, url.split('/')[-4])
    url += 'config.xml'
    response = requests.get(url, auth=(USER, API_TOKEN), timeout=REQUEST_TIMEOUT)
    os.makedirs(dir_name, exist_ok=True)
    f_name = url.split('/')[-2]
    if not response.ok:
        print('error %d getting job config: %s' % (response.status_code, url))
    else:
        with open(os.path.join(dir_name, f_name + '.xml'), 'w') as output:
            output.write(response.text)

        print(f_name)


def get_directory_list():
    """
    Получает список job'ов с главной страницы,
    Данные job'ы должны быть типа Folder и содержать в себе все остальные job'ы
    """
    url_list = []
    response = requests.get(BASE_URL, auth=(USER, API_TOKEN), timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
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
        response = requests.get(ur, auth=(USER, API_TOKEN), timeout=REQUEST_TIMEOUT)
        data = response.json()
        for job in data.get('jobs', []):
            job_url_list.append(job['url'])

    return job_url_list


def main():
    missing = [name for name, value in (
        ("JENKINS_SERVER", SERVER),
        ("JENKINS_USER", USER),
        ("JENKINS_API_KEY", API_TOKEN),
    ) if not value]
    if missing:
        sys.exit(f"missing required environment variables: {', '.join(missing)}")

    # Получаем список URL'ов на все вложенные job'ы
    urls = get_job_list(get_directory_list())
    for url in urls:
        # Проходимся по списку, получаем XML и сохраняем его на диск
        get_config_xml(url)


if __name__ == '__main__':
    main()
