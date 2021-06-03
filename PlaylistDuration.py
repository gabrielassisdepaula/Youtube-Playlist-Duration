import requests
import datetime
from decouple import config
from requests.structures import CaseInsensitiveDict

from OAuthAuthentication import OAuthAuthentication

class PlaylistDuration:

    def __init__(self, url=None):
        self.API_KEY = config('API_KEY')
        self.playlist_id = self.get_playlist_id(url)
        self.request_url = f"{config('BASE_PLAYLIST_REQUEST_URL')}{self.playlist_id}"
        self.int_hours = self.int_minutes = self.int_seconds = 0
        self.get_playlist_duration()

    def get_playlist_id(self, url):
        print('Getting playlist id...')

        playlist_url = self.get_playlist_url(url)

        equals_index = playlist_url.find('=')
        url_id = playlist_url[equals_index+1 : len(playlist_url)]
        return url_id
    
    def get_playlist_url(self, playlist_url):
        if not playlist_url:
            playlist_url = input("Insert the playlist link: ")
        return playlist_url

    def get_playlist_duration(self):
        print('Getting playlist data...')
        data = self.get_playlist(self.request_url)

        print('Parsing data, this may take a while...\n')
        self.parse_playlist_videos(data)
        self.print_result()

    def get_playlist(self, url):           
        playlist_request = requests.get(url = url)

        if playlist_request.status_code == 200:
            return playlist_request.json()
        elif playlist_request.status_code == 404:
            print("This is a private playlist and you need to give access to get the playlist duration.")
            access_token = OAuthAuthentication().get_access_token()
            return self.get_playlist_with_oauth(url, access_token).json()
        
        return playlist_request.json()
    
    def get_playlist_with_oauth(self, url, access_token):
        headers = CaseInsensitiveDict()
        headers["Authorization"] = f"Bearer {access_token}"
        headers["Accept"] = "application/json"

        return requests.get(url, headers=headers)
    
    def parse_playlist_videos(self, data):
        for video in data["items"]:
            video_id = self.get_video_id(video)
            video_duration = self.get_video_duration(video_id)
            self.parse_video_duration(video_duration)
        
        try:
            if data["nextPageToken"]:
                next_page_data = self.get_next_page_data(data["nextPageToken"]) 
                self.parse_playlist_videos(self, next_page_data)
        except:
            return

    def get_video_id(self, video): 
        return video["snippet"]["resourceId"]["videoId"]

    def get_video_duration(self, video_id):
        video_url = f"{config('VIDEO_REQUEST_BASE_URL')}{video_id}"

        video_request = requests.get(url = video_url)
        video_data = video_request.json()
        try:
            video_duration = video_data["items"][0]["contentDetails"]["duration"]
        except IndexError:
            return None
        
        return video_duration
        
    def parse_video_duration(self, duration):
        if not duration:
            return

        duration = duration[2:len(duration)]

        if 'H' in duration:
            index = duration.find('H')
            hours = duration[:index]
            self.int_hours += int(hours)
            duration = duration[index+1:len(duration)]
        if 'M' in duration:  
            index = duration.find('M')
            minutes = duration[:index]
            self.int_minutes += int(minutes)
            duration = duration[index+1:len(duration)]
        if 'S' in duration:
            index = duration.find('S')
            seconds = duration[:index]
            self.int_seconds += int(seconds)

    def get_next_page_data(self, pageToken):
        next_page_url = f'{self.request_url}&pageToken={pageToken}'
        return self.get_playlist(next_page_url)

    def print_result(self):
        total_duration = str(datetime.timedelta(hours=self.int_hours, minutes=self.int_minutes, seconds=self.int_seconds))
        total_duration_array = total_duration.split()
        final_result = ''
        time = None

        if 'day' in total_duration:
            days = total_duration_array[0]
            time = total_duration_array[2].split(sep=':')

            if int(days) > 1:
                final_result += f'{days} days, '
            else:
                final_result += f'{days} day, '
        else:
            time = total_duration_array.split(sep=':')

        h, m, s = (time[0], time[1], time[2])
        if int(h) > 0:
            final_result += f'{h} Hours, {m} Minutes and {s} Seconds!'
        else:
            final_result += f'{m} Minutes and {s} Seconds!'
        
        print(final_result)
