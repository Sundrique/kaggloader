import getpass
import os

import mechanize


class KaggLoader(mechanize.Browser, object):
    BASE_DIR = 'kaggloader'
    COOKIE_FILE_NAME = '.cookies'
    COOKIE_PATH = os.path.join(BASE_DIR, COOKIE_FILE_NAME)

    def __init__(self):
        super(KaggLoader, self).__init__()

        self.set_handle_equiv(True)
        self.set_handle_robots(False)

        self.addheaders = [('User-Agent',
                            'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4')]

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
        return 'https://www.kaggle.com/c/' + competition + '/download/' + file

    def rules_not_accepted(self):
        return self.geturl()[-6:] == '/rules'

    def not_logged_in(self):
        return self.geturl().find('https://www.kaggle.com/account/login') == 0

    def is_login_form(self, form):
        return form.attrs.get('method') == 'post' and form.action.find('/login.php') != -1

    def is_accept_rules_form(self, form):
        return form.action[-13:] == '/rules/accept'

    def accept_rules(self):
        self.select_form(predicate=self.is_accept_rules_form)
        self.submit()

    def login_via_fb(self):
        self.follow_link(url_regex=r"facebook", nr=1)
        self.select_form(predicate=self.is_login_form)
        self.form['email'] = raw_input("Email: ")
        self.form['pass'] = getpass.getpass()
        self.submit()

    def download(self, competition, file_name):
        response = self.open(self.get_url(competition, file_name))

        if self.not_logged_in():
            self.login_via_fb()
            self.download(file_name)
        elif self.rules_not_accepted():
            self.accept_rules()
            self.download(file_name)
        else:
            dir = os.path.join(self.BASE_DIR, competition)
            if not os.path.exists(dir):
                os.makedirs(dir)

            with open(os.path.join(dir, file_name), 'wb') as f:
                f.write(response.read())

    def open(self, url):
        response = super(KaggLoader, self).open(url)
        self.cj.save(self.COOKIE_PATH, ignore_discard=False, ignore_expires=False)
        return response