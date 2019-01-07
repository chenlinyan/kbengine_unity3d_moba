# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

eventNamePushMatchDatas 		= "onPushMatchPlayersData"
eventNamePushMatchDataChanged	= "onPushPalyerMatchDataChanged"
eventNameMatchStateChanged		= "onMatchStateChanged"
eventNamePushExitMatchState		= "onPushExitMatchState"

class MatchAvatarReport(KBEngine.EntityComponent):

	def __init__(self):
		KBEngine.EntityComponent.__init__(self)

	def onAttached(self, owner):

		pass

	def onDetached(self, owner):
		pass

	def createCell(self, roomBaseEntityCall, roomCellEntityCall, matchId, roomKey):
		#playerData 玩家的属性，根据实际需求塞数值
		self.matchId = matchId
		self.roomKey = roomKey
		#self.roomCellEntity = roomCellEntityCall
		self.roomBaseEntity = roomBaseEntityCall
		self.owner.createCellEntity(roomCellEntityCall)
		DEBUG_MSG("createCell_createCell!!!")
		pass

	def pushMatchPlayersData(self, playersData):
		#推送参与匹配的玩家的匹配信息
		DEBUG_MSG("Avatar_base_matchComponent::pushMatchPlayersData_entityCall[%i], playersData.len[%i]" % (self.owner.id, len(playersData)))
		self.owner.fireEvent(eventNamePushMatchDatas, playersData)
		pass

	def pushPlayerMatchDataChanged(self, entityId, playerData):
		#推送玩家主动去改变自身匹配数据的信息
		DEBUG_MSG("Avatar_base_matchComponent::pushPlayerMatchDataChanged_entityCall[%i], playersData.len[%i]" % (self.owner.id, len(playerData)))
		self.owner.fireEvent(eventNamePushMatchDataChanged, entityId, playerData)
		pass

	def pushMatchState(self, matchState):
		DEBUG_MSG("Avatar_base_matchComponent::pushMatchState_entityCall[%i],state[%i]" % (self.owner.id, matchState))
		self.owner.fireEvent(eventNameMatchStateChanged, matchState)
		pass

	def pushExitMatchMsg(self, entityId):
		DEBUG_MSG("Avatar_base_matchComponent::pushExitMatchMsg_entityCall[%i]" % (self.owner.id))
		self.owner.fireEvent(eventNamePushExitMatchState, entityId)
		pass
