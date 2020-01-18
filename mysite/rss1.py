'''
Парсим RSS-ленту Kodges.ru
лента на сайте обновляется неизвестно-сколько-раз-в-сутки путем добавления записей сверху
Чтобы не добавлять лишние записи, мы считаем контрольную сумму crc32 от автор+название,
затем для каждой записи проверяем, нет ли совпадения с БД, если нет - добавляем запись
Эту радость надо собрать на Джанго, добавить веб-морду для таблицы с вьюхой книг по теме,
книг за день, за неделю
Обрабатывать тематику. на веб-морде сделать облако тегов тем
Хостить будем на Pythonanywhere
http://arkadiy39.pythonanywhere.com/
'''
from bs4 import BeautifulSoup as BS
from bs4 import CData
from datetime import date,datetime
from urllib.request import urlopen
import binascii
import urllib.parse
import sqlite3


def get_rss(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    values = {'name': 'Michael Foord',
              'location': 'Northampton',
              'language': 'Python' }
    headers = {'User-Agent': user_agent}
    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data, headers)

    with urllib.request.urlopen(req) as response:
       html = response.read().decode('windows-1251')#Кодировка указана в самом RSS
    return html

def convert_date(s):
    right_datetime_string=datetime.strptime(s.split(',')[1].strip(),"%d %b %Y %H:%M:%S %z")
    s1=right_datetime_string.strftime('%Y-%m-%d %H:%M:%S%z')
    return s1

def get_dicts(rubric_id,url,file):
    arr_dicts=[]
    html=get_rss(url)
    #soup=BS(html,'lxml')
    '''
    lxml не работает с CData 
    '''
    soup=BS(html,'html.parser')
    today=str(date.today())
    for s in soup.findAll('item'):

        #print(s)
        dic = {}
        dic["RUBRIC_ID"]=rubric_id
        dic["FILE"]=file
        dic["TITLE"] = s.find('title',).text
        dic["LINK"] = s.find('guid',).text
        dic["DATE"] = today
        #По дате pubdate
        #Надо YYYY-MM-DD HH:MM:SS
        #А нам приходит Tue, 07 Jan 2020 19:34:19 +0300
        dic["PUBDATE"] = convert_date(s.find('pubdate',).text)
        '''if isinstance(s.find('category',), CData):
            print
            'CData contents: %r' % cd'''
        dic["CATEGORY"] = s.find('category',).text
        dic["DOWNLOADED"] = 0
        dic["AUTHOR"]='NA'#на всяк случай, бывает, что строка с Автор: не находится
        arr=s.find('description',).text.split("\n")

        #Это работало бы с lxml
        '''if arr[len(arr)-1].strip().endswith(']]>'):
            dic["DESCRIPTION"]=arr[len(arr)-1].strip()[:-3:]
        for line in arr:
            line.strip()
            if line.startswith('Автор:'):
                dic["AUTHOR"] = line[7::].strip()
            if line.startswith('Страниц:'):
                dic["PAGES"] = line[8::].strip()
            if line.startswith('Формат:'):
                dic["FORMAT"] = line[7::].strip()
            if line.startswith('Размер:'):
                dic["SIZE"] = line[7::].strip()
            if line.startswith('Качество:'):
                dic["QUALITY"] = line[9::].strip()
            if line.startswith('Язык:'):
                dic["LANGUAGE"] = line[5::].strip()
            if line.startswith('Год издания:'):
                dic["YEAR"] = line[12::].strip()'''
        #конец Это работало бы с lxml
        # Немного индусского кода, т.к. Html.parser потупее
        for line in arr:
            if not line.strip()=='':
                if 'Автор:' in line:
                    dic["AUTHOR"]=line[line.find("/span>")+6:line.find("<br"):].strip()
                if 'Страниц' in line:
                    dic["PAGES"]=line[line.find("/span>")+6:line.find("<br"):].strip()
                if 'Формат' in line:
                    dic["FORMAT"]=line[line.find("/span>")+6:line.find("<br"):].strip()
                if 'Размер' in line:
                    dic["SIZE"]=line[line.find("/span>")+6:line.find("<br"):].strip()
                if 'Качество' in line:
                    dic["QUALITY"]=line[line.find("/span>")+6:line.find("<br"):].strip()
                if 'Язык' in line:
                    dic["LANGUAGE"]=line[line.find("/span>")+6:line.find("<br"):].strip()
                if 'Год издания' in line:
                    dic["YEAR"]=line[line.find("/span>")+6:line.find("<br"):].strip()
                #Сейчас вообще жесть
                if not line.strip().startswith('<'):
                    if line.strip().startswith('&nbsp;') and line.strip().endswith('<br /><br />'):
                        dic["DESCRIPTION"] = line.strip()[len('&nbsp;'):len(line.strip())-len('<br /><br />'):]
                    elif line.strip().startswith('&nbsp;') and line.strip().endswith('<br />'):
                        dic["DESCRIPTION"] = line.strip()[len('&nbsp;'):len(line.strip()) - len('<br />'):]
                    elif line.strip().startswith('&nbsp;'):
                        dic["DESCRIPTION"] = line.strip()[len('&nbsp;')::]
                    elif line.strip().endswith('<br /><br />'):
                        dic["DESCRIPTION"] = line.strip()[:len(line.strip()) - len('<br /><br />'):]
                    else:
                        dic["DESCRIPTION"]=line.strip()
        data=dic["AUTHOR"]+dic["TITLE"]
        hexdata=data.encode('utf-8')
        dic["CRC32"]=hex(binascii.crc32(hexdata)& 0xffffffff)
        '''for k,v in dic.items():
            print(k,v)'''
        arr_dicts.append(dic)
    return arr_dicts



