import os

from bs4 import BeautifulSoup

import login
import mechanize


class KaggLoader(mechanize.Browser, object):
    BASE_DIR = 'kaggloader'
    COOKIE_FILE_NAME = '.cookies'
    COOKIE_PATH = os.path.join(BASE_DIR, COOKIE_FILE_NAME)
    HOST_NAME = 'www.kaggle.com'
    PROTOCOL = 'https'
    BASE_URL = PROTOCOL + '://' + HOST_NAME

    def __init__(self, login=login.facebook):
        super(KaggLoader, self).__init__()

        self.login = login

        self.set_handle_equiv(True)
        self.set_handle_robots(False)

        if not os.path.exists(self.BASE_DIR):
            os.makedirs(self.BASE_DIR)

        if not os.path.exists(self.COOKIE_PATH):
            with open(self.COOKIE_PATH, 'w') as f:
                f.write('#LWP-Cookies-2.0')

        self.cj = mechanize.LWPCookieJar()
        self.cj.load(self.COOKIE_PATH, ignore_discard=False, ignore_expires=False)
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(self.cj))
        mechanize.install_opener(opener)

        self.set_cookiejar(self.cj)

    def get_url(self, competition, file):
        return self.BASE_URL + '/c/' + competition + '/download/' + file

    def rules_not_accepted(self):
        return self.geturl()[-6:] == '/rules'

    def not_logged_in(self):
        return self.geturl().find(self.BASE_URL + '/account/login') == 0

    def is_accept_rules_form(self, form):
        return form.action[-13:] == '/rules/accept'

    def accept_rules(self):
        self.select_form(predicate=self.is_accept_rules_form)
        self.submit()

    def download(self, competition, file_name):
        response = self.open(self.get_url(competition, file_name))

        if self.not_logged_in():
            self.login(self)
            self.download(competition, file_name)
        elif self.rules_not_accepted():
            self.accept_rules()
            self.download(competition, file_name)
        else:
            dir = os.path.join(self.BASE_DIR, competition)
            if not os.path.exists(dir):
                os.makedirs(dir)

            with open(os.path.join(dir, file_name), 'wb') as f:
                f.write(response.read())

    def download_all(self, competition):
        for file in self.get_files(competition):
            self.download(competition, file)

    def open(self, url):
        response = super(KaggLoader, self).open(url)
        self.cj.save(self.COOKIE_PATH, ignore_discard=False, ignore_expires=False)
        return response

    def get_files(self, competition):
        self.open(self.BASE_URL + '/c/' + competition + '/data')

        soup = BeautifulSoup(self.response().read(), "html.parser")

        for anchor in soup.find('table', id='data-files').find_all('a'):
            yield anchor['href'].replace('/c/' + competition + '/download/', '')