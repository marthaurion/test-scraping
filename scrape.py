import requests
from bs4 import BeautifulSoup

def main():
    url_dict = {}
    with open('datafile.txt', 'r') as f:
        while True:
            line1 = f.readline().rstrip('\r\n')
            line2 = f.readline().rstrip('\r\n')
            line3 = f.readline().rstrip('\r\n')
            if not line2 or not line3:
                break  # EOF
            url_dict[line2] = line1 # index by url
    base_url = 'http://www.animenano.com/blogs/'
    page_response = requests.get(base_url, timeout=10)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    main_content = page_content.findAll('div',attrs={"class":"maincontent"})[0]
    link_library = main_content.findAll('a')
    with open('datafile.txt', 'a') as f:
        for link in link_library:
            blog_name = link.get_text()
            info_url = link.get('href')
            if not info_url in url_dict:
                print('new')
                blog_url = write_blog_url(info_url, f)
                if blog_url is not None:
                    f.write(blog_name+'\n')
                    f.write(info_url+'\n')
                    f.write(blog_url+'\n')
                

def write_blog_url(url, file):
    base_url = 'http://www.animenano.com'+url
    page_response = requests.get(base_url, timeout=10)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    main_content = page_content.findAll('div',attrs={"class":"entryinfo"})
    if not main_content:
        return None
    for link in main_content[0].findAll('a'):
        if link.previous_sibling.strip() == 'URL:':
            temp_url = link.get('href')
            try:
                ping_response = requests.get(temp_url, timeout=10)
            except:
                return temp_url
            if (ping_response.status_code == requests.codes.ok) and (ping_response.url):
                return ping_response.url
            else:
                return temp_url
    return None

main()