#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests,urllib,sys
import re
import sys

s = requests.session()
firstreq = s.get('http://clickandpay.ru/login/')
#if (firstreq.status_code == requests.codes.ok):
#       print firstreq.headers['content-type']

def javalue_parser(text):
        javalue = re.findall(r'name="javax.faces.ViewState" id="javax.faces.ViewState" value="(.*?)"', text)
        return javalue[0]

payload = urllib.urlencode({
        'loginForm': 'loginForm',
        'phone': '+7(123)333-22-41',
        'javax.faces.ViewState': '%s' % javalue_parser(firstreq.text),
        'javax.faces.partial.ajax': 'true',
        'javax.faces.source': 'nextButton',
        'javax.faces.partial.execute': '@all',
        'javax.faces.partial.render': 'loginPanel',
        'javax.faces.behavior.event': 'action'
        })

payload2 = urllib.urlencode({
        'loginForm': 'loginForm',
        'password': 'PASSWORD',
        'javax.faces.ViewState': '%s' % javalue_parser(firstreq.text),
        'javax.faces.partial.ajax': 'true',
        'javax.faces.source': 'validatePassword',
        'javax.faces.partial.execute': 'validatePassword password',
        'javax.faces.partial.render': 'loginPanel messagePanel',
        'javax.faces.behavior.event': 'action'
        })
		

#print payload
url = 'http://clickandpay.ru/login.jsp'
headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'x-requested-with': 'XMLHttpRequest', 'Faces-Request': 'partial/ajax'}

secreq = s.post(url, data=payload, headers=headers)
if (secreq.status_code == requests.codes.ok):
	thirdreq = s.post(url, data=payload2, headers=headers)
	#print thirdreq.text

s.get('http://clickandpay.ru/sms/')
r = s.get("http://clickandpay.ru/sms/")
#print r.text

smsreq = s.get('http://clickandpay.ru/sms/')
#if (smsreq.status_code == requests.codes.ok):
#        print smsreq.headers['content-type']


smsload = urllib.urlencode({
        'smsForm': 'smsForm',
        #'toPhone': '+7(123)345-01-02',
        'toPhone': sys.argv[1],
        'numberOfSymbolsHidden': '5',
        'numberOfSmsHidden': '1',
        'limitHidden': '160',
        'smsMessage': sys.argv[2],
        'timeToSendField': '',
        'dateToSendField_input': '',
        'javax.faces.ViewState': '%s' % javalue_parser(smsreq.text),
        'javax.faces.partial.ajax': 'true',
        'javax.faces.source': 'sendSmsButton',
        'javax.faces.partial.execute': 'smsForm',
        'javax.faces.partial.render': 'smsForm smsErrors smsListForm',
        'javax.faces.behavior.event': 'action'
        })


sendsms = s.post('http://clickandpay.ru/sms/', data=smsload, headers=headers)
#if (quadreq.status_code == requests.codes.ok):
#	print quadreq.text
#print s.text
