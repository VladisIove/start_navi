import json 
import os
import random
import string
import jwt
import base64
import requests

class Bot:
    users_info = []
    posts_id = []

    def __init__(self, file_name):
        data = self._parser(file_name)
        self.number_of_users = data['number_of_users']
        self.max_posts_per_user = data['max_posts_per_user']
        self.max_likes_per_user = data['max_likes_per_user']


    def _parser(self, file_name):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) 
        with open(os.path.join(__location__, file_name)) as json_file:
            data = json.load(json_file)
        return data
    
    def _random_char(self, y):
       return ''.join(random.choice(string.ascii_letters) for _ in range(y))

    def _make_request(self, url, data, headers):
        response = requests.post(url=url, data=data, headers=headers, verify=False)
        return response.json()

    def create_users(self):
        for _ in range(self.number_of_users):
            data = self._make_request(url='http://127.0.0.1:5000/signup', 
                                        data=json.dumps({
                                        'email': '{}@gmail.com'.format(self._random_char(7)),
                                        'password': self._random_char(14)}),
                                        headers={
                                            'Content-Type': 'application/json'
                                        }
                                    )
        
            self.users_info.append({
                'id': data['user_id']  ,
                'token': data['token'] , 
            })
            
    def create_posts(self):
        for user_info in self.users_info:
            for _ in range(self.max_posts_per_user):
                text = self._random_char(55)
                data_request = {
                                'text': text,
                                'author_id': user_info['id']
                                }
                data = self._make_request(url='http://127.0.0.1:5000/createPost',
                                            data=json.dumps(data_request),
                                            headers={
                                                'Content-Type': 'application/json',
                                                'Authorization': 'Bearer {}'.format(user_info['token'])
                                            })
                self.posts_id.append(
                    data['id']
                )

    def like_posts(self):
        for user_info in self.users_info:
            for _ in range(self.max_likes_per_user):
                post_id = random.choice(self.posts_id) 
                data_request = {
                                'user_id': user_info['id'],
                                'post_id': post_id
                                }
                data = self._make_request(url='http://127.0.0.1:5000/likePost',
                                            data=json.dumps(data_request),
                                            headers={
                                                'Content-Type': 'application/json',
                                                'Authorization': 'Bearer {}'.format(user_info['token'])
                                            })

if __name__ == "__main__":
    bot = Bot('config.json')
    bot.create_users()
    bot.create_posts()
    bot.like_posts()
    print('Finish')