#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Codes required to create citation templates for wikifa."""


from datetime import date
import re


def sfn_template(d):
    """Create sfn template using the given dictionary."""
    if 'authors' in d:
        s = '<ref>{{پک'
        c = 0
        for name in d['authors']:
            c += 1
            if c < 5:  # {{پک}} only accepts a maximum of four authors
                s += '|' + name.lastname
    else:
        s = '<ref>{{پک/بن'
    if 'year' in d:
        s += '|' + d['year']
    if 'title' in d:
        s += '|ک=' + d['title']
    if 'language' in d:
        s += '|زبان=' + d['language']
    s += '|ص='
    if 'pages' in d:
        s += d['pages']
    s += '}}</ref>'
    return s


def citation_template(d, date_format):
    """Create citation template using the given dictionary."""
    if d['type'] == 'book':
        s = '* {{یادکرد کتاب'
    elif d['type'] in ['article', 'jour']:
        s = '* {{یادکرد ژورنال'
    elif d['type'] == 'web':
        s = '* {{یادکرد وب'
    else:
        raise KeyError(d['type'] + " is not a valid value for d['type']")

    if 'authors' in d:
        s += names2para(d['authors'],
                        'نام',
                        'نام خانوادگی'
                        'نویسنده')
    if 'editors' in d:
        s += names2para(d['editors'],
                        'نام ویراستار',
                        'نام خانوادگی ویراستار',
                        'ویراستار')
    if 'translators' in d:
        s += names1para(d['translators'], 'ترجمه')
    if 'others' in d:
        s += names1para(d['others'], 'دیگران')
    if 'title' in d:
        s += '|عنوان=' + d['title']
    if 'journal' in d:
        s += '|ژورنال=' + d['journal']
    elif 'website' in d:
        s += '|وب‌گاه=' + d['website']
    if 'publisher' in d:
        s += '|ناشر=' + d['publisher']
    if 'address' in d:
        s += '|مکان=' + d['address']
    if 'series' in d:
        s += '|سری=' + d['series']
    if 'volume' in d:
        s += '|جلد=' + d['volume']
    if 'issue' in d:
        s += '|شماره=' + d['issue']
    if 'year' in d:
        s += '|سال=' + d['year']
    if 'month' in d:
        s += '|ماه=' + d['month']
    if 'isbn' in d:
        s += '|شابک=' + d['isbn']
    if d['type'] == 'article' or d['type'] == 'jour':
        if 'pages' in d:
            s += '|صفحه=' + d['pages']
    if 'url' in d:
        s += '|پیوند=' + d['url']
    if 'doi' in d:
        s += '|doi=' + d['doi']
    if 'language' in d:
        s += '|زبان=' + d['language']
    if 'url' in d:
        s += '|تاریخ بازبینی=' + date.isoformat(date.today())
    s += '}}'
    return s


def names2para(names, fn_parameter, ln_parameter, nofn_parameter=None):
    """Take list of names. Return the string to be appended to citation."""
    c = 0
    s = ''
    for name in names:
        c += 1
        if c == 1:
            if name.firstname or not nofn_parameter:
                s += '|' + ln_parameter + '=' + name.lastname
                s += '|' + fn_parameter + '=' + name.firstname
            else:
                s += '|' + nofn_parameter + '=' + name.fullname
        else:
            if name.firstname or not nofn_parameter:
                s += '|' + ln_parameter + commons.ennum2fa(c) + '=' +\
                     name.lastname
                s += '|' + fn_parameter + commons.ennum2fa(c) + '=' +\
                     name.firstname
            else:
                s += '|' + nofn_parameter + commons.ennum2fa(c) +\
                     '=' + name.fullname
    return s


def names1para(translators, para):
    """Take list of names. Return the string to be appended to citation."""
    s = '|' + para + '='
    c = 0
    for name in translators:
        c += 1
        if c == 1:
            s += name.fullname
        elif c == len(translators):
            s += ' و ' + name.fullname
        else:
            s += '، ' + name.fullname
    return s
