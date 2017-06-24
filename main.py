#! /usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict
import logging
import logging.handlers
from urllib.parse import parse_qs, urlparse, unquote
from html import unescape
from wsgiref.headers import Headers

try:
    from flup.server.fcgi import WSGIServer
except ImportError:
    from wsgiref.simple_server import make_server
import requests

from config import lang
from src.adinebook import adinehbook_response
from src.commons import uninum2en, response_to_json
from src.doi import doi_response, DOI_SEARCH
from src.googlebooks import googlebooks_response
from src.isbn import ISBN_10OR13_SEARCH, IsbnError, isbn_response
from src.noorlib import noorlib_response
from src.noormags import noormags_response
from src.pubmed import pmcid_response, pmid_response
from src.urls import urls_response
from src.waybackmachine import waybackmachine_response
if lang == 'en':
    from src.html.en import (
        DEFAULT_RESPONSE,
        UNDEFINED_INPUT_RESPONSE,
        HTTPERROR_RESPONSE,
        OTHER_EXCEPTION_RESPONSE,
        response_to_html,
        CSS,
        CSS_HEADERS,
        JS,
        JS_HEADERS,
    )
else:
    from src.html.fa import (
        DEFAULT_RESPONSE,
        UNDEFINED_INPUT_RESPONSE,
        HTTPERROR_RESPONSE,
        OTHER_EXCEPTION_RESPONSE,
        response_to_html,
        CSS,
        CSS_HEADERS,
    )


NETLOC_RESPONSE_GET = {
    'www.adinehbook.com': adinehbook_response,
    'www.adinebook.com': adinehbook_response,
    'adinebook.com': adinehbook_response,
    'adinehbook.com': adinehbook_response,
    'www.noorlib.ir': noorlib_response,
    'www.noorlib.com': noorlib_response,
    'noorlib.com': noorlib_response,
    'noorlib.ir': noorlib_response,
    'www.noormags.ir': noormags_response,
    'www.noormags.com': noormags_response,
    'noormags.com': noormags_response,
    'web.archive.org': waybackmachine_response,
    'web-beta.archive.org': waybackmachine_response,
}.get

RESPONSE_HEADERS = Headers([('Content-Type', 'text/html; charset=UTF-8')])


def mylogger():
    custom_logger = logging.getLogger()
    custom_logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(
        filename='yadkard.log',
        mode='a',
        maxBytes=20000,
        backupCount=0,
        encoding='utf-8',
        delay=0
    )
    handler.setLevel(logging.INFO)
    fmt = '\n%(asctime)s\n%(levelname)s\n%(message)s\n'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    custom_logger.addHandler(handler)
    return custom_logger


def url_doi_isbn_response(user_input, date_format):
    en_user_input = unquote(uninum2en(user_input))
    # Checking the user input for dot is important because
    # the use of dotless domains is prohibited.
    # See: https://features.icann.org/dotless-domains
    if '.' in en_user_input:
        # Try predefined URLs
        # Todo: The following code could be done in threads.
        if not user_input.startswith('http'):
            url = 'http://' + user_input
        else:
            url = user_input
        netloc = urlparse(url)[1]
        if '.google.com/books' in url:
            return googlebooks_response(url, date_format)
        response_getter = NETLOC_RESPONSE_GET(netloc)
        if response_getter:
            return response_getter(url, date_format)
        # DOIs contain dots
        m = DOI_SEARCH(unescape(en_user_input))
        if m:
            return doi_response(m.group(1), pure=True, date_format=date_format)
        return urls_response(url, date_format)
    else:
        # We can check user inputs containing dots for ISBNs, but probably is
        # error prone.
        m = ISBN_10OR13_SEARCH(en_user_input)
        if m:
            try:
                return isbn_response(m.group(), True, date_format)
            except IsbnError:
                pass
        return UNDEFINED_INPUT_RESPONSE


def application(environ, start_response):
    query_dict_get = parse_qs(environ['QUERY_STRING']).get

    path_info = environ['PATH_INFO']
    if '/static/' in path_info:
        if path_info.endswith('.css'):
            start_response('200 OK', CSS_HEADERS)
            return [CSS]
        else:
            # path_info.endswith('.js') and config.lang == 'en'
            start_response('200 OK', JS_HEADERS)
            return [JS]

    date_format = query_dict_get('dateformat', [''])[0].strip()

    input_type = query_dict_get('input_type', [''])[0]

    # Warning: input is not escaped!
    user_input = query_dict_get('user_input', [''])[0].strip()
    if not user_input:
        response_body = response_to_html(
            DEFAULT_RESPONSE, date_format, input_type
        ).encode()
        RESPONSE_HEADERS['Content-Length'] = str(len(response_body))
        start_response('200 OK', RESPONSE_HEADERS.items())
        return [response_body]

    output_format = query_dict_get('output_format', [''])[0]  # apiquery

    resolver = input_type_to_resolver[input_type]
    # noinspection PyBroadException
    try:
        response = resolver(user_input, date_format)
    except requests.ConnectionError:
        status = '500 ConnectionError'
        logger.exception(user_input)
        if output_format == 'json':
            response_body = response_to_json(HTTPERROR_RESPONSE)
        else:
            response_body = response_to_html(
                HTTPERROR_RESPONSE, date_format, input_type
            )
    except Exception:
        status = '500 Internal Server Error'
        logger.exception(user_input)
        if output_format == 'json':
            response_body = response_to_json(OTHER_EXCEPTION_RESPONSE)
        else:
            response_body = response_to_html(
                OTHER_EXCEPTION_RESPONSE, date_format, input_type
            )
    else:
        status = '200 OK'
        if output_format == 'json':
            response_body = response_to_json(response)
        else:
            response_body = response_to_html(response, date_format, input_type)
    response_body = response_body.encode()
    RESPONSE_HEADERS['Content-Length'] = str(len(response_body))
    start_response(status, RESPONSE_HEADERS.items())
    return [response_body]


input_type_to_resolver = defaultdict(
    lambda: url_doi_isbn_response, {
    'url-doi-isbn': url_doi_isbn_response,
    'pmid': pmid_response,
    'pmcid': pmcid_response,
})

if __name__ == '__main__':
    logger = mylogger()
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("langid").setLevel(logging.WARNING)
    try:
        # on remote server
        WSGIServer(application).run()
    except NameError:
        # on local computer
        httpd = make_server('localhost', 5000, application)
        httpd.serve_forever()
