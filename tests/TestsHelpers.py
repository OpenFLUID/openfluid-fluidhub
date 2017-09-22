
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os
import requests
import errno
import json


################################################################################
################################################################################


TestsPath = os.path.dirname(os.path.abspath(__file__))
RootPath = os.path.dirname(TestsPath)
ServerPath = os.path.join(RootPath,"_dev","server")
DataServerPath = os.path.join(ServerPath,"data")
LocalPath = os.path.join(RootPath,"_dev","local")
LocalWaresPath = os.path.join(LocalPath,"wares")


FluidhubAddr = "127.0.0.1:3447"
if "FLUIDHUB_ADDR" in os.environ :
  FluidhubAddr = os.environ["FLUIDHUB_ADDR"]


Wares = { "simulators" : ["sim.01","sim.02","sim.03"],
          "observers" : ["obs.01","obs.02"],
          "builderexts" : ["bext.01"]
        }

Users = {
          "user1" : {
            "password" : "user1"
          },
          "user2" : {
            "password" : "user2",
            "fullname" : "User 2"
          },
          "user3" : {
            "password" : "user3",
            "fullname" : "User 3",
            "email" : "user3@users.org"
          }
        }


################################################################################
################################################################################


def executeGetRequest(URL,Headers=dict()):
  Headers['cache-control'] = "no-cache"
  Response = requests.request("Get", URL, headers=Headers)
  return Response


################################################################################


def executePutRequest(URL,Data,Headers=dict()):
  Headers['cache-control'] = "no-cache"
  Response = requests.request("Put", URL, data=Data,headers=Headers)
  return Response


################################################################################


def executeDeleteRequest(URL,Headers=dict()):
  Headers['cache-control'] = "no-cache"
  Response = requests.request("Delete", URL, headers=Headers)
  return Response


################################################################################


def printResponse(Response):
  print Response.url,":",Response.status_code
  print Response.text


################################################################################


def askForToken(Username,Password):
  Response = requests.get("http://%s/api/users/auth" % FluidhubAddr, auth=(Username,Password))
  JSON = json.loads(Response.text)
  return JSON['token']
