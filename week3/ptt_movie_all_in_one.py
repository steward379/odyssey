import urllib.request as req
import bs4
import os

if os.path.exists("movie.txt"):
    os.remove("movie.txt")

def get_data(url, page_count, type):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1 Edg/114.0.0.0",
        "Cookie": "over18=1"
    }
    req_obj = req.Request(url, headers=headers)

    try:
        with req.urlopen(req_obj) as res:
            data = res.read().decode("utf-8")

    except Exception as err:
        print(f"Error occurred: {err}")
        return None

    root = bs4.BeautifulSoup(data, "html.parser")
    print(f"抓到第 {page_count+1} 頁的 {type} 資料了")
    return root

def get_article_datetime(article_urls, page_count):
    article_datetime_dict = {}

    article_count = 0
    
    for article_url in article_urls:
        article_datetime = ""

        if article_url != "沒網址，本文恐已被刪除":
            root = get_data(article_url, page_count, "🖊️文章")

            meta_divs = root.find_all("div", class_="article-metaline")
            
            for meta_div in meta_divs:
                tag_elem = meta_div.find("span", class_="article-meta-tag")
                
                if tag_elem.text.strip() == "時間":
                    value_elem = meta_div.find("span", class_="article-meta-value")
                    article_datetime = value_elem.text.strip()
                    article_count += 1
                    break
        else:
            article_datetime = "沒網址沒法看時間"
            article_count += 1
        
        article_datetime_dict[article_url] = article_datetime
        print(f"抓到第{page_count+1} 頁第 {article_count} 篇時間",article_datetime)

    print(article_datetime_dict)
    return article_datetime_dict

def write_data(page_url, page_count):
    root = get_data(page_url, page_count, "👆主頁")

    titles = root.find_all("div", class_="title")

    article_urls = []
    for title in titles:
        if title.a is not None:
            article_urls.append("https://www.ptt.cc" + title.a["href"])
        else:
            article_urls.append("沒網址，本文恐已被刪除")

    article_datetime_dict = get_article_datetime(article_urls, page_count)

    with open("movie.txt", "a", encoding="utf-8") as file:
        file.write(f"=== 第 {page_count+1} 頁 ===\n")
        for i, title in enumerate(titles):
            if title.a is not None:
                title_text = title.a.string.strip()
            else:
                title_text = title.string.strip()
            
            push_count_elem = title.find_previous_sibling("div", class_="nrec")
            push_count = push_count_elem.span.string.strip() if push_count_elem.span is not None else "0"

            article_datetime = article_datetime_dict[article_urls[i]]

            print(f"第{page_count+1}頁第 {i + 1} 篇", title_text, push_count, article_datetime)
            file.write(f"{title_text},{push_count},{article_datetime}\n")

    nextLink = root.find("a", string="‹ 上頁")
    return nextLink["href"]

def write_page_data_into_txt():
    page_url = "https://www.ptt.cc/bbs/movie/index.html"
    page_limit = 3
    page_count = 0

    while page_count < page_limit:
        print(f"=== 第 {page_count+1} 頁 ===")
        page_url = "https://www.ptt.cc" + write_data(page_url, page_count)
        page_count += 1

write_page_data_into_txt()
