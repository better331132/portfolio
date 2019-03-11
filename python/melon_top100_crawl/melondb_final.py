from bs4 import BeautifulSoup
import requests
import re
import time
import pymysql
import json
import melondbft as bft
from datetime import date

conn = bft.get_conn('melondb')
with conn:
    cur = conn.cursor()
    sqlsongNo = "select songNo from Song"
    cur.execute(sqlsongNo)
    songNos = cur.fetchall()
    
    sqlalbumNo = "select albumNo from Album"
    cur.execute(sqlalbumNo)
    albumNos = cur.fetchall()
    
    sqlartistNo = "select artistNo from Artist"
    cur.execute(sqlartistNo)
    artistNos = cur.fetchall()

    sqlrankDate = "select rankDate from SongRank"
    cur.execute(sqlrankDate)
    rankDates = cur.fetchall()
url = "http://vlg.berryservice.net:8099/melon/list"
# url = "https://www.melon.com/chart/day/index.htm"

heads = {
    "Referer": "https: // www.melon.com/chart/index.htm",
    "User-Agent": "Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

res = requests.get(url, headers=heads)
html = res.text
soup = BeautifulSoup(html, 'html.parser')
trs = soup.select("form#frm table tr")
trs.pop(0)
pattern_no = re.compile('\(\'(.*)\'\)')
pattern_artist = re.compile('\((.*)\)')

songInfo_dic = {}

for i, tr in enumerate(trs):
    songNo = tr.attrs['data-song-no']
    t_albumNo = tr.select_one('.wrap a').attrs['href']
    albumNo = re.findall(pattern_no, t_albumNo)[0]
    artists = tr.select('.ellipsis.rank02 a')
    for artist in artists:
        t_artistNo = artist.attrs['href']
        artistNo = re.findall(pattern_no, t_artistNo)[0]
        songInfo_dic[songNo] = {'songNo': songNo, 'albumNo': albumNo, 'artistNo': artistNo}
#=============================================================db와 비교하기 위해 songNo, albumNo, artistNo 추출

rankDate = bft.crawl_rankDate(soup)
conn_melondb = bft.get_conn('melondb')
with conn_melondb:
    cur_A = conn_melondb.cursor()
    cur_B = conn_melondb.cursor()
    cur_C = conn_melondb.cursor()
    cur_D = conn_melondb.cursor()
    cur_U = conn_melondb.cursor()
    cur_L = conn_melondb.cursor()
    cur_M = conn_melondb.cursor()
    oldSong_oldAlbum_oldArtist = []
    newSong_oldAlbum_oldArtist = []
    newSong_oldAlbum_newArtist = []
    newSong_newAlbum_oldArtist = []
    newSong_newAlbum_newArtist = []
    crawlDate = str(date.today())
    for tr in trs:
        songNo = int(tr.attrs['data-song-no'])
        t_albumNo = tr.select_one('.wrap a').attrs['href']
        albumNo = int(re.findall(pattern_no, t_albumNo)[0])
        artists = tr.select('.ellipsis.rank02 span.checkEllipsis a')
        if (songNo,) in songNos:
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            rating = bft.crawl_rating(albumNo)
            likecnt_json = bft.crawl_likeCnt(songNo, songInfo_dic)
            for i in likecnt_json['contsLike']:
                if songNo == i['CONTSID']:
                    likeCnt = i['SUMMCNT']
            rank = bft.crawl_rank(tr)
            sql_U = "update Album set rating = %s where albumNo = %s"
            cur_U.execute(sql_U, [rating, songNo])
            if (rankDate,) in rankDates:
                sql_L = "update SongRank set likeCnt = %s where songNo = %s and rankDate = %s"
                cur_L.execute(sql_L, [likeCnt, songNo, rankDate])
            else:
                lst_A = [songNo, rankDate, rank, likeCnt, crawlDate]
                sql_A = "insert ignore into SongRank(songNo, rankDate, rank, likeCnt, crawlDate) values(%s, %s, %s, %s, %s)"
                cur_A.execute(sql_A, lst_A)
            oldSong_oldAlbum_oldArtist.append(songNo)
        #=========================================================================================================A타입
        elif (albumNo,) in albumNos:
            print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
            rating = bft.crawl_rating(albumNo)
            likecnt_json = bft.crawl_likeCnt(songNo, songInfo_dic)
            for i in likecnt_json['contsLike']:
                if songNo == i['CONTSID']:
                    likeCnt = i['SUMMCNT']
            rank = bft.crawl_rank(tr)
            songTitle = bft.crawl_songTitle(tr)
            genre = bft.crawl_genre(songNo)
            lst_B = [songNo, songTitle, genre, albumNo]
            sql_B = """insert ignore into Song(songNo, songTitle, genre, albumNo) 
                                    values (%s, %s, %s, %s)"""
            cur_B.execute(sql_B, lst_B)
            newSong_oldAlbum_oldArtist.append(songNo)
            for artist in artists:
                t_artistNo = artist.attrs['href']
                artistNo = re.findall(pattern_no, t_artistNo)[0]
                artistName = bft.crawl_artistName(tr)
                lst_M = [songNo, artistNo]
                sql_M = """insert ignore into SongArtist(songNo, artistNo)
                                        values(%s, %s)"""
                cur_M.execute(sql_M, lst_M)
            lst_A = [songNo, rankDate, rank, likeCnt, crawlDate]
            sql_A = "insert ignore into SongRank(songNo, rankDate, rank, likeCnt, crawlDate) values(%s, %s, %s, %s, %s)"
            cur_A.execute(sql_A, lst_A)
        #=========================================================================================================B타입
        else:
            for artist in artists:
                t_artistNo = artist.attrs['href']
                artistNo = int(re.findall(pattern_no, t_artistNo)[0])
                artistName = bft.crawl_artistName(tr)
                if (artistNo,) in artistNos:
                    print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
                    rating = bft.crawl_rating(albumNo)
                    likecnt_json = bft.crawl_likeCnt(songNo, songInfo_dic)
                    for i in likecnt_json['contsLike']:
                        if songNo == i['CONTSID']:
                            likeCnt = i['SUMMCNT']
                    rank = bft.crawl_rank(tr)
                    songTitle = bft.crawl_songTitle(tr)
                    genre = bft.crawl_genre(songNo)
                    newSong_newAlbum_oldArtist.append(songNo)
                    albumTitle = bft.crawl_albumTitle(tr)
                    rating = bft.crawl_rating(albumNo)
                    dds = bft.crawl_rara(albumNo)
                    lst_D = [albumNo, albumTitle, rating, artistNo]
                    sql_D = "insert ignore into Album(albumNo, albumTitle, rating, artistNo) values(%s, %s, %s, %s)"
                    cur_D.execute(sql_D, lst_D)
                    for i, dd in enumerate(dds):
                        if i == 0:
                            releaseDate = dd.text.replace('.','')
                            sql_U = "update Album set releaseDate = %s where albumNo = %s"
                            cur_D.execute(sql_U, [releaseDate, albumNo])
                        elif i == 1:
                            albumGenre = dd.text
                            sql_U = "update Album set albumGenre = %s where albumNo = %s"
                            cur_D.execute(sql_U, [albumGenre, albumNo])
                        elif i == 2:
                            releaser = dd.text
                            sql_U = "update Album set releaser = %s where albumNo = %s"
                            cur_D.execute(sql_U, [releaser, albumNo])
                        else:
                            agency = dd.text
                            sql_U = "update Album set agency = %s where albumNo = %s"
                            cur_D.execute(sql_U, [agency, albumNo])
                    lst_B = [songNo, songTitle, genre, albumNo]
                    sql_B = """insert ignore into Song(songNo, songTitle, genre, albumNo) 
                                            values (%s, %s, %s, %s)"""
                    cur_B.execute(sql_B, lst_B)
                    lst_A = [songNo, rankDate, rank, likeCnt, crawlDate]
                    sql_A = "insert ignore into SongRank(songNo, rankDate, rank, likeCnt, crawlDate) values(%s, %s, %s, %s, %s)"
                    cur_A.execute(sql_A, lst_A)
                    for artist in artists:
                        t_artistNo = artist.attrs['href']
                        artistNo = re.findall(pattern_no, t_artistNo)[0]
                        artistName = bft.crawl_artistName(tr)
                        lst_M = [songNo, artistNo]
                        sql_M = """insert ignore into SongArtist(songNo, artistNo)
                                                values(%s, %s)"""
                        cur_M.execute(sql_M, lst_M)
                #=========================================================================================================C타입
                else:
                    print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
                    rating = bft.crawl_rating(albumNo)
                    likecnt_json = bft.crawl_likeCnt(songNo, songInfo_dic)
                    for i in likecnt_json['contsLike']:
                        if songNo == i['CONTSID']:
                            likeCnt = i['SUMMCNT']
                    rank = bft.crawl_rank(tr)
                    newSong_newAlbum_newArtist.append(songNo)
                    songTitle = bft.crawl_songTitle(tr)
                    genre = bft.crawl_genre(songNo)
                    for artist in artists:
                        t_artistNo = artist.attrs['href']
                        artistNo = re.findall(pattern_no, t_artistNo)[0]
                        artistName = bft.crawl_artistName(tr)
                        dl = bft.crawl_dae(artistNo)
                        dts = bft.get_dts(artistNo)
                        rng = len(dts) + 1
                        lst_C = [artistNo, artistName]
                        sql_C = "insert ignore into Artist(artistNo, artistName) values(%s, %s)"
                        cur_C.execute(sql_C, lst_C)
                        for i in range(1, rng):
                            categ = dl.select_one("dt:nth-of-type({})".format(i)).text
                            if categ == '데뷔':
                                debutDate = dl.select_one("dd:nth-of-type({}) span".format(i)).text.replace('.','')
                                sql_U = "update Artist set debutDate = %s where artistNo = %s"
                                cur_C.execute(sql_U, [debutDate, artistNo])
                            elif categ == '활동유형':
                                artistType = dl.select_one("dd:nth-of-type({})".format(i)).text
                                sql_U = "update Artist set artistType = %s where artistNo = %s"
                                cur_C.execute(sql_U, [artistType, artistNo])
                            elif categ == '소속사':
                                emc = dl.select_one("dd:nth-of-type({})".format(i)).text
                                sql_U = "update Artist set emc = %s where artistNo = %s"
                                cur_C.execute(sql_U, [emc, artistNo])
                            else:
                                continue
                        albumTitle = bft.crawl_albumTitle(tr)
                        rating = bft.crawl_rating(albumNo)
                        dds = bft.crawl_rara(albumNo)
                        lst_D = [albumNo, albumTitle, rating, artistNo]
                        sql_D = "insert ignore into Album(albumNo, albumTitle, rating, artistNo) values(%s, %s, %s, %s)"
                        cur_D.execute(sql_D, lst_D)
                        for i, dd in enumerate(dds):
                            if i == 0:
                                releaseDate = dd.text.replace('.','')
                                sql_U = "update Album set releaseDate = %s where albumNo = %s"
                                cur_D.execute(sql_U, [releaseDate, albumNo])
                            elif i == 1:
                                albumGenre = dd.text
                                sql_U = "update Album set albumGenre = %s where albumNo = %s"
                                cur_D.execute(sql_U, [albumGenre, albumNo])
                            elif i == 2:
                                releaser = dd.text
                                sql_U = "update Album set releaser = %s where albumNo = %s"
                                cur_D.execute(sql_U, [releaser, albumNo])
                            else:
                                agency = dd.text
                                sql_U = "update Album set agency = %s where albumNo = %s"
                                cur_D.execute(sql_U, [agency, albumNo])
                        lst_B = [songNo, songTitle, genre, albumNo]
                        sql_B = """insert ignore into Song(songNo, songTitle, genre, albumNo) 
                                                values (%s, %s, %s, %s)"""
                        cur_B.execute(sql_B, lst_B)
                        lst_A = [songNo, rankDate, rank, likeCnt, crawlDate]
                        sql_A = "insert ignore into SongRank(songNo, rankDate, rank, likeCnt, crawlDate) values(%s, %s, %s, %s, %s)"
                        cur_A.execute(sql_A, lst_A)
                        t_artistNo = artist.attrs['href']
                        artistNo = re.findall(pattern_no, t_artistNo)[0]
                        lst_M = [songNo, artistNo]
                        sql_M = """insert ignore into SongArtist(songNo, artistNo)
                                                values(%s, %s)"""
                        cur_M.execute(sql_M, lst_M)
                #=========================================================================================================D타입
    conn_melondb.commit()

noo = set(newSong_oldAlbum_oldArtist)
non = set(newSong_oldAlbum_newArtist)
nno = set(newSong_newAlbum_oldArtist)
nnn = set(newSong_newAlbum_newArtist)
print("기존 곡 수 >>>>>>>>>>>>>>>>", len(set(oldSong_oldAlbum_oldArtist)))
print("챠트에 새로진입한 곡 수 >>>>", len(noo)+len(non)+len(nno)+len(nnn))