from mysql.connector import connect, Error

import wikicrawling


def get_db_connection():
    return connect(host="localhost", user="rares", password="123456", database="states_db")


def query_select_top_10_desc_by_column(column_criteria):
    return f'SELECT * FROM states ORDER BY {column_criteria} DESC LIMIT 20'


def insert_rows(cursor, rows):
    query = """INSERT INTO states (wiki_url, population, time_zone, languages,
     currency, area_km2, government, 
     official_name, density_km2, capital_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.executemany(query, rows)


def insert_all_countries(cursor, db):
    rows = get_rows_of_db_from_spider()
    insert_rows(cursor, rows)
    db.commit()
    return cursor.rowcount


def row_to_string(row):
    result = ''
    for val in row:
        result += str(val) + ','
    return result[:-1]


def get_rows_of_db_from_spider():
    # with open('output.txt', 'a', encoding='utf-8') as the_file:
    rows = list()
    excluded = ['Transnistria']
    # indexes_no_col = [1, 4, 8]
    for link in wikicrawling.links_all:
        if link not in excluded:
            curr_info = wikicrawling.WikiCrawler.get_info_all_by_link(link)
            curr_row = [curr_info['wiki_url'], curr_info['population'], curr_info['time_zone'],
                        curr_info['languages'], 'not available', curr_info['area_km2'], curr_info['government'],
                        curr_info['official_name'], curr_info['density_km2'], curr_info['capital_name']]
            # the_file.write(row_to_string(curr_row) + '\n')
            rows.append(curr_row)
    return rows


def init_db():
    try:
        states_db = get_db_connection()
        cursor = states_db.cursor()
        rows_inserted_count = insert_all_countries(cursor, states_db)
        print('Rows inserted: ' + str(rows_inserted_count))
    except Error as e:
        print(e)


def top_10(column):
    query = query_select_top_10_desc_by_column(column)
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query)

    result = cursor.fetchall()
    return result


def get_query_match_info(column, info):
    column = column.lower()
    info = info.lower()

    if column == 'language' or column == 'languages':
        return f"SELECT * FROM states WHERE LOWER(languages) LIKE '%{info}%'"
    if column == 'time_zone' or column == 'timezone':
        return f"SELECT * FROM states WHERE LOWER(time_zone)='{info}'"
    if column == 'government' or column == 'politics':
        return f"SELECT * FROM states WHERE LOWER(government) LIKE '%{info}%'"
    if column == 'capital_name' or column == 'capitalname' or column == 'capital':
        return f"SELECT * FROM states WHERE LOWER(capital_name) LIKE '%{info}%'"


def all_match_info(column, info):
    db = get_db_connection()
    cursor = db.cursor()
    query = get_query_match_info(column, info)
    cursor.execute(query)

    result = cursor.fetchall()
    return result
