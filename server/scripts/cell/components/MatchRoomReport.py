# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class MatchRoomReport(KBEngine.EntityComponent):
	def __init__(self):
		KBEngine.EntityComponent.__init__(self)

	def onAttached(self, owner):
		matchGlobalData = KBEngine.globalData["HallsMatcher"]
		self.componentObj = KBEngine.globalData["HallsMatcher"].getComponent("Matcher")

		self.componentObj.onRoomGetCell(self.owner, self.roomKeyC, self.owner.spaceID)

		DEBUG_MSG("MatchRoomReport_cell_onAttached::onRoomGetCell_componentObj[%s]" % (type(self.componentObj)))

	def onDetached(self, owner):
		self.componentObj.onRoomDestory(self.roomKeyC, self.owner.spaceID)

