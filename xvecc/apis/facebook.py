#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import json
import requests
import re
import facepy
from facepy.exceptions import FacebookError

from .webapi import WebAPI, APIError, convertduration


def set_fb_token(token):
    FacebookAPI.__token__ = token


class FacebookAPI(WebAPI):
    __token__ = 'not_set_put_one'
    __part__ = 'description,length,picture,source,title,status,published,privacy'
    __url__ = ('/v2.5/{video_id}?fields={part}')

    def __init__(self):
        self._data = {}
        self._results = None
        self._video_id = 0

    def _call_api(self):
        fb  = facepy.GraphAPI(self.__token__)
        built_url = self.__url__.format(
            video_id=self._video_id,
            part=self.__part__)
        try:
            answer = fb.get(built_url)
            if "description" in answer:
                self._data = answer
                return True
            else:
                return False
        except FacebookError as fber:
            raise APIError(fber.code, fber.message)
        except:
            raise APIError(500, "Facebook API Error")


    def _is_ok(self):
        """Extract privacy policy and upload status to determine availability."""
        if (self._data['status']['video_status'] == 'ready' and
            self._data['published'] and
            self._data['privacy']['value'] == 'EVERYONE'):
            return True
        return False

    def check(self, video_id):
        if video_id != self._video_id:
            self._results = None
        self._video_id = video_id
        return self._call_api()

    @property
    def video_data(self):
        if not self._data:
            return {}
        if not self._results:
            self._results = {
                'title': self._data['title'],
                'description': self._data['description'],
                'image': self._data['picture'],
                'duration': convertduration(self._data['length']),
                'status': self._is_ok()
            }
        return self._results
