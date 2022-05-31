import os
import re
import sys
import HttpUtil


def write_file(path: str, mode: str = "a", content: str = ""):
    if mode == "r":
        return open(path, mode, encoding='utf-8').read()
    with open(path, mode, encoding='utf-8') as f:
        f.write(content)


class Book:
    def __init__(self, book_id):
        self.book_url = 'http://www.huanxiangji.com/book/{}/'.format(book_id)
        self.book_info_html = HttpUtil.get(self.book_url)
        self.book_name = re.findall('<h1>(.*?)</h1>', self.book_info_html)[0]
        self.book_author = re.findall('<p>作者：(.*?)</p>', self.book_info_html)[0]
        self.book_state = re.findall('>状态：(.*?)</p>', self.book_info_html)[0]
        self.book_update = re.findall('<p>最后更新：(.*?)</p>', self.book_info_html)[0]
        self.introduce = ""
        if not os.path.exists("./config"):
            os.mkdir("./config")
        if not os.path.exists("./novel"):
            os.mkdir("./novel")

    def show_book_information(self):
        self.introduce += "书名：{}\n".format(self.book_name)
        self.introduce += "作者：{}\n".format(self.book_author)
        self.introduce += "状态：{}\n".format(self.book_state)
        self.introduce += "最后更新：{}\n".format(self.book_update)
        self.introduce += "书籍地址：{}\n".format(self.book_url)
        print(self.introduce, "\n")

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
        write_file("./novel/" + self.book_name + ".txt", 'w', self.introduce)
        for catalogue in catalogue_info:
            chapter_file_name = catalogue[0].replace(".html", '.txt')
            if os.path.exists("./config/" + chapter_file_name):
                write_file(
                    "./novel/" + self.book_name + ".txt", 'a',
                    "\n\n\n" + write_file("./config/" + chapter_file_name, 'r')
                )
        self.introduce = ""

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
            content_text = chapter_name + ''.join(["\n　　" + line for line in content if line.strip() != ''])
            write_file("./config/" + chapter_id.replace(".html", '.txt'), 'w', content_text)
        return chapter_info


if __name__ == '__main__':
    try:
        book = Book(sys.argv[1])
        book.show_book_information()
        chapter_list = book.get_context()
        if chapter_list:
            book.save_chapter(chapter_list)
    except IndexError:
        print("请输入书籍ID")
