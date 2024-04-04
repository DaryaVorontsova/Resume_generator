from jinja2 import Template
from datetime import datetime

import requests
import os
import dotenv

TEMPLATE_NAME = './templates/index.html'
INDEX_PUBLIC_NAME = "./public/index.html"

def get_vk_data():

    access_token_vk = os.getenv('TOKEN')
    user_id = os.getenv('ID')  
    api_version = os.getenv('API_VERSION')

    url_vk = f'https://api.vk.com/method/account.getProfileInfo?user_ids={user_id}&access_token={access_token_vk}&v={api_version}'

    response = requests.get(url_vk)

    name = ''
    surname = ''
    birthday = ''
    city = ''
    vk_id = ''

    if response.status_code == 200:
        data = response.json()
        name = data['response']['first_name']
        surname = data['response']['last_name']
        birthday = data['response']['bdate']
        city = data['response']['city']['title']
        vk_id = data['response']['screen_name']
    
    return(name, surname, birthday, city, vk_id)

def get_git_data():

    access_token_git = os.getenv("TOKENGIT")
    username = os.getenv("USERNAMEGIT")
    url_git = f'https://api.github.com/users/{username}/repos'
    headers = {'Authorization': f'token {access_token_git}'}

    response = requests.get(url_git, headers=headers)

    experience = ''
    numb_public_repos = ''
    ava = ''
    names_repos = []
    
    if response.status_code == 200:
        data_git = response.json()
        experience = data_git[0]['owner']['html_url']
        ava = data_git[0]['owner']['avatar_url']

        for item in data_git:
            repos = item["name"]
            leng = item["language"]
            desc = item["description"]
            names_repos.append({"name": repos, "language": leng, "description": desc})      

    return(experience, ava, names_repos)

def create_resume_():
    
    dotenv.load_dotenv()
    name, surname, birthday, city, vk_id = get_vk_data()
    experience, ava, names_repos = get_git_data()
    
    with open(TEMPLATE_NAME, "r", encoding="utf-8") as template_file:
        template_data = template_file.read()
        jinja_template = Template(template_data)
        rendered_file_resume = jinja_template.render(
            name_person = name,
            surname_person = surname,
            birthday_person = birthday,
            city_person = city,
            vk_id_person = vk_id,
            link_github = experience,
            avatar_url = ava,
            my_repositories = names_repos,
            datetime = datetime.now()
        )
        with open(INDEX_PUBLIC_NAME, 'w', encoding="utf-8") as resume:
            resume.write(rendered_file_resume)
    return rendered_file_resume