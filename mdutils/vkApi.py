# -*- coding: utf-8

import cookielib, urlparse, json
from mechanize import Browser
from mechanize import _http


class Api:
    appid = '5415093'
    token = None
    query_pattern = 'https://api.vk.com/method/%s?%s&access_token='

    ua = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
    br = None
    cl = None

    def __init__(self, login, password, scope, testmode=False):
        self.br = Browser()
        self.cl = cookielib.LWPCookieJar()
        self.br.set_cookiejar(self.cl)

        self.br.set_handle_equiv(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(_http.HTTPRefreshProcessor(), max_time=1)
        self.br.addheaders = [('User-agent', self.ua)]

        self.br.open('https://oauth.vk.com/authorize?client_id=' + self.appid +
                     '&scope=' + scope + '&redirect_uri=http://oauth.vk.com/blank.html' +
                     '&display=mobile&response_type=token')

        self.br.select_form(nr=0)
        self.br.form['email'] = login
        self.br.form['pass'] = password
        self.br.submit()

        if len(list(self.br.forms())) > 0:
            self.br.select_form(nr=0)
            self.br.submit()

        params = urlparse.urlparse(self.br.geturl()).fragment
        params = params.split('&')

        for val in params:
            tp = val.split('=')
            if tp[0] == 'access_token':
                self.token = tp[1]
                self.query_pattern += self.token
                if testmode:
                    self.query_pattern += '&test_mode=1'
                break

    def query(self, func, data):
        response = self.br.open(self.query_pattern % (func, data))
        return response.read()
