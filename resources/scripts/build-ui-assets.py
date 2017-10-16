#!/usr/bin/env python


__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os

import __common__


################################################################################
################################################################################


SrcPath = os.path.join(__common__.RootPath,"fluidhub","app","ui","assets")
DestPath = os.path.join(__common__.RootPath,"fluidhub","app","ui","static")


CSSAssets = {
              os.path.join("css","fluidhub.scss") : os.path.join("css","fluidhub.css")
            }

for Key,Value in CSSAssets.iteritems():
  print Key,"=>",Value
  Cmd = "sass --scss %s %s " % (os.path.join(SrcPath,Key),os.path.join(DestPath,Value))
  os.system(Cmd)
