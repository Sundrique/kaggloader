# import urllib2
# from bs4 import BeautifulSoup
#
# url = 'http://m.facebook.com'
#
# response = urllib2.urlopen(url)
#
# html = response.read()
#
# print response.info()
#
# soup = BeautifulSoup(html, "html.parser")
#
# form = soup.find('form', id='login_form')
#
# print form


#https://www.kaggle.com/c/the-allen-ai-science-challenge/download/training_set.tsv.zip
#https://www.kaggle.com/account/authenticate/facebook

import os
import getpass
import mechanize


def get_url(competition, file):
    return 'https://www.kaggle.com/c/' + competition + '/download/' + file


def rules_not_accepted(browser):
    return browser.geturl()[-6:] == '/rules'


def kaggle_not_logged_in(browser):
    return browser.geturl().find('https://www.kaggle.com/account/login') == 0


def is_login_form(form):
    return form.attrs.get('method') == 'post' and form.action.find('/login.php') != -1


def is_accept_rules_form(form):
    return form.action[-13:] == '/rules/accept'


def kaggle_accept_rules(browser):
    browser.select_form(predicate=is_accept_rules_form)
    browser.submit()


def kaggle_rules_not_accepted(browser):
    return browser.geturl()[-6:] == '/rules'


def kaggle_login_via_fb(browser):
    browser.follow_link(url_regex=r"facebook", nr=1)
    browser.select_form(predicate=is_login_form)
    browser['email'] = raw_input("Email: ")
    browser['pass'] = getpass.getpass()
    browser.submit()


def download(browser, competition, file_name):
    response = br.open(get_url(competition, file_name))

    if kaggle_not_logged_in(browser):
        kaggle_login_via_fb(browser)
        download(browser, competition, file_name)
    elif kaggle_rules_not_accepted(browser):
        kaggle_accept_rules(browser)
        download(browser, competition, file_name)
    else:
        dir = os.path.join(directory, competition)
        if not os.path.exists(dir):
            os.makedirs(dir)

        with open(os.path.join(directory, competition, file_name), 'wb') as f:
            f.write(response.read())


br = mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_robots(False)

directory = 'kaggloader'
cookie_file_name = '.cookies'
cookie_path = os.path.join(directory, cookie_file_name)

if not os.path.exists(directory):
    os.makedirs(directory)

if not os.path.exists(cookie_path):
    with open(cookie_path, 'w') as f:
        f.write('#LWP-Cookies-2.0')

cj = mechanize.LWPCookieJar()
cj.load(cookie_path, ignore_discard=False, ignore_expires=False)
opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cj))
mechanize.install_opener(opener)

br.set_cookiejar(cj)

br.addheaders = [('User-Agent',
                  'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4')]
#br.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56')]

#response = br.open('https://www.kaggle.com/account/authenticate/facebook')

#print response.info()

competition = 'the-allen-ai-science-challenge'
file_name = 'training_set.tsv.zip'

download(br, competition, file_name)

# response = br.open('https://www.kaggle.com/c/the-allen-ai-science-challenge/download/training_set.tsv.zip')
#
# print response.info()
#
# response = br.open('https://www.kaggle.com/c/the-allen-ai-science-challenge/download/training_set.tsv.zip')
# if kaggle_rules_not_accepted(br):
#     kaggle_accept_rules(br)
#
# print response.info()

#response = br.open('https://www.kaggle.com/c/the-allen-ai-science-challenge/download/training_set.tsv.zip')

#print response.info()

# br.open("https://m.facebook.com")
#
# assert br.viewing_html()
#

# response = br.open('https://www.kaggle.com/account/authenticate/facebook')
# #response = br.follow_link(predicate=is_eng_link)
# #print response.read()
#
# br.select_form(predicate=is_login_form)
# br['email'] = 'sundrique@gmail.com'
# br['pass'] = 'sxa2DhBkjxWJq3'
# response = br.submit()
# print br.request.header_items()


cj.save(cookie_path, ignore_discard=False, ignore_expires=False)