class all_functions:

    def get_chanel_stats(youtube, channel_ids):

        all_data = []
        request = youtube.channels().list(
            part='snippet, contentDetails,statistics',
            id= ','.join(channel_ids)
        )
        response = request.execute()
        
        for i in range(len(response['items'])):
            data = dict(channel_name = response['items'][i]['snippet']['title'],
                        Geographical_area = response['items'][i]['snippet']['country'],
                        Channel_views = response['items'][i]['statistics']['viewCount'],
                        Channel_subscribers = response['items'][i]['statistics']['subscriberCount'],
                        Channel_videos = response['items'][i]['statistics']['videoCount'],
                        playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads']
                        )
            all_data.append(data)

        return all_data
    
    

    def get_video_ids(youtube, playlist_id):

        request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId = playlist_id,
            maxResults = 50
        )

        response = request.execute()

        return response
    


    def get_video_ids_all(youtube, playlist_id):
        
        request = youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId = playlist_id,
                    maxResults = 50)
        response = request.execute()
        
        video_ids = []
        
        for i in range(len(response['items'])):
            video_ids.append(response['items'][i]['contentDetails']['videoId'])
            
        next_page_token = response.get('nextPageToken')
        more_pages = True
        
        while more_pages:
            if next_page_token is None:
                more_pages = False
            else:
                request = youtube.playlistItems().list(
                            part='contentDetails',
                            playlistId = playlist_id,
                            maxResults = 50,
                            pageToken = next_page_token)
                response = request.execute()
        
                for i in range(len(response['items'])):
                    video_ids.append(response['items'][i]['contentDetails']['videoId'])
                
                next_page_token = response.get('nextPageToken')
            
        return video_ids
    
    def get_video_details(youtube, video_ids):
        
        request = youtube.videos().list(
                    part='snippet,statistics',
                    id=','.join(video_ids[:50]))
        response = request.execute()
            
            
        return response
    
    def get_video_details_all(youtube, video_ids):
        all_video_stats = []
        
        for i in range(0, len(video_ids), 50):
            request = youtube.videos().list(
                        part='snippet,statistics',
                        id=','.join(video_ids[i:i+50]))
            response = request.execute()
            
            for video in response['items']:
                video_stats = dict(Title = video['snippet']['title'],
                                Published_date = video['snippet']['publishedAt'],
                                Views = video['statistics']['viewCount'],
                                Likes = video['statistics']['likeCount'],
                                Comments = video['statistics']['commentCount']
                                )
                all_video_stats.append(video_stats)
        
        return all_video_stats