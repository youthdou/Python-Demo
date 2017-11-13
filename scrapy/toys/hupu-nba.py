import sys
import requests
from bs4 import BeautifulSoup
import html5lib
import time

def getText(bsObj, strSelector):
    strInfo = ''
    infos = bsObj.select(strSelector)
    if len(infos) > 0:
        return infos[0].text
    return strInfo

'''
def parseUrl(strUrl):
    r = requests.get(strUrl)
    bsObj = BeautifulSoup(r.text, 'html5lib')
    #team_a = bsObj.find_all('div', {'class':'team_a'})
    team_a_score = getText(bsObj, 'body > div.gamecenter_livestart > div.gamecenter_content.boxscore_td '
                          '> div.gamecenter_content_l > div.box_a > div.team_vs > div.team_vs_box '
                          '> div.team_a > div.message > h2')

    team_a_name = getText(bsObj, 'body > div.gamecenter_livestart > div.gamecenter_content.boxscore_td '
                          '> div.gamecenter_content_l > div.box_a > div.team_vs > div.team_vs_box '
                          '> div.team_a > div.message > p > a')

    game_info = getText(bsObj, 'body > div.gamecenter_livestart > div.gamecenter_content.boxscore_td '
                        '> div.gamecenter_content_l > div.box_a > div.team_vs > div.team_vs_box '
                        '> div.team_num')

    team_b_score = getText(bsObj, 'body > div.gamecenter_livestart > div.gamecenter_content.boxscore_td '
                                  '> div.gamecenter_content_l > div.box_a > div.team_vs > div.team_vs_box '
                                  '> div.team_b > div.message > h2')

    team_b_name = getText(bsObj, 'body > div.gamecenter_livestart > div.gamecenter_content.boxscore_td > '
                                 'div.gamecenter_content_l > div.box_a > div.team_vs > div.team_vs_box > div.team_b '
                                 '> div.message > p > a')

    return '[%s]%s [%s] [%s]%s' % (team_a_name, team_a_score, game_info, team_b_name, team_b_score)
'''

def getTeamInfo(bsObj, strTeam):
    div = bsObj.find('div', strTeam)
    name = div.img['alt']
    score = div.h2.text 
    return (name, score)

def getGameInfo(bsObj):
    div = bsObj.find('div', {'class':'team_num'})
    if div is None:
        return ''
    return div.text

def parseUrl(strUrl):
    r = requests.get(strUrl)
    bsObj = BeautifulSoup(r.text, 'html5lib')
    #team_a = bsObj.find_all('div', {'class':'team_a'})
    team_a = getTeamInfo(bsObj, 'team_a')
    team_b = getTeamInfo(bsObj, 'team_b')
    game = getGameInfo(bsObj)

    return '[%s]%s [%s] [%s]%s' % (team_a[0], team_a[1], game, team_b[0], team_b[1])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: %s url" % (sys.argv[0]))
        sys.exit(1)
    print('Start to collect: ', sys.argv[1])
    while True:
        time.sleep(5)
        print(parseUrl(sys.argv[1]))