def post_row(conn, tablename, rec):
    keys = ','.join(rec.keys())
    question_marks = ','.join(list('?'*len(rec)))
    values = tuple(rec.values())
    try:
        conn.execute('INSERT INTO '+tablename+' ('+keys+') VALUES ('+question_marks+')', values)
        conn.commit()
    except sqlite3.Error as e:
        print(type(e).__name__)


def main():
    #TODO:переписать работу с базой на ORM-подход!
    #Мегасловарь рубрик с сайта кодгес
    rubrics={1:('komp','Компьютерная литература'),2:('nauka','Наука и образование'),3:('tehnika','Технические издания'),
    4:('policy','Политика'),5:('dosug','Дом и семейный очаг'),6:('hudlit','Художественная литература'),
    7:('hobbi','Досуг и хобби'),8:('fizra','Физкультура и спорт'),9:('medik','Медицина и здравоохранение'),
    10:('army','Военная тематика'),11:('econom','Экономика и финансы'),12:('kultura','Искусство и культура'),
    13:('yurist','Юриспруденция'),14:('pereodika','Газеты и журналы'),15:('audio','Аудиокниги'),
    16:('epub','Книги для мобильных устройств'),17:('other','Разное')}
    for k,v in rubrics.items():
        url='https://www.kodges.ru/'+v[0]+'/rss.xml'
        #url='https://www.kodges.ru/komp/program/rss.xml'
        conn = sqlite3.connect("db.sqlite3")
        sql_check_crc32 = "SELECT CRC32 FROM arkadiy39_books WHERE CRC32=?"
        counter=0
        print(f'{url} == {v[1]}')
        for f in get_dicts(k,url,'-'):
            #print(f"{f['CRC32']}")
            #print(f)
            cursor = conn.cursor()
            cursor.execute(sql_check_crc32, [(f['CRC32'])])
            if cursor.fetchone() is None:
                post_row(conn,'arkadiy39_books',f)
                print(f"Новая книга: {f['TITLE']}")
                counter+=1
            '''for k, v in f.items():
                print(f"{f['CRC32']}")'''
        print(f'Добавлено {counter} записей')

if __name__ == "__main__":
    main()