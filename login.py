import getpass


def facebook(browser):
    def is_fb_login_form(form):
        return form.attrs.get('method') == 'post' and form.action.find('/login.php') != -1

    browser.addheaders = [('User-Agent',
                        'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4')]

    browser.follow_link(url_regex=r"facebook", nr=1)
    browser.select_form(predicate=is_fb_login_form)
    browser.form['email'] = raw_input("Email: ")
    browser.form['pass'] = getpass.getpass()
    browser.submit()