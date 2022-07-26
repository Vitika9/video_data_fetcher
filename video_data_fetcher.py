from googleapiclient.discovery import build

DEVELOPER_KEY = 'REPLACE_THIS'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
SAMPLE_VIDEO_ID = '96vCSyjxdSg'

def get_video_data(youtube, video_id):
    results = youtube.videos().list(
            # snippet: title, description, publishedAt, channelId
            # contentDetails: duration
            # statistics: viewCount, likeCount, dislikeCount, favoriteCount, commentCount
            part="snippet,contentDetails,statistics",
            id=video_id,
        ).execute()
    return results

def get_comment_threads(youtube, video_id):
    results = youtube.commentThreads().list(
            # passing "snippet" as argument for part parameter for retrieving only top-level comments
            part="snippet",
            videoId=video_id,
        ).execute()
    return results

def my_print(string):
    print(string + "\n____________________________________________\n")

video_id = input("Enter video id (or use " + SAMPLE_VIDEO_ID + " as sample): ")

try:
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY, static_discovery = False)

    # if video_id is invalid then video_data will be empty, so no need for exception handling
    video_data = get_video_data(youtube, video_id)

    my_print("")
    for item in video_data["items"]:
            my_print("TITLE: " + item["snippet"]["title"])
            my_print("DESCRIPTION: " + item["snippet"]["description"])
            my_print("DURATION: " + item["contentDetails"]["duration"])
            my_print("VIEW COUNT: " + item["statistics"]["viewCount"])
            my_print("LIKE COUNT: " + item["statistics"]["likeCount"])
            my_print("COMMENT COUNT: " + item["statistics"]["commentCount"])
            my_print("FAVORITE COUNT: " + item["statistics"]["favoriteCount"])
            my_print("PUBLISHED AT: " + item["snippet"]["publishedAt"])
            my_print("CHANNEL ID: " + item["snippet"]["channelId"])

    # if video_id is invalid then get_comment_threads will throw an exception
    try:
        comment_threads = get_comment_threads(youtube, video_id)

        print("COMMENTS: ")
        for comment_thread in comment_threads["items"]:
                comment = comment_thread["snippet"]["topLevelComment"]
                author = comment["snippet"]["authorDisplayName"]
                text = comment["snippet"]["textDisplay"]
                print("Comment by " + author + ": " + text)
    except:
        print("Invalid video ID")
        
    my_print("")
except:
    print("Check your internet connection")

input("Press enter to exit")
