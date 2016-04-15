# -*- coding: utf-8
# для работы надо создать в корне файл conf.json где сохранить данные авторизации и id приложения

import json, sys
from mdutils import vkApi


class App:
    vkapi = None
    appId = None

    def __init__(self, appid, login, password):
        self.vkapi = vkApi.Api(login, password, 'wall')
        self.appId = appid

    def getPosts(self, count):
        if self.appId:
            return self.vkapi.query('wall.get', 'owner_id=%s&count=%d&filter=owner' % (self.appId, count))
        else:
            return False


if __name__ == "__main__":
    with open('conf.json') as f:
        conf = f.read()
    conf = json.loads(conf)
    app = App(conf['appId'], conf['login'], conf['password'])
    print app.getPosts(10)
