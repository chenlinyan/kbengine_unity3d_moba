# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class MatchRoomReport(KBEngine.EntityComponent):
	def __init__(self):
		KBEngine.EntityComponent.__init__(self)
		# 为了方便访问，将base属性的roomEntityCall与当前的房间SpaceId联系保存起来######
		KBEngine.globalData["Room_%i" % self.owner.spaceID] = self.owner.base

		DEBUG_MSG("MatchRoomReport_init::set KBEngine.globalData[Room_%i]" % (self.owner.spaceID))

	def onAttached(self, owner):
		matchGlobalData = KBEngine.globalData["HallsMatcher"]
		self.componentObj = KBEngine.globalData["HallsMatcher"].getComponent("Matcher")
		self.componentObj.onRoomGetCell(self.owner, self.roomKeyC)

		DEBUG_MSG("MatchRoomReport_cell_onAttached::onRoomGetCell_componentObj[%s]" % (type(self.componentObj)))

	def onDetached(self, owner):
		del KBEngine.globalData["Room_%i" % self.owner.spaceID]
		self.componentObj.onRoomDestory(self.roomKeyC)


