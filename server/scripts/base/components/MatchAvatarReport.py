# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

eventNameJoinMatch				= "onJoinMatch"
eventNameExitMatch				= "onExitMatch"
eventNameMatchDataChanged		= "onMatchDataChanged"
eventNameMatchStateChanged		= "onMatchStateChanged"

class MatchAvatarReport(KBEngine.EntityComponent):

	def __init__(self):
		KBEngine.EntityComponent.__init__(self)

	def onAttached(self, owner):
		pass

	def onDetached(self, owner):
		pass

	def createCell(self, roomBaseEntityCall, roomCellEntityCall, matchId, roomKey):
		# playerData 玩家的属性，根据实际需求塞数值
		self.matchId = matchId
		self.roomKey = roomKey
		self.roomBaseEntity = roomBaseEntityCall
		self.owner.createCellEntity(roomCellEntityCall)

		DEBUG_MSG("createCell_createCell!!!")

	def onJoinMatch(self, playersData, state):
		'''
		推送参与匹配的玩家的匹配信息
		'''
		DEBUG_MSG("Avatar_base_matchComponent::onJoinMatch_entityCall[%i], playersData.len[%i]" % (self.owner.id, len(playersData)))

		self.owner.fireEvent(eventNameJoinMatch, playersData, state)

	def onMatchDataChanged(self, entityId, playerData):
		'''
		推送玩家主动去改变自身匹配数据的信息
		'''
		DEBUG_MSG("Avatar_base_matchComponent::onMatchDataChanged_entityCall[%i], playersData.len[%i]" % (self.owner.id, len(playerData)))

		self.owner.fireEvent(eventNameMatchDataChanged, entityId, playerData)

	def onMatchStateChaned(self, matchState):
		'''
		推送匹配状态信息
		'''
		DEBUG_MSG("Avatar_base_matchComponent::pushMatchState_entityCall[%i],state[%i]" % (self.owner.id, matchState))

		self.owner.fireEvent(eventNameMatchStateChanged, matchState)

	def onExitMatch(self, entityId):
		'''
		推送玩家离开匹配的信息
		'''
		DEBUG_MSG("Avatar_base_matchComponent::onExitMatch_entityCall[%i]" % (self.owner.id))

		self.owner.fireEvent(eventNameExitMatch, entityId)
