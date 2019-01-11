# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

eventNameEnterRoom				= "onEnterRoom"
eventNameLeaveRoom				= "onLeaveRoom"

class MatchBaseRoomReport(KBEngine.EntityComponent):
	def __init__(self):
		KBEngine.EntityComponent.__init__(self)
		DEBUG_MSG("roomKey_init:::[%i]" % self.roomKey)
		self.players = {}

	def onAttached(self, owner):
		DEBUG_MSG("roomKey_onAttached:::[%i]" % self.roomKey)

	def onDetached(self, owner):
		self.players.clear()

	def onEnterRoom(self, playersData):
		DEBUG_MSG("MatchBaseRoomReport_onEnterRoom[%s]" % str(playersData))
		for playersEntityId in playersData.keys():
			self.players[playersEntityId] = playersData[playersEntityId]
			DEBUG_MSG("MatchBaseRoomReport_onEnterRoo[%s]" % str(self.players[playersEntityId]))
		self.owner.fireEvent(eventNameEnterRoom, playersData)

	def onLeaveRoom(self, entityId):
		if entityId in self.players:
			del self.players[entityId]
			self.owner.fireEvent(eventNameLeaveRoom, entityCall)
