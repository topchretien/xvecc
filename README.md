Yelo 2015
=========

This project is a part of [Yielo](http://www.yielo.net/) [Coding Party](http://www.yielo.net/codingparty/).

It comes from a provided list, and we choose ...

eXtended Video Embeded Code Checker !

The project consist in updating base [vecc](https://github.com/magopian/vecc) by using sites API to get
title, description, image, duration and status (aka availability) of the video.

We choose to add an 'apis' dir with a pythonic implementation of each provider api.

A base "WebAPI" class is used to be inherited by each provider api to ensure the use of mandatories methods:
* check(video\_id) which ensure the video is available from provider API
* video\_data which has to be used as an attribut to get the result.

__Usage example:__

    from vecc.core import match
    from apis.youtube import YoutubeAPI
    
    apis = {'youtube': YoutubeAPI, }
    
    video_id, provider = match(embeded_video)
    Api = apis[provider]
    api = Api()
    
    if api.check(video_id):
        video_informations = api.video_data

__CLI usage:__

xvecc manage all options from the original [vecc's Usage description](https://github.com/magopian/vecc#usage)
plus an extra option called 'extract' which provide more informations than 'clean':
* title: Video title,
* description: Video description,
* image: Image associated with the video,
* duration: Video duration as %H:%M:%S,
* status: True if the video is public and operational, else False

'extract' takes a video embed code. This option can be seen as an extended version of "validate".

If the provided code does not match any existent video, only status will be returned as 'False'

Exit codes:
* 1: Provider not found
* 2: Video ID doesn't correspond to an existing video
* 3: Correspond to HTTP 3xx codes
* 4: Correspond to HTTP 4xx codes or timeout when validating the video (HEAD Request time out)
* 5: Correspond to HTTP 5xx codes 
