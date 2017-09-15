
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os
import requests

import common


################################################################################
################################################################################


def createWare(Type,ID) :
  URL = "http://127.0.0.1:3447/api/wares/%s/%s" % (Type,ID)
  Headers = {
     'content-type': "application/json",
     'authorization': "Token %s" % common.AccessToken,
     'cache-control': "no-cache",
  }

  with open(os.path.join(common.ResourcesPath,"tests","definitions",ID+".json")) as DefFile :
    Payload = DefFile.read()
    Response = requests.request("PUT", URL, data=Payload, headers=Headers)
    print Response.status_code,":",Response.text


################################################################################
################################################################################


for Type, IDs in common.Wares.iteritems():
  for ID in IDs:
    createWare(Type,ID)
