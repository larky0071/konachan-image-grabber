from hurry.filesize import size
import requests
import shutil
import json
import time
import os

def create_dirs_if_not_exists():
    path_list = ['./data', './images', './json']
    for path in path_list:
        if not os.path.exists(path):
            os.makedirs(path)

def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')

def save_image_to_file(id, url):
    file_name = './images/' + str(id) + '.jpg'
    res = requests.get(url, stream = True)
    with open(file_name, 'wb') as f:
        shutil.copyfileobj(res.raw, f)

def save_image_info_to_file(id, data):
    with open('./json/' + str(id) + '.json', 'w') as f:
        json.dump(data, f, ensure_ascii = False, indent = 4)

def check_config_exists():
    return os.path.isfile('./data/data.json')

def create_config_file():
    with open('./data/data.json', 'w') as f:
        json.dump({'endpoint': 1, 'missing': []}, f, ensure_ascii = False, indent = 4)

def read_config_file():
    with open('./data/data.json', 'r') as f:
        return json.load(f)

def save_config_file(data):
    with open('./data/data.json', 'w') as f:
        json.dump(data, f, ensure_ascii = False, indent = 4)

def set_endpoint(post_id):
    config = read_config_file()
    config['endpoint'] = post_id
    save_config_file(config)

def get_endpoint():
    config = read_config_file()
    return config['endpoint']

def add_missing(post_id):
    config = read_config_file()
    config['missing'].append(post_id)
    save_config_file(config)

def __main__():
    create_dirs_if_not_exists()
    post_id = 1
    last_post_id = int(input("input last https://konachan.net post id: "))
    if check_config_exists():
        print('- read config')
        post_id = get_endpoint()
    else:
        print('- create config')
        create_config_file()
    while post_id <= last_post_id:
        url = 'https://konachan.net/post.json?tags=id:' + str(post_id)
        clear_console()
        print('- requesting ' + url)
        response = requests.get(url)
        if response:
            print('- request completed')
        else:
            print('- request failed')
            continue
        data = json.loads(response.text)
        print('- current post https://konachan.net/post/show/' + str(post_id))
        if len(data) == 0:
            print('- missing post')
            add_missing(post_id)
        else:
            post = data[0]
            if post['status'] == 'deleted':
                print('- post deleted')
            else:
                print('- downloading image')
                save_image_to_file(post['id'], post['file_url'])
            print('- storing info')
            save_image_info_to_file(post['id'], post)
        set_endpoint(post_id)
        post_id = post_id + 1

__main__()