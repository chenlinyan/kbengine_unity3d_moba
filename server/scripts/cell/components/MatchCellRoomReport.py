# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class MatchCellRoomReport(KBEngine.EntityComponent):
	def __init__(self):
		KBEngine.EntityComponent.__init__(self)

	def onAttached(self, owner):
		matchGlobalData  =  KBEngine.globalData["HallsMatcher"]
		# matchGlobalName  =  matchGlobalData["name"]
		# matchGlobalOwner =  matchGlobalData["owner"]

		# DEBUG_MSG("MatchCellRoomReport_onAttached::[%s] [%s] [%i]" % (matchGlobalName, self.owner, self.roomKeyC))
		self.componentObj = KBEngine.globalData["HallsMatcher"].getComponent("Matcher")
		# self.componentObj = getattr(matchGlobalOwner, matchGlobalName)
		DEBUG_MSG(" MatchCellRoomReport_onRoomGetCell::[%s]" % (type(self.componentObj)))
		self.componentObj.onRoomGetCell(self.owner, self.roomKeyC, self.owner.spaceID)

	def onDetached(self, owner):
		self.componentObj.onRoomDestory(self.roomKeyC, self.owner.spaceID)

