#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import sys
import urllib

from vecc.core import get_clean_code, match, get_link
from vecc.vecc import clean, valid

from apis.webapi import APIError
from apis.youtube import YoutubeAPI
from apis.dailymotion import DailymotionAPI
from apis.vimeo import VimeoAPI
from apis.facebook import FacebookAPI


PROVIDERS_API = {
    'youtube': YoutubeAPI,
    'dailymotion': DailymotionAPI,
    'vimeo': VimeoAPI,
    'facebook': FacebookAPI,
}


def extract(code):
    video_id, provider = match(code)
    clean_code = get_clean_code(video_id, provider)
    real_link = get_link(video_id, provider)
    if not clean_code:
        if code[-4:].lower() == '.mp4':
            #test if url exists
            if urllib.urlopen(code).getcode() == 200:
                return {
                    'provider': 'mp4',
                    'real_link': code,
                    "status": True
                }
        return {}
    ret = {
        'video_id': video_id,
        'provider': provider,
        'clean_code': clean_code,
        'real_link': real_link}
    try:
        Api = PROVIDERS_API[provider]
    except KeyError:
        sys.exit()
    api = Api()
    try:
        if api.check(video_id):
            details = api.video_data
            ret.update(details)
        else:
            print("details error")
    except APIError, e:
        print("status: False")
        print("{}: {}".format(provider, e))
    return ret

def main():
    parser = argparse.ArgumentParser(description='Video Embed Code Cleaner.')
    parser.add_argument(
        '-t', '--timeout',
        type=float,
        default=10,
        help='timeout for the validation (10 seconds by default)')
    subparsers = parser.add_subparsers(title='sub-commands')

    parser_clean = subparsers.add_parser('clean', help='clean the embed code')
    parser_clean.add_argument('code', help='video embed code to clean')
    parser_clean.add_argument(
        '-v', '--validate', action='store_true',
        help='also validate that the video is still available')
    parser_clean.set_defaults(func=clean)

    parser_validate = subparsers.add_parser(
        'validate', help='validate that the video is still available')
    parser_validate.add_argument('video_id', help='id of the video')
    parser_validate.add_argument('provider', help='provider of the video')
    parser_validate.set_defaults(func=valid)

    parser_extract = subparsers.add_parser(
        'extract', help='Extract informations from the video')
    parser_extract.add_argument('code',
        help='video embed code from which extract infos')
    parser_extract.set_defaults(func=extract)

    args = parser.parse_args()
    ret = extract(args.code)
    print(ret)


if __name__ == '__main__':
    main()
