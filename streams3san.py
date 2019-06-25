#!/usr/bin/env python
# encoding: utf-8

import datetime
import tweepy
import json
import sys
import time
import boto3

s3 = boto3.resource("s3")
bucket_name = "malaysian-tweets"

# Authentication details. To  obtain these visit dev.twitter.com
consumer_key=''
consumer_secret=''
access_token=''
access_token_secret=''

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    # def __init__(self):
    #     self.start_time = time.time()
    #     self.file_name = datetime.datetime.now().strftime("%m-%d.json")

    def on_data(self, data):
        # Parsing
        decoded = json.loads(data)
        # if "country_code" in decoded["place"]:
        #     if not decoded["place"]["country_code"] == "MY":
        #         return True
        file_name = datetime.datetime.now().strftime("s-%Y-%m-%d.json")
        #open a file to store the status objects
        file = open(file_name, 'a')
        #write json to file
        json.dump(decoded,file,sort_keys = True,indent = 4)
        file.write(',\n')
        file.close()
        # object_name = sys.argv[2]
        try:
            response = s3.Object(bucket_name, file_name).put(Body=open(file_name, 'rb'))
            # print (response)
        except Exception as error:
            print (error)
        #show progress
        # print ("Writing tweets to file,CTRL+C to terminate the program")
        # if time.time() - self.start_time > 1 * 60:
        #     self.start_time = time.time()



        return True

    def on_error(self, status):
        print (status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    #Hashtag to stream
    stream.filter(locations=[98.933, 0, 124.125, 15])
    # stream.filter(track = "M")
