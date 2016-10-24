from bs4 import BeautifulSoup
import re
import urllib
import requests

numPages = 10
out_file = 'antichess_games.txt'

def main():
    url = 'https://en.lichess.org/games/search'
    params = { 'page': '1', 'perf': '13', 'status': '60', 'sort.field': 'd', 'sort.order': 'desc', '_': '1477283238146' }
    headers = { 'Connection': 'keep-alive', 'Accept': 'text/html, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36', 'Referer': 'https://en.lichess.org/games/search?page=1&perf=13&status=60&sort.field=d&sort.order=desc&_=1477270963263', 'Accept-Encoding': 'gzip, deflate, sdch, br', 'Accept-Language': 'en-US,en;q=0.8' }
    
    f=open(out_file, 'a')

    for pageNum in xrange(1, 1+numPages):
    	params['page'] = str(pageNum)
    	print 'Downloading Page', pageNum, 'out of', numPages
    	response = requests.get(url, params=params, headers=headers)
    	html = response.text
        soup = BeautifulSoup(html, "html5lib")

        games = soup.find_all('div', 'game_row paginated_element')
        for game in games:
            game_url = 'https://en.lichess.org' + game.a.get('href')
            print "    Downloading game from", game_url

            sock = urllib.urlopen(game_url) 
            game_html = sock.read()    
            sock.close()

            game_soup = BeautifulSoup(game_html, "html5lib")
            relevant_div = game_soup.find_all('div', 'pgn')
            if len(relevant_div) == 1:
            	content = re.split("<.*?>", str(relevant_div[0]))
            	if content[len(content) - 2].startswith('1. '):
            		f.write(game_url + '\n')
            		f.write(content[len(content) - 2] + '\n')

    f.close()

if __name__=="__main__":
    main()