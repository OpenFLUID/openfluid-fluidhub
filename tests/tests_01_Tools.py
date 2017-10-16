
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import unittest
import time

from FluidHub import Tools

import TestsHelpers as helpers


################################################################################
################################################################################


class tests_Tools(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    pass


  def setUp(self):
    pass


################################################################################
################################################################################


  def test01_isValidUsers(self):

    self.assertTrue(Tools.isValidUsername("george"))
    self.assertTrue(Tools.isValidUsername("john81"))
    self.assertTrue(Tools.isValidUsername("ringo"))

    self.assertFalse(Tools.isValidUsername("john_81"))
    self.assertFalse(Tools.isValidUsername("john 81"))
    self.assertFalse(Tools.isValidUsername("Ringo"))
    self.assertFalse(Tools.isValidUsername("0ringo"))


################################################################################


  def test02_isValidEmails(self):

    self.assertTrue(Tools.isValidEmail("george@sgtpepper.org"))
    self.assertTrue(Tools.isValidEmail("george.harrison@sgtpepper.org"))
    self.assertTrue(Tools.isValidEmail("george.harrison@sgt-pepper.org"))
    self.assertTrue(Tools.isValidEmail("george-ringo-paul-john@fabfour.org"))
    self.assertTrue(Tools.isValidEmail("GeorgeHarrison@sgt-pepper.org"))

    self.assertFalse(Tools.isValidEmail("georgeatsgt-pepper.org"))
    self.assertFalse(Tools.isValidEmail("george at sgt-pepper.org"))
    self.assertFalse(Tools.isValidEmail("george@ sgt-pepper.org"))
    self.assertFalse(Tools.isValidEmail("george @sgt-pepper.org"))


################################################################################


  def test10_isValidUsernameList(self):

    ValidLists = {
      "george,ringo,john,paul" : ["george","ringo","john","paul"],
      "*,ringo,john,paul" : ["*","ringo","john","paul"],
      "*" : ["*"],
      "" : [],
      "george,ringo,,,,john,paul" : ["george","ringo","john","paul"],
      "george,ringo,  ,john,paul" : ["george","ringo","john","paul"],
      " , ,  ,    ,paul" : ["paul"],
      " , ,  ,    ," : []
    }

    InvalidLists = [
      "geo rge,ringo,john,paul",
      "george,ringo,john,9paul"
    ]


    for Key,Value in ValidLists.iteritems():
      self.assertEqual(Tools.getAsValidList(Key,Tools.isValidUsername,True,","),Value)

    for Item in InvalidLists:
      self.assertIsNone(Tools.getAsValidList(Item,Tools.isValidUsername,True))



################################################################################


  def test11_isValidEmailList(self):

    ValidLists = {
      "george@sgtpepper.org,ringo@abbeyroad.org" : ["george@sgtpepper.org","ringo@abbeyroad.org"],
      "george@sgt-pepper.org,ringo@abbeyroad.org" : ["george@sgt-pepper.org","ringo@abbeyroad.org"],
      " , ,  ,    ,paul@fabfour.org" : ["paul@fabfour.org"],
      " , ,  ,    ," : [],
      "" : []
    }

    InvalidLists = [
      "paul@fabfour.org,john",
      "paul@ fabfour.org",
      "paulatfabfour.org",
      "paul@fabfour.org,*"
    ]


    for Key,Value in ValidLists.iteritems():
      self.assertEqual(Tools.getAsValidList(Key,Tools.isValidEmail,False,","),Value)

    for Item in InvalidLists:
      self.assertIsNone(Tools.getAsValidList(Item,Tools.isValidEmail,False))


################################################################################
################################################################################


if __name__ == '__main__':
    unittest.main()
