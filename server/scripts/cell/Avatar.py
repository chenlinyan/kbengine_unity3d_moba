# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import GameUtils
import GameConfigs
import Data_avatar_initable
import GameConstants
TIMER_TYPE_ADD_TRAP = 1
from CSV_Helper import *

class Avatar(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)

		# 随机的初始化一个出生位置
		#self.position = GameUtils.randomPosition3D(self.modelRadius)

		self.roomBaseId = -1
		#玩家可通过全局数据找到相对应的房间,加载进入房间内
		self.getCurrRoom().enterRoom(self, self.teamId)
		DEBUG_MSG("teamId_teamId:::[%s]" % (self.teamId))

	def isAvatar(self):
		"""
		virtual method.
		"""
		return True
	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------

	def onDestroy(self):
		"""
		KBEngine method.
		entity销毁
		"""
		pass

	def relive(self, exposed, type):
		"""
		defined.
		复活
		"""
		if exposed != self.id:
			return

		DEBUG_MSG("Avatar::relive: %i, type=%i." % (self.id, type))

	def getCurrRoomBase(self):
		"""
		获得当前space的entity baseEntityCall,这是由Mather组件中创建房间提供的
		"""
		return KBEngine.globalData.get("Room_%i" % self.spaceID)

	def getCurrRoom(self):
		"""
		获得当前space的entity
		"""
		if self.roomBaseId == -1:
			roomBase = self.getCurrRoomBase()
			DEBUG_MSG("getCurrRoomBase_spaceID[%i][%s]" % (self.spaceID,str(roomBase)))
			self.roomBaseId = roomBase.id
			if roomBase is None:
				self.roomBaseId = -1
				return roomBase

		return KBEngine.entities.get(self.roomBaseId, None)

	def getHeroId(self):
		return self.heroId

	def setTeamId(self, teamId):
		self.teamId = teamId

	def getTeamId(self):
		DEBUG_MSG("getTeamIdgetTeamIdgetTeamId:::[%s][%s]" % (self.teamId, self))
		return self.teamId

	def submitStatisticalResult(self, winTeamId):
		#提交统计结果
		self.getCurrRoom().statisticalResult(winTeamId)

	def getGameState(self):
		self.gameStateC = self.getCurrRoom().getGameState()
		DEBUG_MSG("Avatar[%i] gameState changed::getGameState" % (self.id))

	def adjustFrameId(self, frameId):
		"""
			调整逻辑帧数
		"""
		# if self.componentFrameSync:
		# 	self.componentFrameSync.adjustFrameId(frameId)
		pass