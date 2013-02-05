#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests,sys
import re
import urllib.parse
import urllib
import sys

s = requests.session()
firstreq = s.get('http://clickandpay.ru/login/')
#if (firstreq.status_code == requests.codes.ok):
#       print firstreq.headers['content-type']

def javalue_parser(text):
        javalue = re.findall(r'name="javax.faces.ViewState" id="javax.faces.ViewState" value="(.*?)"', text)
        return javalue[0]

payload = urllib.parse.urlencode({
        'loginForm': 'loginForm',
        'phone': '+7(123)456-12-81',
        'javax.faces.ViewState': '%s' % javalue_parser(firstreq.text),
        'javax.faces.partial.ajax': 'true',
        'javax.faces.source': 'nextButton',
        'javax.faces.partial.execute': '@all',
        'javax.faces.partial.render': 'loginPanel',
        'javax.faces.behavior.event': 'action'
        })

payload2 = urllib.parse.urlencode({
        'loginForm': 'loginForm',
        'password': 'myc00lpwd',
        'javax.faces.ViewState': '%s' % javalue_parser(firstreq.text),
        'javax.faces.partial.ajax': 'true',
        'javax.faces.source': 'validatePassword',
        'javax.faces.partial.execute': 'validatePassword password',
        'javax.faces.partial.render': 'loginPanel messagePanel',
        'javax.faces.behavior.event': 'action'
        })

#print(payload)
url = 'http://clickandpay.ru/login.jsp'
headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 
		'x-requested-with': 'XMLHttpRequest',
		'Faces-Request': 'partial/ajax',
		'Referer': 'http://clickandpay.ru/clickphone/',
		'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
		'Accept-Charset' : 'windows-1251,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'gzip,deflate,sdch',
		'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.58 Safari/537.22',
		}

secreq = s.post(url, data=payload, headers=headers)
if (secreq.status_code == requests.codes.ok):
	thirdreq = s.post(url, data=payload2, headers=headers)
#<extension primefacesCallbackParam="valid">{"valid":true}</extension><extension
#check for auth validation
#	print (thirdreq.text)

smsreq = s.get('http://clickandpay.ru/clickphone/')
#if (smsreq.status_code == requests.codes.ok):
#        print(smsreq.headers['content-type'])
shitload = {
	'callMessageNotificationForm':'callMessageNotificationForm',
	'javax.faces.ViewState':'%s' % javalue_parser(smsreq.text),
	'javax.faces.partial.ajax':'true',
	'javax.faces.source':'j_idt214',
	'javax.faces.partial.execute':'@all',
	'javax.faces.partial.render':'zvonilka_panel',
	'j_idt214':'j_idt214',
}

a = s.post('http://clickandpay.ru/clickphone.jsp', data=shitload, headers=headers)

smsload = {
	'j_idt409:j_idt411': 'j_idt409:j_idt411',
	'j_idt409:j_idt411:calleeText': sys.argv[1],
	'j_idt409:j_idt411:userContactsFilter': '',
        'javax.faces.ViewState': '%s' % javalue_parser(smsreq.text),
	'javax.faces.partial.ajax': 'true',
	'javax.faces.source': 'j_idt409:j_idt411:j_idt416',
	'javax.faces.partial.execute': 'j_idt409:j_idt411',
	'javax.faces.partial.render': 'smsDealPanel',
	'j_idt409:j_idt411:j_idt416': 'j_idt409:j_idt411:j_idt416'
	}

smsload2 = {
	'j_idt462:smsForm': 'j_idt462:smsForm',
	'j_idt462:options': 'MT_SMS',
	'j_idt462:smsMessage': sys.argv[2],
	'j_idt462:numberOfSymbolsHidden':'5',
	'j_idt462:numberOfSmsHidden':'1',
	'j_idt462:limitHidden': '160',
	'j_idt462:timeToSendField': '',
	'j_idt462:dateToSendField_input': '',
        'javax.faces.ViewState': '%s' % javalue_parser(smsreq.text),
	'javax.faces.partial.ajax': 'true',
	'javax.faces.source': 'j_idt462:j_idt485',
	'javax.faces.partial.execute': 'j_idt462:smsForm j_idt462:options',
	'javax.faces.partial.render':'j_idt462:smsForm smsDealPanel',
	'j_idt462:j_idt485':'j_idt462:j_idt485'
        }
#print(smsload)
url = 'http://clickandpay.ru/clickphone.jsp'
sendsms = s.post(url, data=smsload, headers=headers)
if (sendsms.status_code == requests.codes.ok):
	thirdreq = s.post(url, data=smsload2, headers=headers)

#print(sendsms)
