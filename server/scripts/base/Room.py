# -*- coding: utf-8 -*-
import KBEngine
import random
import copy
import math
from KBEDebug import *
import GameConfigs
import GameConstants

TIMER_TYPE_STATISTICAL = 1
class Room(KBEngine.Space):
	"""
	一个可操控cellapp上真正space的实体
	注意：它是一个实体，并不是真正的space，真正的space存在于cellapp的内存中，通过这个实体与之关联并操控space。
	"""
	def __init__(self):
		KBEngine.Entity.__init__(self)

		self.cellData["roomKeyC"] = self.roomKey
		self.avatars = {}
		pass


	def onGetCell(self):
		#KBEngine.globalData["Halls"].onRoomGetCell(self, self.roomKey)
		pass

	def onLoseCell(self):
		#KBEngine.globalData["Halls"].onRoomStateChanged(self.roomKey, GameConstants.GAMESTATE_END)
		pass

	def enterRoom(self, entityCall):
		self.avatars[entityCall.id] = entityCall
		DEBUG_MSG("RoomBaseBase_enterRoom::_entityCall[%i]" %(entityCall.id))
		# entityCall.createCell(self.cell, self.roomKey, teamId)
		# self.cell.enterRoom(entityCall, teamId)
		# self.avatars[entityCall.id] = entityCall
		# print("enterRoom_enterRoom")
		pass

	def leaveRoom(self, entityId, teamId):
		pass

	def onDestory(self):
		DEBUG_MSG("Room_%i is Destroy!" % self.roomKey)
		pass

	def onTimer(self, id, userArg):
		pass

	#统计结果
	def statisticalResult(self, entityId, teamId, value):
		pass

	def anayizeResults(self):
		pass

	def transmitResults(self, teamId, endValue):
			#向客戶端传输结算数据
		pass

