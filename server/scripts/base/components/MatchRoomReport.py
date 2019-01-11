# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

eventNameEnterRoom				= "onEnterRoom"
eventNameLeaveRoom				= "onLeaveRoom"

class MatchRoomReport(KBEngine.EntityComponent):
	def __init__(self):
		KBEngine.EntityComponent.__init__(self)
		self.players = {}

	def onAttached(self, owner):
		DEBUG_MSG("MatchRoomReport_base_onAttached::roomKey[%i]" % self.roomKey)

	def onDetached(self, owner):
		self.players.clear()

	def onEnterRoom(self, playersData):
		'''
		玩家进入房间
		'''
		DEBUG_MSG("MatchRoomReport_base_onEnterRoom::playersData[%s]" % str(playersData))

		self.players.update(playersData)
		self.owner.fireEvent(eventNameEnterRoom, playersData)

	def onLeaveRoom(self, entityId):
		'''
		玩家离开房间
		'''
		if entityId in self.players:
			del self.players[entityId]
			self.owner.fireEvent(eventNameLeaveRoom, entityCall)
