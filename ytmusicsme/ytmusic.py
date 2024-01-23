import requests
import json
import pandas as pd
import ytmusicsme.helper as h
import ytmusicsme.contants as c
import re
import html
import http.client
import json
from urllib.parse import urlencode


class YTMusic():
  
    def __init__(self):
        self.name = 'YTMUSIC'
        
    def query_stats(self,artistId):
        
        # json_data = {'context': c.JSON_DATA_CONTEXT_MAINPAGE}
        # json_data['browseId'] = artistId
        # json_data['params'] = 'ggMCCAI%3D'


        # response = requests.post(
        #     'https://music.youtube.com/youtubei/v1/browse',
        #     params=c.PARAMS,
        #     headers=c.HEADERS_MAINPAGE,
        #     json=json_data,
        # )

        # j = json.loads(response.text)
        # response.close()

        json_data = {'context': c.JSON_DATA_CONTEXT_MAINPAGE}
        json_data['browseId'] = artistId
        json_data['params'] = 'ggMCCAI%3D'

        conn = http.client.HTTPSConnection('music.youtube.com')
        conn.request(
            'POST',
            '/youtubei/v1/browse?'+urlencode(c.PARAMS),
            json.dumps(json_data),
            c.HEADERS
        )
        response = conn.getresponse()
        result = response.read().decode('utf-8')
        conn.close()

        j = json.loads(result)

        return j

    def query_stats_next(self,artistId,ctoken):
        
        # params = c.PARAMS
        # params['type'] = 'next'
        # params['ctoken'] = ctoken
        # params['continuation'] = ctoken

        # json_data = {'context': c.JSON_DATA_CONTEXT_MAINPAGE}
        # json_data['browseId'] = artistId
        # json_data['params'] = 'ggMCCAI%3D'

        # response = requests.post(
        #     'https://music.youtube.com/youtubei/v1/browse',
        #     params=c.PARAMS,
        #     headers=c.HEADERS_MAINPAGE,
        #     json=json_data,
        # )

        # j = json.loads(response.text)
        # response.close()

        params = c.PARAMS
        params['type'] = 'next'
        params['ctoken'] = ctoken
        params['continuation'] = ctoken

        json_data = {'context': c.JSON_DATA_CONTEXT_MAINPAGE}
        json_data['browseId'] = artistId
        json_data['params'] = 'ggMCCAI%3D'

        conn = http.client.HTTPSConnection('music.youtube.com')
        conn.request(
            'POST',
            '/youtubei/v1/browse?'+urlencode(params),
            json.dumps(json_data),
            c.HEADERS
        )
        response = conn.getresponse()
        result = response.read().decode('utf-8')
        conn.close()

        j = json.loads(result)

        return j
    
    def json_to_stats(self,songs):
        df = []

        for song in songs:

            plays,title,videoId,artist,artistId,album,albumId = None, None, None, None, None, None, None

            if 'flexColumns' in song:
                for item in song['flexColumns']:


                    o = item['musicResponsiveListItemFlexColumnRenderer']['text']['runs'][0]
                    text = o['text']

                    if 'odtworz' in text and 'navigationEndpoint' not in o:
                        plays = h.convert_string_to_number(re.sub('odtworz.*','',text))

                    if 'navigationEndpoint' in o:
                        if 'watchEndpoint' in o['navigationEndpoint']:
                            title = o['text']
                            videoId = o['navigationEndpoint']['watchEndpoint']['videoId']


                    if 'navigationEndpoint' in o:
                        if 'browseEndpoint' in o['navigationEndpoint']:
                            if 'browseEndpointContextSupportedConfigs' in o['navigationEndpoint']['browseEndpoint']:

                                pageType = o['navigationEndpoint']['browseEndpoint']['browseEndpointContextSupportedConfigs']['browseEndpointContextMusicConfig']['pageType']

                                if pageType == 'MUSIC_PAGE_TYPE_ARTIST':
                                    artistId = o['navigationEndpoint']['browseEndpoint']['browseId']
                                    artist = o['text']


                                if pageType == 'MUSIC_PAGE_TYPE_ALBUM':
                                    albumId = o['navigationEndpoint']['browseEndpoint']['browseId']
                                    album = o['text']


                df.append([plays,title,videoId,artist,artistId,album,albumId])



        df = pd.DataFrame(df,columns=['plays','title','videoId','artist','artistId','album','albumId'])

        return df

    def get_stats_old(self,artistId):

        df_list = []

        j = self.query_stats(artistId)
        #songs = j['contents']['singleColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['musicPlaylistShelfRenderer']['contents']
        songs = h.find_musicPlaylistShelfRenderer(j)


        df = self.json_to_stats(songs['contents'])
        df_list.append(df)


        #loop
        while(True):
            if 'contents' in j:
                if 'continuations' in j['contents']['singleColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['musicPlaylistShelfRenderer']:
                    
                    continuation = j['contents']['singleColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['musicPlaylistShelfRenderer']['continuations'][0]
                    ctoken = continuation['nextContinuationData']['continuation']
                    j = self.query_stats_next(artistId,ctoken)

                    songs = j['continuationContents']['musicPlaylistShelfContinuation']['contents']
                    #songs = h.find_musicPlaylistShelfRenderer(j)
                    
                    df = self.json_to_stats(songs)
                    df_list.append(df)
                    
                else:
                    break
            else:
                break



        return pd.concat(df_list, ignore_index=True)
    
    def query_search(sefl,q):

        json_data = {'context': c.JSON_DATA_CONTEXT}
        json_data['query'] = q
        
        # response = requests.post(
        #     'https://music.youtube.com/youtubei/v1/search',
        #     params=c.PARAMS,
        #     cookies=c.COOKIES,
        #     headers=c.HEADERS,
        #     json=json_data,
        # )

        # j = json.loads(response.text)
        # response.close()

        conn = http.client.HTTPSConnection('music.youtube.com')
        conn.request(
            'POST',
            '/youtubei/v1/search?'+urlencode(c.PARAMS),
            json.dumps(json_data),
            c.HEADERS
        )
        response = conn.getresponse()
        result = response.read().decode('utf-8')
        conn.close()

        return result
    
    def search(self,q):
        j = self.query_search(q)

        df_list = []

        tabbedSearchResultsRenderers = h.find_objects_list(json.loads(j),'tabbedSearchResultsRenderer')

        for tabbedSearchResultsRenderer in tabbedSearchResultsRenderers:
            for tab in tabbedSearchResultsRenderer['tabs']:

                videoId, title, artistId, artist, albumId, album = None,  None,  None,  None,  None,  None, 

                for content in tab['tabRenderer']['content']['sectionListRenderer']['contents']:
                    if 'musicCardShelfRenderer' in content:
                        if 'subtitle' in content['musicCardShelfRenderer']:
                            for run in content['musicCardShelfRenderer']['subtitle']['runs']:
                                if 'navigationEndpoint' in run:
                                    pageType = run['navigationEndpoint']['browseEndpoint']['browseEndpointContextSupportedConfigs']['browseEndpointContextMusicConfig']['pageType']
                                    browseId = run['navigationEndpoint']['browseEndpoint']['browseId']
                                    text = run['text']

                                    if 'MUSIC_PAGE_TYPE_ARTIST' in pageType:
                                        artistId = browseId
                                        artist = text

                                    if 'MUSIC_PAGE_TYPE_ALBUM':
                                        albumId = browseId
                                        album = text

                        if 'title' in content['musicCardShelfRenderer']:
                            title = content['musicCardShelfRenderer']['title']['runs'][0]['text']
                            videoId = content['musicCardShelfRenderer']['title']['runs'][0]['navigationEndpoint']['watchEndpoint']['videoId']

                df_list.append([videoId, title, artistId, artist, albumId, album])

        df = pd.DataFrame(df_list,columns=['videoId', 'title', 'artistId', 'artist', 'albumId', 'album'])

        return df
    
    def get_stats_artistid_old(self,artistId):

        j = self.query_stats(artistId)
        obj_list = h.find_objects_list(j,'browseEndpoint')

        for obj in obj_list:
            if 'browseId' in obj and 'browseEndpointContextSupportedConfigs' in obj:
                if 'MUSIC_PAGE_TYPE_PLAYLIST' in obj['browseEndpointContextSupportedConfigs']['browseEndpointContextMusicConfig']['pageType']:
                    return obj['browseId']
        
    def get_stats(self,artistId):

        df_list = []

        j = self.query_stats(artistId)
        songs = h.find_all_music_renderers(j)

        df = self.json_to_stats(songs)
        df_list.append(df)

        nextContinuationData_list = h.find_objects_list(j,'nextContinuationData')


        for nextContinuationData in nextContinuationData_list:
            if 'continuation' in nextContinuationData:
                ctoken = nextContinuationData['continuation']
                j = self.query_stats_next(artistId,ctoken)

                songs = h.find_objects_list(j,'musicResponsiveListItemRenderer')

                df = self.json_to_stats(songs)
                df_list.append(df)

        return pd.concat(df_list, ignore_index=True)

    def get_stats_artistid(self,artistid):


        # response = requests.get(
        #     'https://music.youtube.com/channel/'+artistid,
        #     cookies=c.COOKIES,
        #     headers=c.HEADERS
        #     )

        # html_txt = response.text
        # response.close()

        conn = http.client.HTTPSConnection('music.youtube.com')
        conn.request('GET', '/channel/UCwKinv11f26aSK5tRu53WzQ', headers=c.HEADERS)
        response = conn.getresponse()
        html_txt = response.read().decode('utf-8')
        conn.close()

        pattern = re.compile(r'initialData\.push\(.*?\);')
        pattern2 = re.compile(r'browseId\":\".*?\"')

        matches = pattern.findall(html_txt)

        # Output the matches
        for match in matches:
            match_clean = html.unescape(match.replace('\/','').encode('utf-8').decode('unicode-escape'))
            match_clean = match_clean.replace('initialData.push(','').replace(');','')

            if 'ggMCCAI%3D' in match_clean:
                index = match_clean.find('ggMCCAI')
                string_lookup = match_clean[max(index-100,0):max(index,1)]
                matches2 = pattern2.findall(string_lookup)

                for match2 in matches2:
                    return (match2.replace('browseId":"','').replace('"',''))
