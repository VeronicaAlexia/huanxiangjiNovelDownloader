import os
import re
import sys
import HttpUtil


class Book:
    def __init__(self, book_id):
        self.book_url = 'http://www.huanxiangji.com/book/{}/'.format(book_id)
        self.book_info_html = HttpUtil.get(self.book_url)
        self.book_name = re.findall('<h1>(.*?)</h1>', self.book_info_html)[0]
        self.book_author = re.findall('<p>作者：(.*?)</p>', self.book_info_html)[0]
        self.book_state = re.findall('>状态：(.*?)</p>', self.book_info_html)[0]
        self.book_update = re.findall('<p>最后更新：(.*?)</p>', self.book_info_html)[0]
        if not os.path.exists("//config//"):
            os.mkdir("./config")

    def get_catalogue(self):
        download_url_list = list()
        catalogue_list = re.findall('<li><a href="(.*?)">(.*?)</a></li>', self.book_info_html)
        if catalogue_list:
            for i in catalogue_list:
                if i[0].endswith('.html') and i[0].replace(".html", "").isdigit():
                    download_url_list.append(i)
            return download_url_list
        return False

    def save_chapter(self, catalogue_info):
        for catalogue in catalogue_info:
            open("./novel/" + self.book_name + ".txt", 'w')
            chapter_file_name = catalogue[0].replace(".html", '.txt')
            if os.path.exists("./config/" + chapter_file_name):
                with open("./novel/" + self.book_name + ".txt", 'a', encoding='utf-8') as f:
                    with open("./config/" + chapter_file_name, 'r', encoding='utf-8') as f1:
                        f.write(f1.read())

    def get_context(self):
        chapter_info = self.get_catalogue()
        if not chapter_info or len(chapter_info) == 0:
            print("没有章节信息")
            return False
        for catalogue in chapter_info:
            chapter_id, chapter_name = catalogue[0], catalogue[1]
            if os.path.exists("./config/" + chapter_id.replace(".html", '.txt')):
                continue
            print("开始下载 : {}".format(chapter_name))
            content_html = HttpUtil.get(self.book_url + chapter_id)
            content_info = content_html.split('<div class="content" id="content">')[1].split('</div>')[0]
            content = re.sub('<br />', '\n', content_info).replace('&nbsp;', '').replace(" ", "").split('\n')
            content_text = chapter_name
            for line in content:
                if line.strip() != '':
                    content_text += "\n　　" + line
            with open("./config/" + chapter_id.replace(".html", '.txt'), 'w', encoding='utf-8') as f:
                f.write(content_text)
        return chapter_info


if __name__ == '__main__':
    book = Book(sys.argv[1])
    chapter_list = book.get_context()
    if chapter_list:
        book.save_chapter(chapter_list)
