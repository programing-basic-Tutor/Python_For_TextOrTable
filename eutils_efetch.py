#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import socket, time

print os.getcwd()

ID_list = [a.rstrip() for a in open("nocl_id.txt",'r').readlines()]

base = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
## search = {"db": "taxonomy", "id": "2057", "retmode":"xml"}
user_agent="Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
headers = {'User-Agent':user_agent}

output = open("tax_result.txt",'w')

timeout = 5
socket.setdefaulttimeout(timeout)
sleep_download_time = 3

for order_id in ID_list:
    
    search = {"db": "taxonomy", "id": order_id, "retmode":"xml"}
    values = urllib.urlencode(search)
    try:
        time.sleep(sleep_download_time)
        request = urllib2.Request(base, values, headers)
        response = urllib2.urlopen(request)
        page = response.read()
        response.close()
    except UnicodeDecodeError as e:
        print ('------UnicodeDecodeError url:', order_id)
    except urllib2.URLError as e:
        print ('------urlError url:',order_id)
    except socket.timeout as e:
        print ('------socket timeout:', order_id)
    
    
    soup = BeautifulSoup(page)
    #print soup.prettify()

    lineage = str(soup.taxaset.lineage.contents[0])
    #print lineage
    line = lineage.split("; ")
    line.reverse()
    rever_line = line
    #print [order_id, ";".join(rever_line)]
    output.write("\t".join([order_id, ";".join(rever_line)])+"\n")

output.close()
