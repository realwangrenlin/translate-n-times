import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import random
import time


class Main_translate(object):

    def __init__(self, text, times):
        self.options = Options()
        pref = {
            'profile.default_content_setting_values': {
                'images': 2,
            },
        }
        self.options.add_experimental_option("prefs", pref)
        self.driver = selenium.webdriver.Chrome(options=self.options)
        self.text = text
        self.html = ''
        self.result = ''
        self.languages = ['af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs',
                          ' bg', 'ca', 'ceb', 'ny', 'zh-TW', 'co', 'hr', 'cs',
                          'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy', 'gl',
                          'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn',
                          'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'km',
                          'rw', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk',
                          'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no',
                          'or', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd',
                          'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su',
                          'sw', 'sv', 'tg', 'ta', 'tt', 'te', 'th', 'tr', 'tk', 'uk',
                          'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu']
        self.wait = WebDriverWait(self.driver, 20)
        self.history_result = []
        self.times = times

    def process_text(self):
        text2 = ''
        for i in self.text:
            text2 += i.replace('\n', '')
        self.text = text2

    def input_content(self, target):
        self.driver.get(
            f'https://translate.google.cn/#view=home&op=translate&sl=auto&tl={target}&text={self.text}')
        if len(self.history_result) >= 1:
            while self.history_result[-1] in self.select_result(check_exist=True):
                self.html = self.driver.page_source
                time.sleep(0.1)
        self.html = self.driver.page_source

    def proccess_html(self, span):
        if len(span) > 1:
            final_str = ''
            for i in span:
                final_str += i.string.replace('<span title="">', '').replace('</span>', '')
            self.result = final_str
        else:
            for i in span:
                self.result = i.string.replace('<span title="">', '').replace('</span>', '')

    def select_result(self, check_exist):
        soup = BeautifulSoup(self.html, 'html.parser')
        span = soup.select('.translation > span')
        if span:
            self.proccess_html(span)
        else:
            span = soup.select('.tlid-copy-target>.result-shield-container>span:first-child')
            self.proccess_html(span)
        if check_exist:
            return self.result
        else:
            self.history_result.append(self.result)

    def start(self):
        self.process_text()
        history_choice = []
        for i in range(int(self.times) - 2):
            choice = random.choice(self.languages)
            if len(history_choice) >= 1:
                while history_choice[-1] == choice:
                    choice = random.choice(self.languages)
            history_choice.append(choice)
            self.input_content(choice)
            self.select_result(check_exist=False)
            self.text = self.result
            print(i + 2)
        self.input_content('zh-CN')
        self.select_result(check_exist=False)
        print(self.times)
        print(history_choice)


if __name__ == '__main__':
    times = input('请输入次数:\n')
    f = open('./input_text.txt', encoding='utf-8')
    text = f.readlines()
    f.close()
    print('启动中')
    main_translate = Main_translate(text=text, times=times)
    main_translate.start()
