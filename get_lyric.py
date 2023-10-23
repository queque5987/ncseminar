from bs4 import BeautifulSoup as bp
import requests
from urllib import parse
import time
import re
import os

header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"}
groups = ["트와이스", "아이브", "아이즈원", "블랙핑크", "뉴진스", "르세라핌", "방탄소년단"]

if __name__ == "__main__":
    for group in groups:
        group_name = parse.quote(group)
        res = requests.get(f"https://www.melon.com/search/total/index.htm?q={group_name}&section=&mwkLogType=T", headers=header)
        soup = bp(res.text, 'html.parser')
        fc_gray = soup.findAll("a", title = "곡정보 보기")
        for i, fc_gray_iter in enumerate(fc_gray):
            if i >= 10: break
            song_name = fc_gray_iter.text.replace("상세정보 페이지 이동", "").strip()
            song_name = re.sub(r"[^a-zA-Z0-9가-힣 \n]", '', song_name)
            match = re.search(r'goSongDetail\(\'(\d+)\'\)', str(fc_gray_iter['href']))
            if match:
                song_id = match.group(1)
                res = requests.get(f"https://www.melon.com/song/detail.htm?songId={song_id}", headers=header)
                soup = bp(res.text, 'html.parser')
                lyric = str(soup.find("div", id = "d_video_summary"))
                lyric = lyric.replace("<br/>", "\n")
                lyric = re.sub(r'<[^>]+>', '', lyric).strip()
                if not os.path.isdir(f"output/{group}"):
                    os.mkdir(f"output/{group}")
                with open(f"output/{group}/{song_name}.txt", "w", encoding="utf-8") as f:
                    f.writelines(lyric)
                time.sleep(0.05)
        time.sleep(0.05)