import requests
from bs4 import BeautifulSoup
from queue import Queue
import os


class Func:
    @staticmethod
    def handleURL(url: str):
        ulist = url.replace(
            "http://", "").replace("https://", "").replace(':', '_').replace(".bjtu.edu.cn", "").split('/')
        if len(ulist) == 1:
            return ulist
        else:
            return ulist[:-1]

    @staticmethod
    def chdir(url: list):
        os.chdir(Crawler.Path)
        for uu in url:
            if os.path.exists(uu):
                pass
            else:
                os.mkdir(uu)
            os.chdir(uu)

    @staticmethod
    def getFileName(url: str):
        cnt = 0
        for c in url:
            if c == '/':
                cnt += 1
        if cnt == 2:
            return "index.html"

        name = url.split('/')[-1].split('?')[0]
        if len(name) == 0:
            return "index.html"
        else:
            suffix = name.split('.')[-1]
            if suffix == 'htm':
                return name + 'l'
            else:
                return name

    @staticmethod
    def formatURL(label: str):
        try:
            index = label.find("href")
            if index == -1:
                return None
            tag = 0
            for i in range(index, len(label)):
                if tag == 1 and label[i] == '"':
                    r = i
                    break
                if tag == 0 and label[i] == '"':
                    tag = 1
                    l = i+1
            return label[l:r]
        except UnboundLocalError:
            print(label)

    @staticmethod
    def check(file_name: str):
        t = str(file_name.split('.')[-1])
        if t == 'html' or t == 'aspx':
            return True
        else:
            return False


class Crawler:
    Path = ""

    def __init__(self):
        print("Starting...")
        self.seed = "http://www.bjtu.edu.cn"
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*"
        }
        Crawler.Path = os.getcwd() + "/bjtu.edu.cn"
        self.urlpool = Queue(maxsize=0)
        self.vispool = {}
        self.listpool = {}
        if os.path.exists(Crawler.Path):
            print("爬虫存储文件夹已存在")
        else:
            os.mkdir(Crawler.Path)
            print("已于" + Crawler.Path + "创建爬虫存储文件夹")

    def getHTML(self, url):
        try:
            print("Current Request URL: " + url)
            tmp = requests.get(url, headers=self.header, timeout=6)
        except Exception:
            print("连接超时 跳过该网页")
            return None
        tmp.encoding = tmp.apparent_encoding
        if tmp.status_code != 200:
            return None

        content_type = tmp.headers["Content-Type"].split(';')
        if "text/html" in content_type:
            return tmp.text
        else:
            return None

    # 主函数太丑啦啊啊啊啊
    def main(self):
        log = open(
            Crawler.Path + "/craw.log", "w", encoding="utf-8")
        structure = open(Crawler.Path + "/structure.txt",
                         "w", encoding="utf-8")
        self.urlpool.put(self.seed)
        self.vispool[self.seed] = 1
        t = Func.handleURL(self.seed)
        t.append(Func.getFileName(self.seed))
        self.listpool[self.seed] = t

        while self.urlpool.qsize() != 0:
            current_url = self.urlpool.get()
            print("\nCurrent URL: " + current_url)
            current_url_list = self.listpool.get(current_url)
            current_file_name = current_url_list[-1]

            print("Current URL list: " + "/".join(current_url_list))
            current_html = self.getHTML(current_url)

            if current_html == None:
                print("Some Error Happend")
                continue

            current_url_list = current_url_list[:-1]
            Func.chdir(current_url_list)
            if os.path.exists(current_file_name):
                print("File exists. Jump to next.")
                continue
            f = open(current_file_name, "w", encoding="utf-8")
            f.write(current_html)
            f.close()

            log.write('/'.join(current_url_list) +
                      '/' + current_file_name + '\n')
            structure.write('/'.join(current_url_list) + '/' +
                            current_file_name + '\n')
            soup = BeautifulSoup(current_html, "html.parser")

            all_url_list = map(str, soup.findAll('a'))
            for nxt_url in all_url_list:
                nurl = Func.formatURL(nxt_url)

                if nurl == None or len(nurl) == 0 or nurl.lower().find("javascript") != -1:
                    continue

                if nurl[0:4] != "http":
                    if nurl[0] != '/':
                        nurl = '/' + nurl
                    nurl = "http://" + current_url.split('/')[2] + nurl

                nxt_url_list = Func.handleURL(nurl)
                nxt_url_list.append(Func.getFileName(nurl))

                if Func.check(nxt_url_list[-1]) == True:
                    log.write('-')
                    log.write('/'.join(nxt_url_list) + '\n')
                    if self.vispool.get(nurl) == None:
                        self.urlpool.put(nurl)
                        self.vispool[nurl] = 1
                        self.listpool[nurl] = nxt_url_list


if __name__ == "__main__":
    crawler = Crawler()
    try:
        crawler.main()
    except KeyboardInterrupt:
        print("爬虫程序提前中止，请于 " + Crawler.Path + " 查看已下载的网页")
