# -*- coding: utf-8 -*-
from __future__ import absolute_import
from scrapy import log
from scrapy.contrib.spidermiddleware.httperror import HttpError


class Handle404Middleware(object):
    """
    Handle '404' pages.
    """

    def __init__(self, settings):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_response(self, request, response, spider):

        if response.status == 404:
            try:
                return response.meta['item']
            except KeyError:
                raise HttpError(response, '404 page with no item to return')
        elif 200 <= response.status < 300:  # common case
            return
        raise HttpError(response, 'Ignoring non-200 response')

    def process_spider_exception(self, response, exception, spider):
        if isinstance(exception, HttpError):
            log.msg(
                format="Ignoring response %(response)r: HTTP status code is not handled or not allowed",
                level=log.DEBUG,
                spider=spider,
                response=response
            )
            return []