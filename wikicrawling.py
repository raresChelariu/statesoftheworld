from urllib.request import urlopen as url_req
from bs4 import BeautifulSoup as soup
import re
import json


class InfoProcessing:
    @staticmethod
    def list_to_json(given_list):
        return json.dumps(given_list)

    @staticmethod
    def find_row_by_keyword(rows, keyword):
        for row in rows:
            if keyword in row.get_text():
                return row.get_text()
        return f'Nonexistent keyword : {keyword}'

    @staticmethod
    def get_row_index(rows, keyword):
        for i in range(len(rows)):
            if keyword in rows[i].get_text():
                return i
        return -1

    @staticmethod
    def get_row_rindex(rows, keyword):
        idx = 0
        for i in range(len(rows)):
            if keyword in rows[i].get_text():
                idx = i
        return idx

    @staticmethod
    def process_currency(table_rows):
        def remove_parentheses(txt):
            while True:
                start = txt.find('(')
                end = txt.find(')')
                if start == -1 or end == -1:
                    break
                txt = txt[start + 1:end]
                return txt

        keyword = 'Currency'
        index = InfoProcessing.get_row_index(table_rows, keyword)
        input_txt = table_rows[index].get_text() + ''
        if input_txt.startswith(keyword):
            input_txt = input_txt[len(keyword):]
        return remove_parentheses(input_txt)

    @staticmethod
    def process_population(table_rows):
        keyword = 'Population'
        index = InfoProcessing.get_row_index(table_rows, keyword)

        input_text = '' + table_rows[index + 1].find('td').get_text()

        given = input_text.strip()
        for i in range(len(given)):
            if given[i].isdigit():
                given = given[i:]
                break
        for i in range(len(given)):
            if not given[i].isdigit() and given[i] != ',':
                given = given[:i]
                break

        result = given.replace(',', '')
        # return result
        return int(result)

    @staticmethod
    def process_language(table_rows):
        keyword = 'language'
        index = InfoProcessing.get_row_index(table_rows, keyword)
        input_txt = '' + table_rows[index].find('td').get_text()
        if input_txt.find('[') != -1:
            input_txt = input_txt[:input_txt.index('[')]
        left_index = 1 if input_txt[0] == '\n' else 0
        input_txt = input_txt[left_index:-1] if input_txt[-1] == '\n' else input_txt[left_index:]
        languages = re.findall('[A-Z][^A-Z]*', input_txt.replace('\n', ''))
        # return languages
        return InfoProcessing.list_to_json(languages)

    @staticmethod
    def process_timezone(table_rows):
        keyword = 'Time zone'
        index = InfoProcessing.get_row_index(table_rows, keyword)
        input_txt = table_rows[index].get_text() + ''
        start_index = input_txt.find("UTC") + len("UTC")
        utc_char = '+' if input_txt[start_index] == '+' else '-'
        start_index += 1
        utc_no = ''
        input_txt = input_txt[start_index:]
        for curr_char in input_txt:
            if curr_char.isdigit() or curr_char == ':':
                utc_no += curr_char
        return "UTC" + utc_char + utc_no

    @staticmethod
    def process_capital(table_rows):
        def actual_city(city_name):
            return "de jure" not in city_name and "de facto" not in city_name

        def row_is_ul_list(row):
            if row.find('td') is not None:
                my_td = table_rows[index].find('td')
                if my_td.find('div') is not None:
                    my_div = my_td.find('div')
                    if my_div.find('ul') is not None:
                        return my_div.find('ul')
            return None

        keyword = 'Capital'
        word_largest = 'and largest city'
        index = InfoProcessing.get_row_index(table_rows, keyword)

        my_ul = row_is_ul_list(table_rows[index])
        if my_ul is not None:
            print('we got here :D')
            all_cities_li = my_ul.find_all('li')
            for item in all_cities_li:
                if actual_city(item.find('a').get_text()):
                    return item.find('a').get_text()

        input_txt = table_rows[index].get_text() + ''
        if word_largest in input_txt:
            input_txt = input_txt[input_txt.find(word_largest) + len(word_largest):]
        else:
            input_txt = input_txt[input_txt.find(keyword) + len(keyword):]
        result = ''
        for curr_char in input_txt:
            if curr_char.isalpha() or curr_char == ' ':
                result += curr_char
            else:
                break
        return result

    @staticmethod
    def process_area(table_rows):
        keyword = 'Area'
        keyword2 = 'km'
        index = 0
        for i in range(len(table_rows)):
            if keyword in table_rows[i].get_text() and keyword2 in table_rows[i+1].get_text():
                index = i
                break

        input_txt = table_rows[index + 1].get_text() + ''
        start_idx = 0
        for i in range(len(input_txt)):
            if input_txt[i].isdigit():
                start_idx = i
                break

        last_idx = start_idx
        for i in range(start_idx, len(input_txt)):
            if not input_txt[i].isdigit() and not input_txt[i] == ',':
                last_idx = i
                break
        result = input_txt[start_idx:last_idx] + ''
        result = result.replace(',', '')
        # return result + '@@@' + input_txt
        # return result
        return float(result)

    @staticmethod
    def process_official_name(table_rows):
        input_txt = table_rows[0].find('th').find('div').get_text()
        return input_txt

    @staticmethod
    def process_government(table_rows):
        keyword = 'Government'
        index = InfoProcessing.get_row_rindex(table_rows, keyword)
        # input_txt = table_rows[index].find('td').find_all('a')[-1].get_text()
        input_txt = table_rows[index].find('td').find_all('a')
        govs = list()
        for gov_row in input_txt:
            if gov_row.get_text()[0] != '[':
                govs.append(gov_row.get_text())

        # return govs
        return InfoProcessing.list_to_json(govs)

    @staticmethod
    def process_density(table_rows):
        keyword = 'Density'
        index = InfoProcessing.get_row_index(table_rows, keyword)
        if index == -1:
            return 0
        input_txt = table_rows[index].find('td').get_text()
        start_idx = 0
        for i in range(len(input_txt)):
            if input_txt[i].isdigit():
                start_idx = i
                break

        input_txt = input_txt[start_idx:]
        end_idx = start_idx
        for i in range(len(input_txt)):
            if input_txt[i] in '/[ ':
                end_idx = i
                break
        input_txt = input_txt[:end_idx]
        input_txt = input_txt.replace(',', '')
        # return input_txt
        return float(input_txt)


