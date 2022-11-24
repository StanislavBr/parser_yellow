import sys
import csv
import requests
from bs4 import BeautifulSoup


def parse(link):
    result=[]
    list_link_company = get_link_company(link)
    for data in list_link_company:
        nun_name=get_data_for_link(data)
        print(f'Получил {nun_name} от {data}')
        if nun_name[0] == 'Добавить номер телефона':
            continue
        else:
            print(f'ДОБАВЛЯЮ {nun_name}')
            result.append(nun_name)
    print('Начинаю запись')
    write_file(result)
    print('Записал')
    return result



def get_link_company(link):
    list_link=[]
    link_glob=get_link_all_page(link)
    for link_num in link_glob:
        print(f'Запрос к {link_num}')
        response = requests.get(link_num)
        soup = BeautifulSoup(response.content, 'html.parser')
        link_company=soup.find_all('a', class_='none')
        for link in link_company:
            link_current="https://yellow.place"+link['href']
            list_link.append(link_current) 
    return list_link


def get_data_for_link(link):
    response = response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    number = soup.find('span',class_='i i-small i-call').find('a').get_text()
    name_company=soup.find('div',class_='h1').find('h1').get_text()
    return number,name_company


def get_link_all_page(link):
    list_act_link=[]
    lenu=0
    link_current=link+'page_list?page='
    for cou in range(1,10000):
        lenu+=1
        link_act=link_current+f'{lenu}'
        result = requests.get(link_act)
        try:
            soup = BeautifulSoup(result.content, 'html.parser')
            link_company=soup.find_all('a', class_='none')
            if len(link_company) != 0:
                list_act_link.append(link_act)
            else:
                break
        except:
            break
    return list_act_link

def write_file(data):
    with open('parse.csv', "w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    return
if __name__ == "__main__":
    link = sys.argv[1]
    parse(link=link)