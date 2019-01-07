# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class MatchRoomReport(KBEngine.EntityComponent):
	def __init__(self):
		KBEngine.EntityComponent.__init__(self)

	def onAttached(self, owner):
		matchGlobalData  =  KBEngine.globalData["HallsMatcher"]
		matchGlobalName  =  matchGlobalData["name"]
		matchGlobalOwner =  matchGlobalData["owner"]

		DEBUG_MSG(" MatchRoomReport_MatchRoomReport::[%s] [%s] [%i]" % (matchGlobalName, self.owner, self.owner.matchId ))
		self.componentObj = getattr(matchGlobalOwner, matchGlobalName)
		DEBUG_MSG(" MatchRoomReport_MatchRoomReport_end::[%s] [%s]" % (matchGlobalName, type(self.componentObj)))
		self.componentObj.onRoomGetCell(self.owner, self.owner.matchId, self.owner.spaceID)

	def onDetached(self, owner):
		self.componentObj.onRoomDestory(self.owner.matchId, self.owner.spaceID)
		pass


