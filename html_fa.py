#! /usr/bin/python
# -*- coding: utf-8 -*-

"""HTML skeleton of the application and its predefined responses."""


from string import Template
from datetime import date

class Respose:

    """Create the responce object used by the main application."""

    def __init__(self, sfnt, ctnt='', reft='', error='100'):
        self.sfnt = sfnt
        self.ctnt = ctnt
        self.reft = reft
        self.error = error


def response_to_template(response):
    """Insert the response into the template and return response_body."""
    return template % (response.sfnt,
                       response.ctnt,
                       response.reft,
                       response.error)


template = Template("""<!DOCTYPE html>
<html dir="rtl">
    <head>
        <title>یادفا (ابزار ساخت یادکرد برای ویکی‌پدیای فارسی)</title>
        <style type="text/css">

            textarea, input {
                transition: background-color 5s ease-in;
                background-color: rgb(255, 255, 255);
                border: 1px solid rgb(204, 204, 204);
                padding: 2px 2px;
                margin-bottom: 10px;
                font-size: 14px;
                line-height: 16px;
                color: rgb(85, 85, 85);
                vertical-align: middle;
                border-radius: 5px 5px 5px 5px;
                }
            textarea{
                display:block;
                margin-left: auto;
                margin-right: auto;
                width:100%;
                word-break: break-all;
                }
            body {
                font-family: tahoma;
                font-size:0.8em
                }
            input[type=text]{
                width:50%;
                }
            input[type=submit]{
                float:left;
                }
            #info{
                font-size:90%;
                color:#666666;
                }
            input[type=submit]:hover{
                transition: background-color 1s ease-in;
                background-color:#33CC33;
                }
        </style>
    </head>
    <body>
        <div style="margin-left:auto; margin-right:auto; width:62%;">
            <form method="get" action="yadkard.fcgi">
                <p>
                    نشانی وب/شابک/شناسهٔ برنمود رقمی:<br><input type="text" name="user_input">
                    <input type="submit" value="ثبت درخواست">
                </p>
            </form>
            <p>
                <a href="https://en.wikipedia.org/wiki/Help:Shortened_footnotes">پانویس کوتاه‌شده</a> و یادکرد:<br>
                <textarea rows="6" readonly>$s\n\n$s</textarea>
                <a href="https://en.wikipedia.org/wiki/Wikipedia:NAMEDREFS#WP:NAMEDREFS">برچسب ارجاع درون‌خطی</a>:<br>
                <textarea rows="4" readonly>$s</textarea>
            </p>
            <p>
                <!-- There may be error in language detection. $s % -->
            </p>
            <div id="info">
                <p>
                        با استفاده از این ابزار می‌توانید برچسب ارجاع (تگ <ref>) و یا پانویس کوتاه‌دشده و یادکرد مورد استفاده در ویکی‌پدیای فارسی برای ارجاع به منابع را بسازید. ابزار موارد زیر را به عنوان ورودی می‌پذیرد:</p>
                <p>
                        نشانی وب <a href="http://books.google.com/">کتاب‌های گوگل</a>، <a href="https://en.wikipedia.org/wiki/Digital_object_identifier">شناسانۀ برنمود رقمی</a>، یا <a href="https://en.wikipedia.org/wiki/International_Standard_Book_Number">شابک</a> (حتی برای بسیاری از کتاب‌های فارسی).</p>
                <p>
                        افزون بر این‌ها می‌توانید نشانی وب خبرهای بسیاری از خبرگزاری‌های مهم را نیز در آن آزمایش کنید. توجه داشته باشید که همواره احتمال خطا در خروجی ابزار وجود دارد و نیازمند بازبینی خواهد بود. <b>با مسئولیت خودتان از آن استفاده کنید.<b></p>
            </div>
        </div>
        <script>
            function setCookie(cname, cvalue, exdays) {
                var d = new Date();
                d.setTime(d.getTime() + (exdays*24*60*60*1000));
                var expires = "expires="+d.toGMTString();
                document.cookie = cname + "=" + cvalue + "; " + expires;
            }

            function getCookie(cname) {
                var name = cname + "=";
                var ca = document.cookie.split(';');
                for(var i=0; i<ca.length; i++) {
                    var c = ca[i].trim();
                    if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
                }
                return "";
            }

            function checkCookie() {
                var datefmt = getCookie('datefmt');
                if (datefmt != '') {
                  document.getElementById(datefmt).checked = true;
                }
            }
            checkCookie()
        </script>
    </body>
</html>""")

# Predefined responses
default_response = Respose('یادکرد ساخته‌شده اینجا نمایان خواهد شد...',
                           '',
                           '',
                           '??')

undefined_url_response = Respose('ورودی شناخته نشد.',
                                 'خطا در سیاههٔ خطاها ثبت شد.')

httperror_response = Respose('خطای اچ‌تی‌تی‌پی:',
                             'یک یا چند مورد از منابع اینترنتی مورد ' +
                             'نیاز برای ساخت این یادکرد در این لحظه ' +
                             'در دسترس نیستند. (و یا ورودی نامعتبر است)')

other_exception_response = Respose('خطای ناشناخته‌ای رخ داد..',
                                   'اطلاعات خطا در سیاهه ثبت شد.')

today = date.today()
template = template.safe_substitute({'Ymd': today.strftime('%Y-%m-%d'),
                                     'BdY': today.strftime('%B %d, %Y'),
                                     'bdY': today.strftime('%b %d, %Y'),
                                     'dBY': today.strftime('%d %B %Y'),
                                     'dbY': today.strftime('%d %b %Y'),
                                     }).replace('%', '%%').replace('$', '%')

