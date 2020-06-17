import requests
import datetime

class PlaylistDuration:

    def __init__(self, url=None):
        self.API_KEY = 'AIzaSyBganVKyyXVWfFAbM5yJActaGHOcZuI260'
        self.playlist_id = self.get_playlist_id(url)
        self.url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={self.playlist_id}&key={self.API_KEY}'
        self.int_horas = self.int_minutos = self.int_segundos = 0
        self.main(self.url)
        

    def main(self, url):
        data = self.get_requested_playlist(url)

        print('[DATA] Parsing data, this may take a while...\n')

        self.get_video_id(data, url)
        self.result()


    def get_playlist_id(self, url):
        print('[URL] Getting playlist id...')

        user_url = url

        if not url:
            user_url = input("Insert the playlist link: ")

        equalsIndex = user_url.find('=')
        url_id = user_url[equalsIndex+1:len(user_url)]
        return url_id


    def get_requested_playlist(self, url):   
        print('[PLAYLIST] Getting playlist data...')

        rPlaylist = requests.get(url = url) 
        data = rPlaylist.json()
        return data
        

    def get_video_id(self, data, url): 
        for item in data["items"]:
            self.get_time(item["snippet"]["resourceId"]["videoId"])
        
        try:
            if data["nextPageToken"]:
                self.next_page(url, data["nextPageToken"]) 
        except:
            pass
        finally:
            return

    
    def next_page(url, pageToken):
        url += f'&pageToken={pageToken}'
        self.get_requested_playlist(url)


    def get_time(self, video_id):
        video_url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key=AIzaSyBganVKyyXVWfFAbM5yJActaGHOcZuI260&part=contentDetails'
        rVideo = requests.get(url = video_url)
        dataVideo = rVideo.json()
        duration = dataVideo["items"][0]["contentDetails"]["duration"]
        self.parse_data(duration)


    def parse_data(self, duration):
        duration = duration[2:len(duration)]

        if 'H' in duration:
            index = duration.find('H')
            horas = duration[:index]
            self.int_horas += int(horas)
            duration = duration[index+1:len(duration)]
        if 'M' in duration:  
            index = duration.find('M')
            minutos = duration[:index]
            self.int_minutos += int(minutos)
            duration = duration[index+1:len(duration)]
        if 'S' in duration:
            index = duration.find('S')
            segundos = duration[:index]
            self.int_segundos += int(segundos)



    def result(self):
        teste = str(datetime.timedelta(hours=self.int_horas, minutes=self.int_minutos, seconds=self.int_segundos ))
        testeArray = teste.split(sep=':')
        h, m, s = (testeArray[0], testeArray[1], testeArray[2])

        if int(h) > 0:
            print(f"{h} Hours, {m} Minutes and {s} Seconds!")
        else:
            print(f"{m} Minutes and {s} Seconds!")
    
            