def crawl_info_from_link_country(link_country):
    page_soup = get_soup_for_link(link_country)
    table_rows = page_soup. \
        find('div', {"id": "content"}). \
        find('div', {"id": "bodyContent"}). \
        find('div', {"id": "mw-content-text"}). \
        find('table', {"class": "infobox geography vcard"}).find('tbody').find_all('tr')

    info = dict()
    info['wiki_url'] = link_country
    info['population'] = InfoProcessing.process_population(table_rows)
    info['time_zone'] = InfoProcessing.process_timezone(table_rows)
    info['languages'] = InfoProcessing.process_language(table_rows)
    info['currency'] = InfoProcessing.process_currency(table_rows)
    info['area_km2'] = InfoProcessing.process_area(table_rows)
    info['government'] = InfoProcessing.process_government(table_rows)
    info['official_name'] = InfoProcessing.process_official_name(table_rows)
    info['density_km2'] = InfoProcessing.process_density(table_rows)
    info['capital_name'] = InfoProcessing.process_capital(table_rows)

    return info


def get_soup_for_link(link):
    url_client = url_req(link)
    page_html = url_client.read()
    url_client.close()
    return soup(page_html, "html.parser")


def get_link_for_every_countries():
    url_all_countries = 'https://en.wikipedia.org/wiki/List_of_sovereign_states'

    page_soup = get_soup_for_link(url_all_countries)
    countries_rows_unfiltered = page_soup.find('table').find('tbody').find_all('tr')[5:]

    url_root_country = 'https://en.wikipedia.org'
    links = list()
    for country in countries_rows_unfiltered:
        tag_text = country.text + ' '
        if 'ZZZ' in tag_text or 'AAA' in tag_text:
            continue
        first_column = country.select('td')[0]
        link = url_root_country + first_column.select('a')[0]['href']
        links.append(link)
    return links


links_all = get_link_for_every_countries()


class WikiCrawler:
    @staticmethod
    def get_link_for_every_countries():
        return links_all

    @staticmethod
    def get_info_all_by_id(country_name):
        print('\n\n\n\n\n IN get_info_all_by_id \n\n\n\n')
        print(f'{WikiCrawler.get_link_by_id(country_name)}')
        print('\n\n\n\n\n IN get_info_all_by_id \n\n\n\n')
        return crawl_info_from_link_country(WikiCrawler.get_link_by_id(country_name))

    @staticmethod
    def get_info_all_by_link(country_link):
        print(country_link)
        return crawl_info_from_link_country(country_link)

    @staticmethod
    def get_link_by_id(country_name):
        country_name = country_name.lower()
        link_list_lower = [each_string.lower() for each_string in links_all]
        for index in range(len(link_list_lower)):
            if country_name in link_list_lower[index]:
                return links_all[index]
        return f'Country {country_name} not found'
