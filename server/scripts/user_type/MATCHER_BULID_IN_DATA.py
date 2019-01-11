# -*- coding: utf-8 -*-
import KBEngine
import GlobalConst
from KBEDebug import *

class TMatherBulidInData(dict):
	"""
	"""
	def __init__(self):
		"""
		"""
		dict.__init__(self)
		# self["MinPlayers"] = 0
		# self["MaxPlayers"] = 0
		# self["MatchTime"]  = 0

	def asDict(self):
		for key, val in self.items():
			return {"minPlayers" : val[0], "maxPlayers" : val[1], "matchTime" :val[2]}

	# def createFromDict(self, dictData):
	# 	self[dictData["minPlayers"]] = [dictData["maxPlayers"], dictData["matchTime"]]
	# 	return self

class MATCHER_BULID_IN_DATA_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TMatherBulidInData().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TMatherBulidInData)

matcher_bulid_In_dict = MATCHER_BULID_IN_DATA_PICKLER()