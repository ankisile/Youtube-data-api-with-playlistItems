import imp
import json
import os
import datetime as dt
import re
import sys
import pandas as pd #엑셀 형태로 저장하기 위한 라이브러리
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
from pprint import pprint
import openpyxl as xl
from urllib.request import urlopen
from bs4 import BeautifulSoup
import config
from oauth2client.service_account import ServiceAccountCredentials
import gspread



def get_videos(service, upload_id):
    try:
        response = service.playlistItems().list(
            part="snippet", #응답 받을 내용들
            playlistId = upload_id,
            maxResults=5,
        ).execute()

        # pprint(response)
        return response['items']
        
    except HttpError as e:
        errMsg = json.loads(e.content)
        print('HTTP Error:')
        print(errMsg['error']['message'])




# def video2excel(link, datetime):
def video2excel(datetime):


    DEVELOPER_KEY = config.key
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    service = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY, static_discovery=False)


    print("Start")
    # link_list = get_link(link) 
    link_list = get_link() 

    
    df = pd.DataFrame()

    columns = ['Video Link', 'Video Title', 'Publish Date',  'Channel Name', 'Description', 'Thumbnail' ]

    for i in link_list:

        channel_id = get_channel_id(i)
        upload_id = channel_id[:1] + 'U' + channel_id[1+1:]
        response = get_videos(service, upload_id)

        for res in response:
            row = []

            publishedAt = dt.datetime.strptime(res['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            inputAt = dt.datetime.strptime(datetime, "%Y-%m-%dT%H:%M:%SZ")
            if publishedAt>inputAt:
                rs = res['snippet']
                video_url = "https://www.youtube.com/watch?v={0}".format(rs['resourceId']['videoId'])
                video_title = rs['title']
                video_desc = rs['description']
                thumbnail = rs['thumbnails']['standard']['url'] if 'standard' in rs['thumbnails'] else rs['thumbnails']['high']['url']
                channel_name =rs['channelTitle']
                publish_date = publishedAt

                row.append([video_url, video_title, publish_date, channel_name, video_desc, thumbnail])
                video_df = pd.DataFrame(data=row, columns=columns) 
        
                df = pd.concat([df, video_df], ignore_index=True)
                
    # print(df)
    df.to_excel("video_url.xlsx", index=False)
    return "Success"


def get_channel_id(value):
    
    # print(value)
    query = urlparse(value)

    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path[:9] == '/channel/':
            return query.path.split('/')[2]
        else:
            html = urlopen(value)
            bsObject = BeautifulSoup(html, "html.parser")
            return bsObject.find("meta",{"itemprop":"channelId"}).get('content')
    # fail?
    return None


# def get_link(url):

#     value=url.replace('"','')

#     read_xlsx = xl.load_workbook(value)
#     read_sheet = read_xlsx.active

#     name_col = read_sheet['A']
#     names = []
#     for cell in name_col:
#         names.append(cell.value)

#     return names

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)



def get_link():

    scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
    ]

    credential = ServiceAccountCredentials.from_json_keyfile_name(resource_path("momof_json.json"), scope)
    gc = gspread.authorize(credential)


    spreadsheet_key = "1jt84gI9KLHchUzyMxT1g9CXGNLh4csjb5M77w9-JHvQ"
    doc = gc.open_by_key(spreadsheet_key)


    sheet = doc.worksheet("시트1")

    column_data =  sheet.col_values(1)
    print(column_data)

    return column_data


# if __name__ == "__main__":    
    # url = input("url 입력 = ")
    # get_channel_id(url)
    

    # id = get_link(url)
    # video2excel(url, datetime)