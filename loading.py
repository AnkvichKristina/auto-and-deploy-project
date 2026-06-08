import os
import re
import psycopg2
import logging
from datetime import datetime
from psycopg2.extras import execute_values
import pandas as pd
from config import DB_CONFIG

base_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(base_dir, 'logs')
DATA_DIR = os.path.join(base_dir, 'data')


def extract():
    pattern = re.compile(r'^\d+_\d+\.csv$')
    logging.info('Начало поиска файлов')
    csv_files = [file for file in os.listdir(DATA_DIR) if pattern.match(file)]
    logging.info(f'Найдено файлов: {len(csv_files)}')
    if not csv_files:
        logging.info('Файлы для загрузки не найдены')
        return None, []
    all_data = []
    try:
        for file in csv_files:
            file_path = os.path.join(DATA_DIR, file)
            df = pd.read_csv(file_path, encoding='utf-8')
            name = file.replace('.csv', '')
            shop_num, cash_num = map(int, name.split('_'))
            df['shop_num'] = shop_num
            df['cash_num'] = cash_num
            all_data.append(df)
        sales_df = pd.concat(all_data, ignore_index=True)
        return sales_df, csv_files
    except Exception as e:
        logging.error(f'Ошибка: {e}')
        return


def load(sales_df, csv_files):
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        cursor = conn.cursor()
        records = sales_df.values.tolist()
        execute_values(
            cursor,
            """
            INSERT INTO sales (
                doc_id,
                item,
                category,
                amount,
                price,
                discount,
                shop_num,
                cash_num
            )
            VALUES %s
            """,
            records
        )
        conn.commit()
        for file in csv_files:
            os.remove(os.path.join(DATA_DIR, file))
        logging.info('Файлы успешно обработаны и удалены')
        logging.info(f'Загружено строк: {len(sales_df)}')
    except Exception as e:
        conn.rollback()
        logging.error(f'Ошибка при загрузке в базу данных: {e}')
    finally:
        cursor.close()
        conn.close()


def main():
    os.makedirs(log_dir, exist_ok=True)
    log_filename = os.path.join(log_dir, f"{datetime.now().date()}_loading.log")
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    sales_df, csv_files = extract()
    if sales_df is None:
        return
    load(sales_df, csv_files)


if __name__ == '__main__':
    main()