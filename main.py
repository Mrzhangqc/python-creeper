import requests

requests.packages.urllib3.disable_warnings()

from bs4 import BeautifulSoup
import sys
import time
import os
import imgkit
import xlwt

# import json
# from urllib.parse import parse_qs
# from wsgiref.simple_server import make_server


destop_path = "d:\\Users\\admin\\Desktop\\"
path = os.path.split(__file__)


def exportSSRDataFile(soup):
    data = soup.select("#main > article > div > table > tbody > tr > td.v2ray > a")
    if data:
        f = open(str(destop_path) + "ssr.txt", "w+")
        for label in data:
            f.write(label["data"] + "\n  ")
        f.close()
        print("导出文件到桌面文件ssr.txt")
        print("获取数据完成!")
    else:
        print("暂无数据")


def exportSSImage(soup):
    tableData = soup.select("#main > article > div > table")

    html_string = (
        """
    <html>
      <head>
        <meta content="png"/>
        <meta content="Landscape"/>
      </head>
      {tableString}
      </html>
    """
    ).format(tableString=tableData)

    output_file = destop_path + "screenshot.png"
    config = imgkit.config(
        wkhtmltoimage=r"H:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe"
    )

    try:
        exist_file = os.path.exists(output_file)
        if exist_file:
            os.remove(output_file)

        imgkit.from_string(html_string, output_file, config=config)
        print("截图成功")
    except IOError as e:
        print("截图失败:", e)


def exportIpDataFile(soup):
    trData = soup.select("#main > article > div > table > tbody > tr")
    dataLen = len(trData)
    if dataLen < 1:
        return ""

    file = destop_path + "server-list.xls"
    if os.path.exists(file):
        os.remove(file)

    wb = xlwt.Workbook()
    ws = wb.add_sheet("IP列表")

    head = ["IP", "端口", "密码", "加密", "协议", "混淆"]
    for i in range(len(head)):
        ws.write(0, i, head[i])

    for lineNum in range(dataLen):
        tr = trData[lineNum]
        cols = tr.find_all("td")
        for colNum in range(len(cols)):
            if colNum > 0:
                tdText = cols[colNum].get_text()

                ws.write(lineNum + 1, colNum - 1, tdText)

    wb.save(file)
    print("翻墙服务器列表, 导出成功!")


def getDataByType(t="ssr"):
    url = "https://fanqiang.network/"
    # 模拟浏览器访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36"
    }

    print("正在请求数据....")
    i = 0
    while i < 4:
        try:
            res = requests.get(url, headers=headers, timeout=10, verify=False)
        except requests.exceptions.ProxyError:
            i += 1
            if i == 4:
                break
            print("代理出错,正在重试..." + " 第" + str(i) + "次")
            time.sleep(3)
        except requests.exceptions.ConnectTimeout:
            i += 1
            if i == 4:
                break
            print("请求超时, 正在重试..." + " 第" + str(i) + "次")
            time.sleep(3)
        except requests.exceptions as e:
            print(e)
            break
        else:
            i = 4
            if res.status_code == 200:
                encoding = res.encoding
                target_encoding = res.apparent_encoding

                resultStr = res.text.encode(encoding).decode(target_encoding)
                # resultStr = res.text
                soup = BeautifulSoup(resultStr, "lxml")

                if t == "-t=ssr":
                    exportSSRDataFile(soup)
                elif t == "-t=img":
                    exportSSImage(soup)
                else:
                    exportIpDataFile(soup)
            else:
                print("爬取失败", res.status_code)


if __name__ == "__main__":
    argv = sys.argv
    t = ""
    if len(argv) > 1:
        t = argv[1]
    else:
        t = "-t=ssr"
    getDataByType(t)

##接口参数
# def application(environ, start_response):
#     start_response("200 OK", [("Content-Type", "text/html")])
#     params = parse_qs(environ["QUERY_STRING"])

#     ##得到网址中的参数
#     ssr = params["name"][0]
#     if ssr == "free":
#         return getSSRData()
#     else:
#         return [json.dumps({"err": "参数校验失败"}).encode("utf-8")]


# if __name__ == "__main__":
#     ##自定义开启的端口
#     port = 5088
#     httpd = make_server("0.0.0.0", port, application)
#     print("serving http on port {0}...".format(str(port)))
#     httpd.serve_forever()
