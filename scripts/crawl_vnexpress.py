from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd
import random

# Cấu hình Selenium
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

# Trang chủ
home_url = "https://vnexpress.net"
driver.get(home_url)
print("Đang load trang chủ...")

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "wrapper-topstory-folder"))
    )
except:
    print("Lỗi load trang chủ!")
    driver.quit()
    exit()

soup_home = BeautifulSoup(driver.page_source, "html.parser")

# Lấy link bài báo từ top stories
article_links = []
top_section = soup_home.find("div", class_="wrapper-topstory-folder")
if top_section:
    for a in top_section.find_all("a", href=True):
        href = a["href"]
        if href.startswith("https://vnexpress.net/") and not any(
            x in href for x in ["/tag/", "/chu-de/", "/video/"]
        ):
            title = a.get("title") or a.get_text(strip=True)
            if title and href not in [link[0] for link in article_links]:
                article_links.append((href, title))

print(f"Tìm thấy {len(article_links)} bài báo nổi bật. Bắt đầu crawl full comment...")

all_data = []

for idx, (url, title) in enumerate(article_links, 1):
    print(f"\n[{idx}/{len(article_links)}] → {title} - {url}")

    driver.get(url)
    time.sleep(random.uniform(3, 6))

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "list_comment"))
        )
    except:
        print("  Bài này không có comment, bỏ qua.")
        continue

    # Load full comment bằng cách click "Xem thêm" đến hết
    last_count = 0
    while True:
        current_soup = BeautifulSoup(driver.page_source, "html.parser")
        current_comments = current_soup.find_all("div", class_="comment_item")
        current_count = len(current_comments)

        if current_count == last_count:
            print(f"  Đã load hết ({current_count} bình luận)")
            break

        last_count = current_count

        try:
            more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "show_more_coment"))
            )
            driver.execute_script("arguments[0].click();", more_button)
            print(f"  Click 'Xem thêm'... ({current_count})")
            time.sleep(random.uniform(2.5, 5))
        except:
            print(f"  Không còn nút → kết thúc ({current_count})")
            break

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Thời gian đăng bài
    date_tag = soup.find("span", class_="date")
    article_date = date_tag.get_text(strip=True) if date_tag else "Không tìm thấy"

    # Bình luận
    comments = soup.find_all("div", class_="comment_item")

    for cmt in comments:
        name_tag = cmt.find("a", class_="nickname")
        username = name_tag.get_text(strip=True) if name_tag else "Ẩn danh"

        content_tag = cmt.find("p", class_="full_content")
        content = content_tag.get_text(separator=" ", strip=True) if content_tag else ""
        if username != "Ẩn danh":
            content = content.replace(username, "", 1).strip()

        like_tag = cmt.find("a", class_="number")
        likes = (
            like_tag.get_text(strip=True)
            if like_tag and like_tag.get_text(strip=True).isdigit()
            else "0"
        )

        reply_tag = cmt.find("span", class_="num_reply_cmt")
        replies_num = reply_tag.get_text(strip=True) if reply_tag else "0"

        all_data.append(
            {
                "Tiêu đề bài báo": title,
                "Thời gian": article_date,
                "Khu Vực": "tp-ho-chi-minh",  # Mặc định cho tất cả
                "Người bình luận": username,
                "Nội dung": content,
                "Lượt thích": likes,
                "Phản hồi": replies_num,
            }
        )

driver.quit()

# Lưu Excel
if all_data:
    df = pd.DataFrame(all_data)
    df["Lượt thích"] = (
        pd.to_numeric(df["Lượt thích"], errors="coerce").fillna(0).astype(int)
    )
    df["Phản hồi"] = (
        pd.to_numeric(df["Phản hồi"], errors="coerce").fillna(0).astype(int)
    )

    # Đảm bảo thứ tự cột đúng: Khu Vực ở vị trí thứ 3 (sau Thời gian)
    column_order = [
        "Tiêu đề bài báo",
        "Thời gian",
        "Khu Vực",
        "Người bình luận",
        "Nội dung",
        "Lượt thích",
        "Phản hồi",
    ]
    df = df[column_order]

    filename = (
        f"tat_ca_binh_luan_vnexpress_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx"
    )
    df.to_excel(filename, index=False, engine="openpyxl")
    print(
        f"\nHOÀN TẤT! Đã lưu {len(all_data)} bình luận từ {len(article_links)} bài vào: {filename}"
    )
    print(
        "Cột 'Khu Vực' đã được thêm ở vị trí thứ 3 với giá trị mặc định 'tp-ho-chi-minh' cho tất cả."
    )
else:
    print("Không lấy được bình luận nào!")

print("Xong ạ!")
