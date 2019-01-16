# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import GameConfigs
import random
import GameUtils
import GameConstants
from CSV_Helper import *

TIMER_TYPE_DESTROY = 1
TIMER_TYPE_READY = 2
TIMER_TYPE_START = 3
TIMER_TYPE_MINTIME = 4

TIMER_TYPE_ROOM_TICK = 5 #房间帧同步的计算


class Room(KBEngine.Space):
	"""
	游戏场景
	"""
	def __init__(self):
		KBEngine.Entity.__init__(self)

		self.teamA = {}
		self.teamB = {}

		self.gameStateC = GameConstants.GAMESTATE_READY_GAME
		self.startBattleState = False
		#self.testFun()

	def testFun(self):
		self._testFunTimer = self.addTimer(120, 20, TIMER_TYPE_DESTROY)

	def onTimer(self, id, userArg):
		if TIMER_TYPE_DESTROY == userArg:
			self.componentFrameSync.stop()
			self.delTimer(id)
			self.onDestroyTimer()

		if TIMER_TYPE_READY == userArg:
			# 调用帧同步组件，开启幀同步
			self.componentFrameSync.start()
			self.startBattleState = True

			# 删除定时器
			self.delTimer(id)
			DEBUG_MSG("room_avatar_onReadyForBattle")

	def onDestroyTimer(self):
		self.teamA = {}
		self.teamB = {}
		self.destroySpace()

	def onDestory(self):
		pass

	def enterRoom(self, entityCall, teamId):
		"""
		玩家进入房间
		"""
		DEBUG_MSG("RoomCellCell_enterRoom::_entityCall[%i]" %(entityCall.id))
		if teamId == GameConfigs.TEAM_A_ID:
			self.teamA[entityCall.id] = entityCall
		else:
			self.teamB[entityCall.id] = entityCall

		if len(self.teamA) <= 0 or len(self.teamB) <= 0 :
			return

		if self.gameStateC == GameConstants.GAMESTATE_READY_GAME:
			self.gameStateC == GameConstants.GAMESTATE_PLAYING
			for avatar in self.teamA.values():
				avatar.client.onReadyBattle()

			for avatar in self.teamB.values():
				avatar.client.onReadyBattle()

			self.addTimer(GameConfigs.GAME_READY_TIME, 0, TIMER_TYPE_READY)
		else:
			entityCall.client.onReadyBattle()

	def startBattle(self, entityCall):
		pass


	def ifEnterCombatMode(self, entityCall):
		pass

	def statisticalResult(self, winTeamId):
		'''
		玩家选择自己的英雄,并判断当前是否需要可以进入游戏
		'''
		#統計结果
		self.gameStateC = GameConstants.GAMESTATE_STATISTICAL

		# 调用帧同步组件，结束幀同步
		self.componentFrameSync.stop()

		# 看是否需要综合统计计算出赢的队伍

		# 发送游戏结束状态
		for avatar in self.teamA:
			avatar.onPushStatisticalResult(winTeamId)

		for avatar in self.teamB:
			avatar.onPushStatisticalResult(winTeamId)

		self.addTimer(1, 0, TIMER_TYPE_DESTROY)

	def getGameState(self):
		return self.gameStateC

