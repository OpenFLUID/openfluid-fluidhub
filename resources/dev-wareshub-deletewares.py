
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os
import requests

import common


################################################################################
################################################################################


def deleteWare(Type,ID) :
  URL = "http://127.0.0.1:3447/wares/%s/%s" % (Type,ID)
  Headers = {
     'content-type': "application/json",
     'authorization': "Token %s" % common.AccessToken,
     'cache-control': "no-cache",
  }


  Response = requests.request("DELETE", URL, headers=Headers)
  print Response.status_code,":",Response.text


################################################################################
################################################################################


for Type, IDs in common.Wares.iteritems():
  for ID in IDs:
    deleteWare(Type,ID)
