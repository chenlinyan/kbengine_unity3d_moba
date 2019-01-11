# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from MATCHING_INFOS import *

class TMatchingInfos(list):
	"""
	"""
	def __init__(self):
		"""
		"""
		list.__init__(self)

	def asDict(self):
		data = {
			"id"			: self[0],
			"name"			: self[1],
			"teamId"		: self[2],
            "heroId"        : self[3],
            "heroIdLst"     : self[4]
		}

		return data

	def createFromDict(self, dictData):
		self.extend([dictData["id"], dictData["name"], dictData["teamId"], dictData["heroId"], \
			dictData["heroIdLst"]])
		return self

class MATCHING_INFOS_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TMatchingInfos().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TMatchingInfos)

matching_info_inst = MATCHING_INFOS_PICKLER()

class TMatchingInfosList(dict):
	"""
	"""
	def __init__(self):
		"""
		"""
		dict.__init__(self)

	def asDict(self):
		datas = []
		dct = {"values" : datas}

		for key, val in self.items():
			datas.append(val)

		return dct

	def createFromDict(self, dictData):
		for data in dictData["values"]:
			self[data[0]] = data
		return self

class MATCHING_INFOS_LIST_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TMatchingInfosList().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TMatchingInfosList)

matching_info_list_inst = MATCHING_INFOS_LIST_PICKLER()
