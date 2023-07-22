import urllib.request as req
import bs4
import concurrent.futures
import os

if os.path.exists("movie_concurrency.txt"):
    os.remove("movie_concurrency.txt")

def get_data(url):
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
    return root

def get_article_datetime(article_url):
    if article_url == "沒網址，本文恐已被刪除":
        return "沒網址沒時間"

    root = get_data(article_url)

    meta_divs = root.find_all("div", class_="article-metaline")

    article_datetime = ""

    for meta_div in meta_divs:
        tag_elem = meta_div.find("span", class_="article-meta-tag")

        if tag_elem.text.strip() == "時間":
            value_elem = meta_div.find("span", class_="article-meta-value")

            article_datetime = value_elem.text.strip()
            break

    return article_datetime

def write_data(index_url, page_count):
    
    root = get_data(index_url)
    titles = root.find_all("div", class_="title")

    article_urls = []

    for title in titles:
        if title.a is not None:
            article_urls.append("https://www.ptt.cc" + title.a["href"])
        else:
            article_urls.append("沒網址，本文恐已被刪除")

    article_datetime_dict = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_article_datetime, url) for url in article_urls]
        
        for future in concurrent.futures.as_completed(futures):
            article_datetime = future.result()
            article_datetime_dict.append(article_datetime)

    with open("movie_concurrency.txt", "a", encoding="utf-8") as file:
        file.write(f"=== 第 {page_count+1} 頁 ===\n")
        for i, title in enumerate(titles):
            if title.a is not None:
                title_text = title.a.string.strip()
            else:
                title_text = title.string.strip()
            
            push_count_elem = title.find_previous_sibling("div", class_="nrec")
            push_count = push_count_elem.span.string.strip() if push_count_elem.span is not None else "0"

            article_datetime = article_datetime_dict[i] if i < len(article_datetime_dict) else "沒欸"

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
