
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import unittest
import os
import json

import TestsHelpers as helpers


################################################################################
################################################################################


class tests_APIWaresUpdate(unittest.TestCase):

  @classmethod
  def setUpClass(cls):

    cls.Token = helpers.askForToken("admin","admin")


  def setUp(self):
    pass


################################################################################
################################################################################


  def updateWare(self,Type,ID,Definition) :

    URL = "http://%s/api/wares/%s/%s" % (helpers.FluidhubAddr,Type,ID)
    Headers = {
     'content-type': "application/json",
     'authorization': "JWT %s" % self.Token,
     'cache-control': "no-cache",
    }

    Response = helpers.executePatchRequest(URL, Data=json.dumps(Definition), Headers=Headers)
    helpers.printResponse(Response)
    return Response


################################################################################


  def getWare(self,Type,ID) :

    URL = "http://%s/api/wares/%s/%s" % (helpers.FluidhubAddr,Type,ID)

    Response = helpers.executeGetRequest(URL)
    helpers.printResponse(Response)
    return Response


################################################################################
################################################################################


  def test01_UpdateWares(self):

    UpdateDef = {"shortdesc" : "new shortdesc"}
    Response = self.updateWare("builderexts","bext.01",UpdateDef)
    helpers.printResponse(Response)
    self.assertEqual(Response.status_code,200)

    UpdateDef = {"users-ro" : ["john","paul","ringo"]}
    Response = self.updateWare("builderexts","bext.01",UpdateDef)
    helpers.printResponse(Response)
    self.assertEqual(Response.status_code,200)

    UpdateDef = {"users-rw" : ["admin","george"]}
    Response = self.updateWare("builderexts","bext.01",UpdateDef)
    helpers.printResponse(Response)
    self.assertEqual(Response.status_code,200)

    UpdateDef = {"mailinglist" : ["george@sgtpepper.org","john@abbeyroad.org"]}
    Response = self.updateWare("builderexts","bext.01",UpdateDef)
    helpers.printResponse(Response)
    self.assertEqual(Response.status_code,200)

    UpdateDef = {
      "shortdesc" : "another new shortdesc",
      "users-ro" : ["admin","john","paul","ringo"],
      "users-rw" : ["george"],
      "mailinglist" : ["george@sgtpepper.org","john@abbeyroad.org"]
    }

    Response = self.updateWare("builderexts","bext.01",UpdateDef)
    helpers.printResponse(Response)
    self.assertEqual(Response.status_code,200)


################################################################################


  def test10_GetWares(self):

    Response = self.getWare("builderexts","bext.01")
    self.assertEqual(Response.status_code,200)


################################################################################
################################################################################


if __name__ == '__main__':
    unittest.main()
