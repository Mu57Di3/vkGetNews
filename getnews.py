# -*- coding: utf-8
# для работы надо создать в корне файл conf.json где сохранить данные авторизации и id приложения

import json, sys, redis
from mdutils import vkApi


class App:
    conf = None
    vkapi = None
    appId = None
    _redis = None

    def __init__(self, conf):
        self.vkapi = vkApi.Api(conf['login'], conf['password'], 'video,wall')
        self.appId = conf['appId']

    def getPosts(self, count):
        if self.appId:
            return self.vkapi.query('wall.get', 'owner_id=%s&count=%d&filter=owner' % (self.appId, count))
        else:
            return False

    def getRedis(self):
        if not self._redis:
            self._redis = redis.StrictRedis(host=self.conf['r_ip'], port=self.conf['r_port'], db=self.conf['r_base'])
            self._redis.auth(self.conf['r_auth'])
        else:
            self._redis.ping()
        return self._redis

    def parcePosts(self):
        posts = self.getPosts(3)
        posts = json.loads(posts)
        posts = posts['response']
        for post in posts:
            if not isinstance(post,dict):
                continue
            id = post['id']
            out_post = {
                'id': id,
                'message': post['text'],
                'dt': post['date'],
                'media': []
            }
            for item in post['attachments']:
                if item['type'] == 'photo':
                    img = ''
                    for key, value in item['photo'].iteritems():
                        if key.find('photo_') >=0 :
                            img = value
                    out_post['media'].append({'src': img, 'text': item['photo']['text']})
                elif item['type'] == 'video':
                    video = self.vkapi.query('video.get ', 'owner_id=%s&videos=%s' % (
                        item['video']['owner_id'],
                        str(item['video']['owner_id']) + '_' + str(item['video']['vid'])
                    ))
                    video = json.loads(video)
                    video = video['response']['items'][0]
                    out_post['media'].append({'src': video['player'], 'text': item['text']})

            #redis = self.getRedis()
            #redis.hset('magazine:posts', id, json.dump(out_post))
            print json.dumps(out_post)



if __name__ == "__main__":
    with open('conf.json') as f:
        conf = f.read()
    conf = json.loads(conf)
    App(conf).parcePosts()
