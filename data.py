import random
import string
import os
import logging
from datetime import datetime
import pandas as pd

pd.set_option('display.max_columns', None)
CATEGORIES_ITEMS = {
        'Бытовая химия': ['Мыло', 'Шампунь', 'Гель для душа', 'Порошок стиральный', 'Средство для мытья посуды'],
        'Текстиль': ['Полотенце', 'Постельное белье', 'Скатерть', 'Шторы', 'Плед'],
        'Посуда': ['Тарелка', 'Чашка', 'Кастрюля', 'Сковорода', 'Нож'],
        'Продукты': ['Хлеб', 'Молоко', 'Сыр', 'Колбаса', 'Яблоки'],
        'Электроника': ['Наушники', 'Зарядное устройство', 'Мышь', 'Клавиатура', 'Флешка'],
    }
PRICE_RANGES = {
    'Бытовая химия': (100, 400),
    'Текстиль': (500, 3000),
    'Посуда': (250, 2500),
    'Продукты': (90, 350),
    'Электроника': (450, 2000),
}
shop_num = 5
cash_num = 4
max_items_per_check = 5


def random_doc_id(length=7):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


def generate_cash_file(shop, cash):
    items_list = [(good, categ) for categ, goods in CATEGORIES_ITEMS.items() for good in goods]
    num_records = random.randint(25, 60)
    data = {col: [] for col in ['doc_id', 'item', 'category', 'amount', 'price', 'discount']}
    for _ in range(num_records):
        doc_id = random_doc_id()
        num_items = random.randint(1, max_items_per_check)
        for _ in range(num_items):
            item, category = random.choice(items_list)
            amount = random.randint(1, 5)
            low, high = PRICE_RANGES.get(category)
            price = round(random.uniform(low, high), 2)
            if random.random() < 0.3:
                discount = round(price * random.uniform(0.05, 0.3), 2)
            else:
                discount = 0.0
            data['doc_id'].append(doc_id)
            data['item'].append(item)
            data['category'].append(category)
            data['amount'].append(amount)
            data['price'].append(price)
            data['discount'].append(discount)
    df = pd.DataFrame(data)
    folder_path = os.path.join(base_dir, 'data')
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f'{shop}_{cash}.csv')
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    logging.info(f'Создан файл {shop}_{cash}.csv, строк: {len(df)}')


base_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(base_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(log_dir, f"{datetime.now().date()}_data.log")
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
for shop in range(1, shop_num + 1):
    for cash in range(1, cash_num + 1):
        generate_cash_file(shop, cash)
