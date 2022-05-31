import os
import re

from zhconv import convert

import HttpUtil


class Book:
    def __init__(self, args):
        self.args = args
        self.book_url = 'http://www.huanxiangji.com/book/{}/'.format(self.args.id)
        self.book_info_html = HttpUtil.get(self.book_url)
        self.book_name = re.sub(r"[/\\:*?\"<>|]", "", re.findall('<h1>(.*?)</h1>', self.book_info_html)[0])
        self.book_author = re.findall('<p>作者：(.*?)</p>', self.book_info_html)[0]
        self.book_state = re.findall('>状态：(.*?)</p>', self.book_info_html)[0]
        self.book_update = re.findall('<p>最后更新：(.*?)</p>', self.book_info_html)[0]
        self.out_put_path = os.path.join(os.getcwd(), self.args.output, self.book_name + ".txt")
        self.introduce = ""

    def create_file(self):
        if not os.path.exists(os.path.join(os.getcwd(), "config", self.book_name)):
            os.makedirs(os.path.join(os.getcwd(), "config", self.book_name))
        if not os.path.exists(self.args.output):
            os.mkdir(self.args.output)
        write_file(self.out_put_path, 'w', self.introduce)

    def show_book_information(self):
        self.introduce += "书名：{}\n".format(self.book_name)
        self.introduce += "作者：{}\n".format(self.book_author)
        self.introduce += "状态：{}\n".format(self.book_state)
        self.introduce += "最后更新：{}\n".format(self.book_update)
        self.introduce += "书籍地址：{}\n".format(self.book_url)
        if self.args.show:
            print("书籍详细:\n" + self.introduce, "\n")
        else:
            print("开始下载:" + self.book_name)

    def get_catalogue(self):
        download_url_list = list()
        catalogue_list = re.findall('<li><a href="(.*?)">(.*?)</a></li>', self.book_info_html)
        if catalogue_list:
            for i in catalogue_list:
                if i[0].endswith('.html') and i[0].replace(".html", "").isdigit():
                    download_url_list.append(i)
            return download_url_list
        return False

    def get_context(self):
        chapter_info = self.get_catalogue()
        if not chapter_info or len(chapter_info) == 0:
            print("没有章节信息")
            return False
        for catalogue in chapter_info:
            chapter_id, chapter_name = catalogue[0], catalogue[1]
            if os.path.exists(os.path.join("config", self.book_name, chapter_id.replace(".html", '.txt'))):
                continue
            print("开始下载 : {}".format(chapter_name))
            content_html = HttpUtil.get(self.book_url + chapter_id)
            content_info = content_html.split('<div class="content" id="content">')[1].split('</div>')[0]
            content = re.sub('<br />', '\n', content_info).replace('&nbsp;', '').replace(" ", "").split('\n')
            content_text = chapter_name + ''.join(["\n　　" + line for line in content if line.strip() != ''])
            write_file(os.path.join("config", self.book_name, chapter_id.replace(".html", '.txt')), 'w', content_text)
        return chapter_info

    def save_chapter(self, catalogue_info):
        merge_text = []
        for catalogue in catalogue_info:
            chapter_file_name = catalogue[0].replace(".html", '.txt')
            if os.path.exists(os.path.join("config", self.book_name, chapter_file_name)):
                read_content = write_file(os.path.join("config", self.book_name, chapter_file_name), 'r')
                if self.args.traditional:
                    save_content = "\n\n\n" + convert(read_content, 'zh-hant')
                else:
                    save_content = "\n\n\n" + read_content
                write_file(path=self.out_put_path, content=save_content)
                merge_text.append(chapter_file_name)
        if merge_text:
            print(self.book_name, "本地缓存文件一共 {} 章, 已合并完毕".format(len(merge_text)))

def write_file(path: str, mode: str = "a", content: str = ""):
    if mode == "r":
        return open(path, mode, encoding='utf-8').read()
    with open(path, mode, encoding='utf-8') as f:
        f.write(content)
