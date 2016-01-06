#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import json
import requests

from functools import wraps

from .webapi import WebAPI, APIError


class VimeoAPI(WebAPI):
    __token__ = 'dff3840be8c1286f4404fc357f2dc0e8'
    __key__ = ''
    __secret__ = ''
    __scope__ = ['public', 'private']
    __url__ = 'https://api.vimeo.com/videos/{video_id}'

    __api_root__ = 'https://api.vimeo.com'
    __headers__ = {
        'Accept': 'application/vnd.vimeo.*;version=3.2',
    }

    def __init__(self):
        self.token = self.__token__
        self._data = {}
        self._results = None
        self._video_id = 0

    # Internally we back this with an auth mechanism for Requests.
    @property
    def token(self):
        return self._token.token

    @token.setter
    def token(self, value):
        self._token = _BearerToken(value) if value else None

    def _call_api(self):
        url = self.__url__.format(video_id=self._video_id)

        @wraps(requests.get)
        def caller():
            """Wrapper around requests.get to add the Vimeo token.

            Strongly inspired from the official Vimeo API at
            https://github.com/vimeo/vimeo.py/blob/master/vimeo/client.py"""
            kwargs = {
                'timeout': 10,
                'auth': self._token,
                'headers': self.__headers__,
            }

            return requests.get(url, **kwargs)

        answer = caller()
        if answer.status_code < 300:
            self._data = json.loads(answer.content)
            return True

        # Manage error situations
        error_msg = 'Unbound Source Error'
        if 300 <= answer.status_code < 400:
            error_msg = 'HTTP Redirection'
        if 400 <= answer.status_code < 500:
            error_msg = 'HTTP Client Error'
        if 500 <= answer.status_code < 600:
            error_msg = 'HTTP Server Error'
        raise APIError(answer.status_code, error_msg)

    def _parse_duration(self, vduration):
        """Convert seconds to 'day hours:minutes:seconds'."""
        duration_list = [vduration % 60, ]  # Seconds
        days = 0

        for val in (60, 60):  # Minutes, then hours
            if vduration > val:
                vduration = vduration / val
                duration_list.append(vduration % val)
        duration_str = ":".join([str(e) for e in reversed(duration_list)])

        if vduration > 24:
            days = vduration / 24
            duration_str = "{} {}".format(days, duration_str)

        return duration_str

    def _get_best_picture(self, pics_info):
        """Get the best picture available or None."""
        if not pics_info['active']:
            return None
        pic_path = ''
        pic_size = (0, 0)
        for pic in pics_info['sizes']:
            if pic['width'] > pic_size[0] and pic['height'] > pic_size[1]:
                pic_size = (pic['width'], pic['height'])
                pic_path = pic['link']
        ridx = pic_path.rfind("?")
        if ridx != -1:
            pic_path = pic_path[0:ridx]
        return pic_path

    def _is_ok(self, status, privacy):
        if status == 'available' and privacy['view'] == 'anybody':
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
                'title': self._data['name'],
                'description': self._data['description'],
                'image': self._get_best_picture(self._data['pictures']),
                'duration': self._parse_duration(self._data['duration']),
                'status': self._is_ok(
                    self._data['status'],
                    self._data['privacy'])
            }
        return self._results


class _BearerToken(requests.auth.AuthBase):
    """Model the bearer token and apply it to the request."""
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers['Authorization'] = 'Bearer ' + self.token
        return request
