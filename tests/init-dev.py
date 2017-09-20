#!/usr/bin/env python


__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import sys
import os
import shutil

import TestsHelpers as helpers


################################################################################
################################################################################


print "Data directory for development:", helpers.DataServerPath

# Check if data directory does not exist
if os.path.exists(helpers.DataServerPath) :
  print "!!!",helpers.DataServerPath,"already exists. aborting."
else :
  # Install common data
  shutil.copytree(os.path.join(helpers.TestsPath,"server","data"),helpers.DataServerPath)
  with open(os.path.join(helpers.DataServerPath,"common","access-token"), "w") as TokenFile:
    TokenFile.write("%s\n" % helpers.AccessToken)
