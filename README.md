# python-creeper
python 爬虫免费翻墙服务器

## 运行环境

- [Python 3](https://www.python.org/)

## 第三方库

- 需要使用到的库已经放在requirements.txt，使用pip安装的可以使用指令:  
`pip install -r requirements.txt`

## Usage

- 配置导出路径： `export_file_path`

- 配置截图工具安装路径：`wkhtmltoimage_binary_path`

- 开始之前检测代理是否已开启，开启代理后使用指令:  

`导出ssr文件：py main.py -t=ssr`  

`导出截图：py main.py -t=img`  

`导出可用服务器文件：py main.py -t=ip`  

