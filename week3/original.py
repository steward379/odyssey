import urllib.request
import json
import csv
import os

if os.path.exists("mrt.csv"):
    os.remove("mrt.csv")

if os.path.exists("attractions.csv"):
    os.remove("attractions.csv")

url = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json'

with urllib.request.urlopen(url) as url:
    data = json.loads(url.read().decode())
    with open('attraction.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['景點名稱', '區域', '經度', '緯度', '第一張圖檔網址'])

        for attraction in data['result']['results']:
            district = attraction['address'].split('市')[1].split('區')[0].strip() + '區'
            first_image_url = "https://" + attraction['file'].split('https://')[1]
            writer.writerow([attraction['stitle'],  
                             district, 
                             attraction['longitude'], 
                             attraction['latitude'], 
                             first_image_url ])
    mrt_dict = {}


    # max_attractions = max(len(attraction['stitle']) 
    #                       for attraction in data['result']['results'])

    for attraction in data['result']['results']:
        mrt = attraction['MRT']
        if mrt is None:
             mrt_dict["沒有資料"] = [attraction['stitle']]
        elif mrt not in mrt_dict:
            mrt_dict[mrt] = [attraction['stitle']]
        else:
            mrt_dict[mrt].append(attraction['stitle'])


    max_attractions = max(len(attractions) for attractions in mrt_dict.values())

    with open('mrt.csv', 'w', newline='', encoding='utf-8') as mrt_file:
        writer = csv.writer(mrt_file)

        chinese_num = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一']

        writer.writerow(['捷運站名稱'] + ['景點名稱' + chinese_num[i] for i in range(max_attractions)])

        for mrt, attractions in mrt_dict.items():
            # writer.writerow([mrt, ", ".join(attractions)])
            writer.writerow([mrt] + attractions)
            