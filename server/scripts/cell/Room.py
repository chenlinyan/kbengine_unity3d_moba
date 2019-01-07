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

		# 把自己移动到一个不可能触碰陷阱的地方
		self.position = (999999.0, 0.0, 0.0)

		self.teamA  = {}
		self.teamB  = {}
		self._startBattleTime  = 0
		self._destroyTimer 	   = 0

		self.destroySpaceState = False

		self.gameStateC = GameConstants.GAMESTATE_READY_GAME

		self.herosCount  = {}
		self.selectHeroState   = False
		self.startBattleState  = False
		self.testFun()

	def testFun(self):
		self._testFunTimer = self.addTimer(60, 20, TIMER_TYPE_DESTROY)
		pass




	def onTimer(self, id, userArg):
		if TIMER_TYPE_DESTROY == userArg:
			self.delTimer(id)
			self.onDestroyTimer()

		if(TIMER_TYPE_READY == userArg):

			# 开始记录一局游戏时间， 时间结束后将玩家踢出空间同时销毁自己和空间
			#self._destroyTimer = self.addTimer(GameConfigs.GAME_ROUND_TIME, 0, TIMER_TYPE_DESTROY)
			#同开始在记录玩家加入游戏的最小时间值，到达该最小时间阈值不再加入
			#self.addTimer(GameConfigs.GAME_ROUND_TIME - GameConfigs.GAME_MIN_REMAIN_TIME, 0, TIMER_TYPE_MINTIME)

			# for avatar in self.teamA:
			# 		avatar.onPushReadyBattleState()
				# else:
				# 	DEBUG_MSG("Avatar[%i].client(Fun::room_cell_onTimer_TIMER_TYPE_READY) is None!" % (avatar.id))
			# for avatar in self.teamB:
			# 		avatar.onPushReadyBattleState()
				# else:
				# 	DEBUG_MSG("Avatar[%i].client(Fun::room_cell_onTimer_TIMER_TYPE_READY) is None!" % (avatar.id))

			#调用帧同步组件，开启幀同步
			self.componentFrameSync.start()
			self.startBattleState = True

			#删除定时器
			del(id)

			DEBUG_MSG("room_avatar_onReadyForBattle")

		pass

	def onDestroyTimer(self):
		# for avatar in self.redAvatars:
		# 	KBEngine.globalData["Halls"].deregisterHalls(avatar)
		# 	KBEngine.globalData["Halls"].leaveWaitStartGame(avatar)


		# for avatar in self.blueAvatars:
		# 	KBEngine.globalData["Halls"].deregisterHalls(avatar)
		# 	KBEngine.globalData["Halls"].leaveWaitStartGame(avatar)
		# KBEngine.globalData["Halls"].removeRoom(self.roomKeyC)
		self.teamA = {}
		self.teamB = {}
		self.destroySpace()

	def onDestory(self):
		#del KBEngine.globalData["Room_%i" % self.roomKeyC]
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

		if  self.gameStateC == GameConstants.GAMESTATE_READY_GAME:
			for avatar in self.teamA.values():
				avatar.client.onReadyBattle()
			for avatar in self.teamB.values():
				avatar.client.onReadyBattle()

			self.gameStateC == GameConstants.GAMESTATE_BEGIN
			self.addTimer(GameConfigs.GAME_READY_TIME, 0, TIMER_TYPE_READY)
		else:
			entityCall.client.onReadyBattle()

		pass

	def startBattle(self, entityCall):
		pass


	def ifEnterCombatMode(self, entityCall):
		pass

	def statisticalResult(self, winTeamId):
		'''
			玩家选择自己的英雄,并判断当前是否需要可以进入游戏
		'''
		#调用帧同步组件，结束幀同步
		self.componentFrameSync.stop()

		#看是否需要综合统计计算出赢的队伍

		#发送游戏结束状态
		for avatar in self.teamA:
			avatar.onPushStatisticalResult(winTeamId)
		for avatar in self.teamB:
			avatar.onPushStatisticalResult(winTeamId)

		self.addTimer(1, 0, TIMER_TYPE_DESTROY)

	def getGameState(self):
		return self.gameStateC

