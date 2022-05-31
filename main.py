import book
import argparse


def shell_parser():
    parser = argparse.ArgumentParser(
        description='huanxiangji小说下载器',
        usage='python main.py'
              '\n-i <book_id> [required]'
              '\n-t <true/false>'
              '\n-o <output_path>'
              '\n-s <true/false>',
        epilog='欢迎使用小说下载器，如果有问题请在Github提交Issues'
    )
    parser.add_argument('-i', '--id', help='书籍id', required=True)
    parser.add_argument('-t', '--traditional', default=False, help='繁体转换', action='store_true')
    parser.add_argument('-o', '--output', default="novel", help='保存到本地文件名')
    parser.add_argument('-s', '--show', default=True, help='不显示书籍信息', action='store_false')

    if not parser.parse_args().id.isdigit():
        print("书籍id必须是数字")
    else:
        book_config = book.Book(args=parser.parse_args())
        book_config.show_book_information()
        book_config.create_file()
        chapter_list = book_config.get_context()
        if chapter_list:
            book_config.save_chapter(chapter_list)
        else:
            print("没有获取到任何章节信息，下载失败！")


if __name__ == '__main__':
    try:
        shell_parser()
    except KeyboardInterrupt:
        print("\n\nCtrl+C 退出程序成功")
    except Exception as error:
        print(error)
