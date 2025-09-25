

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import csv

driver = webdriver.Chrome()

all_data = []

page = 1
while True:
    url = f"https://stylenewstar.com/collections/bag2?page={page}"
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "lxml")

    product_name_div = soup.find_all('div', class_='product-name-title')
    if not product_name_div:
        print(f"Страница {page} пуста. Останавливаемся.")
        break

    euro_prices = [
        span.get_text(strip=True)
        for span in soup.find_all("span", class_="product-new-price")
        if "€" in span.get_text()
    ]

    condition_divs = soup.find_all('div', class_='product-details-condition')
    conditions = [
        div.get_text(strip=True).replace("Condition:", "").strip()
        for div in condition_divs
    ]

    # --- Фото ---
    image_urls = []

    # находим все ссылки на товары
    product_links = soup.select("a[href^='/products/']")

# используем set, чтобы убрать дубли и только первая картинка
    seen_products = set()
    for link in product_links:
        href = link.get("href")
        if href in seen_products:
            continue  # пропускаем повторные ссылки на тот же товар
        seen_products.add(href)

        img_tag = link.find("img")
        if img_tag:
            src = img_tag.get("src")
            if src.startswith("//"):
                src = "https:" + src
            image_urls.append(
                src)
        else:
            image_urls.append("")

    # --- Названия ---
    product_name = [div.get_text(strip=True) for div in product_name_div]

    english_set = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    allowed_chars = english_set | set(" &-")

    cleaned_names = []
    for name in product_name:
        cleaned = ''.join(char for char in name if char in allowed_chars)
        cleaned = ' '.join(cleaned.split())
        cleaned = re.sub(r'\s*[A-Z0-9-]{1,4}$', '', cleaned)
        cleaned = re.sub(r'\s*[A-Z]{1,3}\s*[A-Z]{1,3}$', '', cleaned)
        cleaned = cleaned.strip(" -")
        cleaned_names.append(cleaned)

    # --- Берём минимальную длину ---
    min_len = min(len(cleaned_names), len(euro_prices), len(conditions), len(image_urls))

    # Добавляем в общий список
    for i in range(min_len):
        all_data.append([cleaned_names[i], euro_prices[i], conditions[i], image_urls[i]])

    print(f"✅ Собрали страницу {page}")
    page += 1

driver.quit()

# --- Сохраняем всё в CSV ---
with open("bags.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Наименование", "Цена", "Кондиция", "Фото"])
    writer.writerows(all_data)

print("🎉 Данные со всех страниц сохранены в bags.csv")



# from selenium import webdriver
# from bs4 import BeautifulSoup
# import time
# import re
# import csv

# driver = webdriver.Chrome()
# driver.get("https://stylenewstar.com/collections/bag2")
# time.sleep(3)  # ждём загрузку страницы

# soup = BeautifulSoup(driver.page_source, "lxml")

# # --- Названия ---
# product_name_div = soup.find_all('div', class_='product-name-title')
# product_name = [div.get_text(strip=True) for div in product_name_div]

# # --- Цены ---
# euro_prices = [
#     span.get_text(strip=True)
#     for span in soup.find_all("span", class_="product-new-price")
#     if "€" in span.get_text()
# ]

# # --- Кондиция ---
# condition_divs = soup.find_all('div', class_='product-details-condition')
# conditions = [
#     div.get_text(strip=True).replace("Condition:", "").strip()
#     for div in condition_divs
# ]

# # --- Фото: берём только первую картинку каждого товара ---
# # --- Фото: только первая картинка на товар ---
# image_urls = []

# # находим все ссылки на товары
# product_links = soup.select("a[href^='/products/']")

# # используем set, чтобы убрать дубли и только первая картинка
# seen_products = set()
# for link in product_links:
#     href = link.get("href")
#     if href in seen_products:
#         continue  # пропускаем повторные ссылки на тот же товар
#     seen_products.add(href)

#     img_tag = link.find("img")
#     if img_tag:
#         src = img_tag.get("src")
#         if src.startswith("//"):
#             src = "https:" + src
#         image_urls.append(f'=IMAGE("{src}")')
#     else:
#         image_urls.append("")



# # --- Очищаем названия ---
# english_set = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
# allowed_chars = english_set | set(" &-")

# cleaned_names = []
# for name in product_name:
#     cleaned = ''.join(char for char in name if char in allowed_chars)
#     cleaned = ' '.join(cleaned.split())
#     cleaned = re.sub(r'\s*[A-Z0-9-]{1,4}$', '', cleaned)
#     cleaned = re.sub(r'\s*[A-Z]{1,3}\s*[A-Z]{1,3}$', '', cleaned)
#     cleaned = cleaned.strip(" -")
#     cleaned_names.append(cleaned)

# # --- Берём минимальную длину ---
# min_len = min(len(cleaned_names), len(euro_prices), len(conditions), len(image_urls))

# # --- Собираем все данные ---
# all_data = []
# for i in range(min_len):
#     all_data.append([cleaned_names[i], euro_prices[i], conditions[i], image_urls[i]])

# driver.quit()

# # --- Сохраняем в CSV ---
# with open("bags.csv", "w", newline="", encoding="utf-8-sig") as f:
#     writer = csv.writer(f, delimiter=";")
#     writer.writerow(["Наименование", "Цена", "Кондиция", "Фото"])
#     writer.writerows(all_data)

# print("✅ Данные с первой страницы сохранены в bags.csv")
