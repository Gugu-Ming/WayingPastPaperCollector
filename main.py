import requests
from bs4 import BeautifulSoup

USERNAME = '>a<'
PASSWORD = 'I love you'

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
    with MoodleSession() as s:
        s.post(LOGIN_URL, data=LOGIN_DATA)
        # s.set_moodle_cookies('mm73omrv0jvhopvpvck1sbcth2', 'h81w2f3Evt', '%25B6%25CDO%251B')
        mathematics_department_page = s.get(MATHEMATICS_DEPARTMENT_URL)

        soup_mathdep = BeautifulSoup(mathematics_department_page.text, 'html5lib')

        pastpaper_tree = {}

        for i in range(1,5):
            id_name = 'section-' + str(i)
            pastpaper_folder_tr = soup_mathdep.find('tr', attrs={'id': id_name})
            folder_urls = find_folder_urls(pastpaper_folder_tr)
            folder_name = find_tr_title(pastpaper_folder_tr)
            pastpaper_tree[folder_name] = folder_urls

            for key in pastpaper_tree[folder_name]:
                folder_url = pastpaper_tree[folder_name][key]['url']
                pastpaper_page = BeautifulSoup(s.get(folder_url).text, 'html5lib')

                pastpaper_tree[folder_name][key]['pastpapers'] = find_pdf_urls(pastpaper_page)

        
        print(pastpaper_tree)
        

def find_folder_urls(pastpaper_folder_tr):
    pastpaper_folder_ul = list(list(pastpaper_folder_tr.children)[1].children)[1]
    pastpaper_folder_a = pastpaper_folder_ul.find_all('a')
    pastpaper_folder_urls = {}

    for a in pastpaper_folder_a:
        title = a.span.contents[0]
        print({'url': a.attrs['href']})
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
        print({index: a.attrs['href']})
    return pastpaper_url

if __name__ == "__main__":
    main()
