#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Test isbn.py module."""


import unittest

from src import isbn_oclc
from src.isbn_oclc import isbn_sfn_cit_ref, oclc_sfn_cit_ref
from test import DummyRequests


class IsbnTest(unittest.TestCase):

    def test_is1(self):
        """not found in adinebook"""
        self.assertIn((
            '* {{cite book '
            '| last=Adkins '
            '| first=Roy '
            '| title=The war for all the oceans : '
            'from Nelson at the Nile to Napoleon at Waterloo '
            '| publisher=Abacus '
            '| publication-place=London '
            '| year=2007 '
            '| isbn=978-0-349-11916-8 '
            '| oclc=137313052 '
            '| ref=harv}}'
        ), isbn_sfn_cit_ref('9780349119168', pure=True)[1])

    def test_is2(self):
        """not found in ottobib"""
        self.assertIn((
            '* {{cite book '
            '| others=بدیل بن علی خاقانی (شاعر),  جهانگیر منصور (به اهتمام),'
            ' and  بدیع الزمان فروزانفر (مقدمه) '
            '| title=دیوان خاقانی شروانی '
            '| publisher=نگاه '
            '| year=1389 '
            '| isbn=978-964-6736-71-9 '
            '| language=fa '
            '| ref={{sfnref | نگاه | 1389}}'
        ), isbn_sfn_cit_ref('978-964-6736-71-9', pure=True)[1])

    def test_is3(self):
        """exists in both"""
        self.assertIn((
            '* {{cite book '
            '| others=سحر معصومی (به اهتمام) '
            '| title=راز گل سرخ: نقد و گزیده شعرهای سهراب سپهری '
            '| publisher=نگاه '
            '| year=1386 '
            '| isbn=964-6736-34-3 '
            '| oclc=53446327 '
            '| language=fa '
            '| ref={{sfnref | نگاه | 1386}}'
        ), isbn_sfn_cit_ref('964-6736-34-3 ')[1])

    def test_is4(self):
        """unpure isbn10 not found in ottobib"""
        self.assertIn((
            '* {{cite book '
            '| last=حافظ '
            '| first=شمس الدین محمد '
            '| others= رضا نظرزاده (به اهتمام) '
            '| title=دیوان کامل حافظ همراه با فالنامه '
            '| publisher=دیوان '
            '| year=1385 '
            '| isbn=964-92962-6-3 '
            '| language=fa '
            '| ref=harv'
        ), isbn_sfn_cit_ref('choghondar 964-92962-6-3 شلغم')[1])


class OCLCTest(unittest.TestCase):

    def test_oclc1(self):
        self.maxDiff = None
        self.assertEqual((
            '* {{cite book '
            '| last=Lewis '
            '| first=James Bryant '
            '| last2=Sesay '
            '| first2=Amadu '
            '| title=Korea and globalization :'
            ' politics, economics and culture '
            '| publisher=RoutledgeCurzon '
            '| year=2002 '
            '| isbn=0-7007-1512-6 '
            '| oclc=875039842 '
            '| ref=harv}}'
        ), oclc_sfn_cit_ref('875039842')[1])

    def test_elec_type_with_url(self):
        self.assertIn((
            "* {{cite web "
            "| last=Rahman "
            "| first=Mizanur "
            "| title=MediaWiki Administrators' Tutorial Guide. "
            "| publisher=Packt Pub. "
            "| year=2007 "
            "| isbn=978-1-84719-045-1 "
            "| oclc=809771201 "
            "| url=http://public.eblib.com/choice/publicfullrecord.aspx?p="
            "995605 "
            "| ref=harv "
            "| access-date="
        ), oclc_sfn_cit_ref('809771201')[1])

    def test_fullname_in_ris(self):
        self.assertEqual((
            '* {{cite book '
            '| author=Universidade Federal do Rio de Janeiro '
            '| title=Universidade do Brasil, 1948-1966. '
            '| year=1966 '
            '| oclc=24680975 '
            '| language=pt '
            '| ref=harv}}'
        ), oclc_sfn_cit_ref('24680975')[1])


isbn_oclc.requests_get = DummyRequests().get
if __name__ == '__main__':
    unittest.main()
