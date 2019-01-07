# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import Functor

ID_MATCH_BEGIN = 0
ID_MATCHING    = 1
ID_MATCH_END   = 2
ID_LOADING_TIME   = 3
ID_ROOM_CREATION_BEGIN       = 4
ID_ROOM_CREATION_COMPLETE    = 5



class MatchRule:
	def check(self, matcher, existPlayersData, playerData):
		return True

class CreateRoomRule:
	def check(self, existPlayersData):
		return True

class Matcher(KBEngine.EntityComponent):
	def __init__(self):
		KBEngine.EntityComponent.__init__(self)
		self.matchId = 0
		self.minPlayers = -1
		self.maxPlayers = -1
		self.matchTime  = -1
		self.matchRules = []
		self.matchPools = {}

		self.roomName   = "Room"
		self.createRoomRules =[]
		self.loadTimeToOpenRoom = 3
		self.loadId = {}

	def onAttached(self, owner):
		KBEngine.globalData["HallsMatcher"] = {"owner":self.owner, "name":self.name}
		DEBUG_MSG("mather instances3333 %s" % (KBEngine.globalData["HallsMatcher"]["owner"]))
		pass

	def onDetached(self, owner):
		pass

	def addMatchRule(self, ruleObj:MatchRule):
		self.matchRules.append(ruleObj)

	def addCreateRoomRule(self, ruleObj:CreateRoomRule):
		self.createRoomRules.append(ruleObj)

	def joinMatch(self, entityCall, matchWayId, matchAvatarCmptName, playerData = {}):
		DEBUG_MSG("Matcher_joinMatch::avatar[%i] ,matchWayId[%i] " % (entityCall.id, matchWayId))
		reqsMatchId = -1
		if (self.maxPlayers > 0 and self.minPlayers > self.maxPlayers)  \
			or (self.maxPlayers == 0):
			return reqsMatchId
		# matchWayId <  0: 表示总要创建一个新的匹配对象
		# matchWayId == 0: 表示随机加入的匹配池的任意匹配对象
		# matchWayId > 0 : 表示加入指定的匹配对象
		if matchWayId < 0:
			reqsMatchId = self.createNewMatch(entityCall, playerData)
		elif matchWayId == 0:
			reqsMatchId = self.randomJoinMatch(entityCall, playerData)
		else:
			reqsMatchId = self.assignJoinMatch(matchWayId, playerData)

		if reqsMatchId < 0:
			return reqsMatchId

		#检查匹配条件是否满足
		matchData = self.matchPools[reqsMatchId]
		if not self.checkMatchCondition(matchData, playerData):
			return -1
		else:
			playerData["cmptName"] = matchAvatarCmptName
			matchData["playersData"][entityCall] = playerData

		#推送匹配信息
		self.pushMatchPlayersData(entityCall, matchAvatarCmptName, matchData)

		#检查条件是否达到可以加入房间
		if self.checkMatchDataToJoinRoom(matchData):
			self.enterRoom(reqsMatchId, matchAvatarCmptName, entityCall)

		return reqsMatchId

	def leaveMatch(self, entityCall, matchId):
		DEBUG_MSG("Matcher_leaveMatch::avatar_entityId[%i] ,matchObjId[%i] " % (entityCall.id, matchId))
		if not self.matchPools.__contains__(matchId):
			DEBUG_MSG("Matcher_leaveMatch::self.matchPools not exit matchObjId[%i] " % (matchId))
			return True

		matchData = self.matchPools[matchId]
		if matchData["loadFlag"] or matchData["hasRoom"]:
			return False
		else:
			if matchData["playersData"].keys().__contains__(entityCall):
				self.sendExitMatchMsg(matchData["playersData"], entityCall.id)
				del matchData["playersData"][entityCall]
			return True

	def createNewMatch(self, entityCall, playerData):

		#先遍历看又没有空出来的匹配池，减少资源消耗
		for matchData in self.matchPools.values():
			DEBUG_MSG("Matcher_createNewMatch::self.matchPools.values.len()[%i]" % len(self.matchPools))
			if len(matchData["playersData"]) == 0:
				return matchData["matchId"]

		#没有可用资源，便创建一个新的匹配对象

		baseMatchArg = {"matchId": self.matchId,
						"matchName:": "defineName",
						"matchState": ID_MATCHING,
						"arriveMaxUser" : False,
						"loadTimeToOpenRoom": self.loadTimeToOpenRoom,
						"loadFlag": False,
						"hasRoom" : False,
						"autoOpenRoom": True,
						"playersData":{}}
		self.matchPools[self.matchId] = baseMatchArg
		DEBUG_MSG("createNewMatch::self.matchId[%i][%i]" % (self.matchId, baseMatchArg["matchId"]))
		self.matchId = self.matchId + 1
		return baseMatchArg["matchId"]

	def randomJoinMatch(self, entityCall, playerData):
		for matchData in self.matchPools.values():
			if not self.ifArriveMaxPlayers(matchData):
				return matchData["matchId"]
			else:
				DEBUG_MSG("randomJoinMatch_arriveMaxNum:::[%s]" % (str(matchData)))
		DEBUG_MSG("Matcher_randomJoinMatch_len:::[%i]" % (len(self.matchPools)))
		return self.createNewMatch(entityCall, playerData)
		pass

	def assignJoinMatch(self, matchId, playerData):
		if self.matchPools.__contains__(matchId):
			return matchId
		else:
			return -1
		pass

	def checkMatchCondition(self, matchData, playerData):
		if self.checkBuildInCondition(matchData, playerData) and \
			self.checkMatchRules(matchData, playerData):
			return True
		return False

	def checkBuildInCondition(self, matchData, playerData):
		if (self.maxPlayers > 0 and self.minPlayers > self.maxPlayers)  \
			or(self.maxPlayers == 0):
			return False
		# if len(matchData["playersData"]) < self.minPlayers:
		# 	return False
		if self.maxPlayers > 0 and len(matchData["playersData"]) >= self.maxPlayers:
			return False
		else:
			return True

	def checkMatchRules(self, matchData, playerData):
		for matchRule in self.matchRules:
			if not matchRule.check(self, matchData["playersData"].values(), playerData):
				return False
		return True

	def checkCreateRoomRules(self, matchData):
		for rule in self.createRoomRules:
			if not rule.check(self, matchData["playersData"].values()):
				return False
		return True

	def checkMatchDataToJoinRoom(self, matchData):
		return self.ifArriveMinPlayers(matchData) and self.checkCreateRoomRules(matchData)

	def checkMatchDataToJoinRoomByMatchId(self, matchId):
		if self.matchPools.__contains__(matchId):
			return self.checkMatchDataToJoinRoom(self.matchPools[matchId])
		else:
			return False

	def ifArriveMaxPlayers(self, matchData):
		if self.maxPlayers < 0:
			return False
		if len(matchData["playersData"]) < self.maxPlayers:
			return False
		return True

	def ifArriveMinPlayers(self, matchData):
		if self.maxPlayers == 0:
			return False
		if self.minPlayers >= 0 and len(matchData["playersData"]) < self.minPlayers:
			return False
		return True

	def enterRoom(self, matchId, cmptName, entityCall):
		DEBUG_MSG("Matcher_enterRoomenterRoom================================ ")
		matchData = self.matchPools[matchId]
		if not matchData["hasRoom"]:
			if matchData["loadFlag"] == False:
				matchData["matchState"] = ID_MATCH_END
				matchData["loadFlag"]   = True
				if matchData["loadTimeToOpenRoom"] > 0:
					#倒计时加载时间处理
					timeId = self.addTimer(matchData["loadTimeToOpenRoom"], 0, matchId)
					self.loadId[timeId] = matchId

					matchData["matchState"] = ID_LOADING_TIME
				else:
					self.createRoom(matchId)
			DEBUG_MSG("Matcher_enterRoom[%s]" % str(matchData))
		elif matchData.__contains__("roomData"):
			roomDatas = matchData["roomData"]
			roomEntityCall = roomDatas["roomCellEntityCall"]
			if roomEntityCall :
				#加入房间中
				avatarCmptObj  = getattr(entityCall, cmptName)
				avatarCmptObj.createCell(roomDatas["roomBaseEntityCall"], roomEntityCall, matchId, roomDatas["roomKey"])
				DEBUG_MSG("Matcher_enterRoom_exitCellRoom[%i]" % (roomEntityCall.id))

		#通知各个玩家现在为等待创建和进入房间时段
		self.sendMatchStateChangedInfo(matchData["playersData"], matchData["matchState"])

	def createRoom(self, matchId):
		DEBUG_MSG("Matcher_createRoom_createRoom================================ ")
		matchData = self.matchPools[matchId]
		newRoomKey = KBEngine.genUUID64()
		params = {
			"roomKey" : newRoomKey,
			"matchId" : matchId,
		}
		KBEngine.createEntityAnywhere(self.roomName, params, Functor.Functor(self.onRoomCreatedCB, matchId, newRoomKey))
		matchData["arriveMaxUser"] = self.ifArriveMaxPlayers(self.matchPools[matchId])
		matchData["hasRoom"]  = True
		matchData["matchState"] = ID_ROOM_CREATION_BEGIN
		playersData = matchData["playersData"]
		self.sendMatchStateChangedInfo(playersData, matchData["matchState"])
		pass

	def onRoomCreatedCB(self, matchId, newRoomKey, roomEntityCall):
		DEBUG_MSG("Halls_component(Mather[%s], roomCellEntityCall[%s])::_onRoomCreatedCB::matchData!" % (self.name, roomEntityCall) )
		#加载room的base部分成功后
		if self.matchPools.__contains__(matchId):
			roomData  = {"roomBaseEntityCall":roomEntityCall, "roomCellEntityCall":None, "roomKey":newRoomKey}
			matchData = self.matchPools[matchId]
			matchData["roomData"] 	= roomData
			matchData["matchState"] = ID_MATCH_END

	def onRoomGetCell(self, roomCellEntityCall, matchId, spaceID):
		if not self.matchPools.__contains__(matchId):
			DEBUG_MSG("Matcher_component(Mather[%s])::_onRoomGetCell no matchData!"%(self.name))
			return
		DEBUG_MSG("Matcher_component(Mather[%s], roomCellEntityCall[%s])::_onRoomGetCell::matchData!"%(self.name, roomCellEntityCall) )
		matchData  = self.matchPools[matchId]
		matchData["matchState"] = ID_ROOM_CREATION_COMPLETE
		roomDatas   = matchData["roomData"]
		playersData = matchData["playersData"]

		roomBaseEntityCall = roomDatas["roomBaseEntityCall"]

		######为了方便访问，将base属性的roomEntityCall与当前的房间SpaceId联系保存起来######
		KBEngine.globalData["Room_%i" % spaceID] = roomBaseEntityCall

		#加载room的cell部分成功后
		roomDatas["roomCellEntityCall"] = roomCellEntityCall

		for entityCall in playersData.keys():
			DEBUG_MSG("Matcher_onRoomGerCell::self.enterGameAvatars.count(%i)" %(len(playersData)))
			DEBUG_MSG("Matcher_onRoomGerCell::entity[%s][%s]" % (type(entityCall), playersData[entityCall]["cmptName"]))
			cmptName = playersData[entityCall]["cmptName"]
			avatarCmptObj = getattr(entityCall, cmptName)
			avatarCmptObj.createCell(roomBaseEntityCall, roomCellEntityCall, matchId, roomDatas["roomKey"])
			# fun = "createCell"
			# getattr(entityCall, fun)(roomEntityCall, matchId, roomDatas["roomKey"])

	def playerEnterRoom(self, entityCall, cmptName, roomEntityCall):
		DEBUG_MSG("Matcher_onRoomGerCell::entity[%s][%s]" % (type(entityCall), playersData[entityCall]["cmptName"]))
		cmptName = playerData["cmptName"]
		avatarCmptObj = getattr(entityCall, cmptName)
		avatarCmptObj.createCell(roomEntityCall, roomCellEntityCall, matchId, roomDatas["roomKey"])
		pass

	def onRoomDestory(self, matchId, spaceID):
		if not self.matchPools.__contains__(matchId):
			return True
		del self.matchPools[matchId]
		del KBEngine.globalData["Room_%i" % spaceID]
		DEBUG_MSG("Matcher_onRoomDestory::destory_matchId[%i], pools.len[%i]." % (matchId, len(self.matchPools)))
		return True

	def pushMatchPlayersData(self, entityCall, cmptName, matchData):

		DEBUG_MSG("Mather_pushMatchPlayersData::entityCall_Id[%i]" % (entityCall.id))
		playersData = matchData["playersData"]
		playerEntityCalls = playersData.keys()

		#推送消息
		for playerEntity in playerEntityCalls:
			if playerEntity.id != entityCall.id:
				avatarCmptObj  = getattr(playerEntity, cmptName)
				avatarCmptObj.pushMatchPlayersData({entityCall:playersData[entityCall]})

		avatarCmptObj  = getattr(entityCall, cmptName)
		avatarCmptObj.pushMatchPlayersData(playersData)

	def acquireAllPlayersMatchData(self, matchId):
		if self.matchPools.__contains__(matchId):
			return self.matchPools[matchId]["playersData"]
		else:
			return {}

	def acquireOnePlayerMatchData(self, matchId, entityCall):
		'''
			获取matchPool中的指定匹配对象中的指定玩家数据
		'''
		if self.matchPools.__contains__(matchId):
			return self.matchPools[matchId]["playersData"][entityCall]
		else:
			return {}

	def changePlayerMatchData(self, matchId, entityCall, playerData, allReplace = False):
		if self.matchPools.__contains__(matchId):
			playersData = self.matchPools[matchId]["playersData"]
			if playersData.__contains__(entityCall):
				srcPlayerData = playersData[entityCall]
				if allReplace == False:
					for keyValue in playerData.keys():
						srcPlayerData[keyValue] = playerData[keyValue]
				else:
					if not playerData.__contains__("cmptName"):
						playerData["cmptName"] = srcPlayerData["cmptName"]
					playersData[entityCall] = playerData
			else:
				return False
		else:
			return False
		return True

	def matchDataChanged(self, matchId, entityCall, playerData, allReplace = False):
		if not self.changePlayerMatchData(matchId, entityCall, playerData, allReplace):
			return False

		#当修改成功后，需要重新判断匹配
		matchData = self.matchPools[matchId]
		playersData =  matchData["playersData"]

		#遍历当前在匹配池中的所有玩家对象，推动玩家改变的匹配信息
		DEBUG_MSG("matchDataChanged_num:::[%i]" % (len(playersData.keys())))
		for playerEntity in playersData.keys():
			avatarCmptObj  = getattr(playerEntity, playersData[playerEntity]["cmptName"])
			avatarCmptObj.pushPlayerMatchDataChanged(entityCall.id, playerData)
			pass

		#查看是否满足创建房间或者加入房间的条件
		# if not matchData["hasRoom"] and self.checkMatchDataToJoinRoomByMatchId(matchId):
		if self.checkMatchDataToJoinRoomByMatchId(matchId):
			self.enterRoom(matchId, matchData["playersData"][entityCall]["cmptName"], entityCall)
		return True

	def sendMatchStateChangedInfo(self, playersData, matchState):
		for entityCall in playersData.keys():
			DEBUG_MSG("Matcher_sendMatchStateChangedInfo::self.enterGameAvatars.count(%i)" %(len(playersData)))
			DEBUG_MSG("Matcher_onRoomGerCell::entity[%s][%s]" % (type(entityCall), playersData[entityCall]["cmptName"]))
			cmptName = playersData[entityCall]["cmptName"]
			avatarCmptObj = getattr(entityCall, cmptName)
			avatarCmptObj.pushMatchState(matchState)

	def sendExitMatchMsg(self, playersData, entityId):
		DEBUG_MSG("Matcher_sendExitMatchMsg::self.enterGameAvatars.count(%i),exitEntitiyId[%i]" % (len(playersData), entityId))
		for entityCall in playersData.keys():
			cmptName = playersData[entityCall]["cmptName"]
			avatarCmptObj = getattr(entityCall, cmptName)
			avatarCmptObj.pushExitMatchMsg(entityId)
		pass

	def onTimer(self, id, userArg):
		if self.loadId.__contains__(id):
			self.createRoom(self.loadId[id])
			self.loadId.pop(id)
			self.delTimer(id)
