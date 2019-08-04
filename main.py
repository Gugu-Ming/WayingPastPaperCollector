import requests
from bs4 import BeautifulSoup
import os

USERNAME = 'WTFK'
PASSWORD = 'CHEMISTRY'

LOGIN_DATA = {
    'username': USERNAME,
    'password': PASSWORD,
}

LOGIN_URL = 'http://student.waying.edu.hk/moodle195/login/index.php'
MATHEMATICS_DEPARTMENT_URL = 'http://student.waying.edu.hk/moodle195/course/view.php?id=222'

class MoodleSession(requests.Session):
    def set_moodle_cookies(self, cMoodleSession, cMoodleSessionTest, cMOODLEID_):
        self.cookies.set('MoodleSession', cMoodleSession)
        self.cookies.set('MoodleSessionTest', cMoodleSessionTest)
        self.cookies.set(' MOODLEID_', cMOODLEID_)

def main():

    result_text_file = open("results.txt", mode="w", encoding="UTF-8")

    with MoodleSession() as s:
        s.post(LOGIN_URL, data=LOGIN_DATA)
        mathematics_department_page = s.get(MATHEMATICS_DEPARTMENT_URL)

        soup_mathdep = BeautifulSoup(mathematics_department_page.text, 'html5lib')

        pastpaper_tree = {}

        for i in range(1,5):
            id_name = 'section-' + str(i)
            pastpaper_folder_tr = soup_mathdep.find('tr', attrs={'id': id_name})

            folder_name = find_tr_title(pastpaper_folder_tr)
            print("[***]Fetching URL data in " + folder_name)

            folder_urls = find_folder_urls(pastpaper_folder_tr)

            pastpaper_tree[folder_name] = folder_urls

            for key in pastpaper_tree[folder_name]:
                folder_url = pastpaper_tree[folder_name][key]['url']
                print("[   ]Fetching URL data in " + key)
                pastpaper_page = BeautifulSoup(s.get(folder_url).text, 'html5lib')

                pastpaper_tree[folder_name][key]['pastpapers'] = find_pdf_urls(pastpaper_page)

        result_text_file.write(str(pastpaper_tree))

        md("downloads")
        for term in pastpaper_tree:
            md("/".join(["downloads",term]))
            for level in pastpaper_tree[term]:
                md("/".join(["downloads",term,level]))
                for pastpaper in pastpaper_tree[term][level]['pastpapers']:
                    download_url = pastpaper_tree[term][level]['pastpapers'][pastpaper]  
                    if not os.path.exists("/".join(["downloads",term,level,pastpaper])):
                        result = s.get(download_url)
                        print("[   ]Downloaded " + pastpaper)
                        open("/".join(["downloads",term,level,pastpaper]), 'wb').write(result.content)
                    else:
                        print("/".join(["downloads",term,level,pastpaper]) + " is not downloaded because the file already exists.")

        
        
        

def find_folder_urls(pastpaper_folder_tr):
    pastpaper_folder_ul = list(list(pastpaper_folder_tr.children)[1].children)[1]
    pastpaper_folder_a = pastpaper_folder_ul.find_all('a')
    pastpaper_folder_urls = {}

    for a in pastpaper_folder_a:
        title = a.span.contents[0]
        pastpaper_folder_urls[title] = {'url': a.attrs['href']}
    
    return pastpaper_folder_urls

def find_tr_title(pastpaper_folder_tr):
    title = pastpaper_folder_tr.find('div', attrs={'class':"summary"}).contents[0]
    return title

def find_pdf_urls(pastpaper_folder_page):
    pastpaper_tr = pastpaper_folder_page.find_all('tr', attrs={'class': 'file'})
    pastpaper_url = {}
    for tr in pastpaper_tr:
        a = tr.td.a
        index = a.contents[1].replace('\xa0', '')
        pastpaper_url[index] = (a.attrs['href'])
    return pastpaper_url

def md(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        print("[***]Created folder "+ folder_name)
    else:
        print(folder_name + " is not created because the folder already exists.")
        

if __name__ == "__main__":
    main()
