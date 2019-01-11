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

		# self.cellData["roomKeyC"] = self.componentBaseMatcherRoom.roomKey
		pass

	def onGetCell(self):
		#KBEngine.globalData["Halls"].onRoomGetCell(self, self.roomKey)
		pass

	def onLoseCell(self):
		self.destroy()
		DEBUG_MSG("Room_base_onLoseCell::Room_destroy")
		#KBEngine.globalData["Halls"].onRoomStateChanged(self.roomKey, GameConstants.GAMESTATE_END)

	def enterRoom(self, entityCall):
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

