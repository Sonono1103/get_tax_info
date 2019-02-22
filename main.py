import sys
import csv
import urllib.request
import xml.etree.ElementTree as ET
import lxml
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from datetime import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv
import logging
from logging import getLogger, StreamHandler, DEBUG, Formatter
from time import sleep

####ログの設定####
logger = logging.getLogger(__name__)
#ファイルに出力
file_handler = logging.FileHandler('tax.log', encoding='utf-8')
file_handler.setLevel(DEBUG)
fhandler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(fhandler_format)
#ターミナルに出力
terminal_handler = logging.StreamHandler()
terminal_handler.setLevel(DEBUG)
thandler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
terminal_handler.setFormatter(thandler_format)

logger.setLevel(DEBUG)
logger.addHandler(file_handler)
logger.addHandler(terminal_handler)
logger.propagate = False


def main():
    if len(sys.argv) != 3:
            logger.error('usage: ./main.py <input_csv_file> <output_csv_file>')
            exit()

    #インプットされたファイルからイエローページID,法人番号を取得する
    #インプットファイルに行名がついていない場合はfor文の[1:]を削る
    inputdata = list(csv.reader(open(sys.argv[1], 'r')))
    corpnum_list = []
    yp_id = []
    for corp in inputdata[1:]:
        yp_id.append(corp[0])
        corpnum_list.append(corp[1])

    #同ディレクトリのenvファイルに入っているAPI_KEYを読み出す
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    api_key= os.environ.get("API_KEY")

    #法人番号をひとつずつ国税庁APIになげて会社名、所在地、取得日時を取得してリストをつくる
    index_num = 0
    corp_info_list = []
    good_count = 0 #正常に終了の数
    bad_count = 0  #異常ありの数
    for corpnum in corpnum_list:
        req = urllib.request.Request("https://api.houjin-bangou.nta.go.jp/3/num?id=" + api_key + "&number=" + corpnum + "&type=12")
        try:
            with urllib.request.urlopen(req) as response:
                XmlData = response.read()
        except urllib.error.HTTPError as err:
            logger.error('{0}  corpnum:{1}'.format(err.code, corpnum))
            bad_count += 1
            index_num += 1
            continue
        except urllib.error.URLError as err:
            logger.error('{0}  corpnum:{1}'.format(err.reason, corpnum))
            bad_count += 1
            index_num += 1
            continue
        
        #ここからパース。soup.<タグ名>.stringでタグに挟まれた部分を取る。
        soup = BeautifulSoup(XmlData, "xml")
        corp_info_list.append([yp_id[index_num], corpnum, \
            soup.find('name').string, " ".join([soup.prefectureName.string, soup.cityName.string, soup.streetNumber.string]), \
                datetime.now().strftime('%Y/%m/%d %H:%M:%S')])
        index_num += 1
        good_count += 1
        logger.info('進捗：正常終了{0}件　異常{1}件'.format(good_count, bad_count))

        sleep(1)

    #CSVファイルに出力
    #========windows encoding========#
    with open(sys.argv[2], 'w', newline='', encoding="utf-8_sig") as f:
        for corp_info in corp_info_list:
            writer = csv.writer(f)
            writer.writerow(corp_info)

if __name__ == "__main__":
    main()







