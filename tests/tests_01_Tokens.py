
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import unittest
import time

from fluidhubcommon.TokenManager import TokenManager

import TestsHelpers as helpers


################################################################################
################################################################################


class tests_Tokens(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    pass


  def setUp(self):
    pass


################################################################################
################################################################################


  def test_runGenerateDecode(self):

    ## simple sub

    Token = TokenManager.generate("user1",60)
    print Token
    self.assertIsNotNone(Token)

    Sub = TokenManager.decode(Token)
    print Sub
    self.assertIsNotNone(Sub)


    ## compound sub

    Token = TokenManager.generate({ "username" : "user1", "isadmin" : False },60)
    print Token
    self.assertIsNotNone(Token)

    Sub = TokenManager.decode(Token)
    print Sub
    self.assertIsNotNone(Sub)


    ## out of delay token

    Token = TokenManager.generate("user1",1)
    print Token
    self.assertIsNotNone(Token)

    time.sleep(2)

    Sub = TokenManager.decode(Token)
    print Sub
    self.assertIsNone(Sub)


################################################################################
################################################################################


if __name__ == '__main__':
    unittest.main()
