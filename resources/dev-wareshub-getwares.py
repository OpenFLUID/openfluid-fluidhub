
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os
import requests

import common


################################################################################
################################################################################


def getWare(Type,ID) :
  URL = "http://127.0.0.1:3447/wares/%s/%s" % (Type,ID)
  Headers = {
     'cache-control': "no-cache",
  }

  print URL
  Response = requests.request("Get", URL, headers=Headers)
  print Response.status_code,":",Response.text


################################################################################


def getWares(Type) :
  URL = "http://127.0.0.1:3447/wares/%s" % (Type)
  Headers = {
     'cache-control': "no-cache",
  }

  print URL
  Response = requests.request("Get", URL, headers=Headers)
  print Response.status_code,":",Response.text


################################################################################


def getAllWares() :
  URL = "http://127.0.0.1:3447/wares"
  Headers = {
     'cache-control': "no-cache",
  }

  print URL
  Response = requests.request("Get", URL, headers=Headers)
  print Response.status_code,":",Response.text



################################################################################
################################################################################


for Type, IDs in common.Wares.iteritems():
  for ID in IDs:
    getWare(Type,ID)
  getWares(Type)

getAllWares()
