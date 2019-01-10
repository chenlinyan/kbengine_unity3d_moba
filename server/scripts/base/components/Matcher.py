# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import Functor

ID_MATCH_BEGIN = 0
ID_MATCHING    = 1
ID_MATCH_CREROOMRULE   = 2
ID_MATCH_END   = 3

ID_LOADING_TIME   = 4
ID_ROOM_CREATION_BEGIN       = 5
ID_ROOM_CREATION_COMPLETE    = 6

#常量标识
INVALIDID_MATCHID = -1

class MatchRule:
	"""
		这里提供了创建匹配规则的基类,供使用者在外部自定义开启房间规则
	"""
	def check(self, matcher, existPlayersData, playerData):
		return True

class CreateRoomRule:
	"""
		这里提供了创建房间规则的基类,供使用者在外部自定义开启房间规则
	"""
	def check(self, existPlayersData):
		return True

class Matcher(KBEngine.EntityComponent):
	def __init__(self):
		KBEngine.EntityComponent.__init__(self)
		'''
			self.minPlayers, self.maxPlayers 为-1，表示对最大最小人数没有限制；
			如果设置了最小人数, self.maxPlayers 要么为-1(表示没有最大人数限制)，要么大于等于最小人数设置的数值；
			且最大人数不能为0;
		'''
		self.matchId    = 1
		self.minPlayers = -1
		self.maxPlayers = -1
		self.matchTime  = -1
		self.matchRules = []
		self.matchPools = {}

		#存储未满人数的matchId
		self.matchIds   = []

		self.roomName = "Room"
		self.createRoomRules = []
		self.befCreRoomLoadTime = 3
		self.loadId = {}

	def onAttached(self, owner):
		KBEngine.globalData["HallsMatcher"] = {"owner":self.owner, "name":self.name}
		DEBUG_MSG("mather instances:: %s" % (KBEngine.globalData["HallsMatcher"]["owner"]))
		pass

	def onDetached(self, owner):
		pass

	def addMatchRule(self, ruleObj:MatchRule):
		self.matchRules.append(ruleObj)

	def addCreateRoomRule(self, ruleObj:CreateRoomRule):
		self.createRoomRules.append(ruleObj)

	def joinMatch(self, entityCall, matchId, playerData = {}):
		"""
			加入匹配
		"""
		DEBUG_MSG("Matcher_joinMatch::avatar[%i], matchId[%i] " % (entityCall.id, matchId))

		reqsMatchId = INVALIDID_MATCHID
		if self.maxPlayers == 0:
			return reqsMatchId
		elif self.maxPlayers > 0 and self.minPlayers > self.maxPlayers:
			return reqsMatchId

		# matchId <  0: 表示总要创建一个新的匹配对象
		# matchId == 0: 表示随机加入的匹配池的任意匹配对象
		# matchId > 0 : 表示加入指定的匹配对象
		if matchId < 0:
			reqsMatchId = self.createNewMatch(playerData)
		elif matchId == 0:
			reqsMatchId = self.randomJoinMatch(playerData)
		else:
			reqsMatchId = self.assignJoinMatch(matchId, playerData)

		if reqsMatchId < 0:
			return reqsMatchId

		DEBUG_MSG("Matcher_joinMatch::avatar[%i], matchId[%i], reqsMatchId[%i] " % (entityCall.id, matchId, reqsMatchId))
		#检查匹配条件是否满足
		matchData = self.matchPools[reqsMatchId]
		if not self.checkMatchCondition(matchData, playerData):
			DEBUG_MSG("entity[%i] check failed of matchConditions!" % (entityCall.id))
			return INVALIDID_MATCHID
		else:
			#获取entity对应的相应组件MatchAvatarReport
			cmptObj = KBEngine.entities[entityCall.id].getComponent("MatchAvatarReport")
			if not cmptObj:
				DEBUG_MSG("entityCall[%i] no exit MatchAvatarReport component!" % (entityCall.id))
				return INVALIDID_MATCHID
			playerData["cmptObj"] = cmptObj

			playerData["entityCall"] = playerData.get("entityCall", entityCall)
			matchData["playersData"][entityCall.id] = playerData

			#再次判断匹配池中是否到达最大人数,到达人数则移除
			if self.ifArriveMaxPlayers(matchData):
				if reqsMatchId in self.matchIds:
					self.matchIds.remove(reqsMatchId)

		#推送匹配信息
		self.broadcastPlayerJoin(entityCall.id, cmptObj, matchData)

		#检查条件是否达到可以加入房间
		if self.checkMatchDataToJoinRoom(matchData):
			self.enterRoom(reqsMatchId, cmptObj, entityCall)

		return reqsMatchId

	def exitMatch(self, entityId, matchId):
		"""
			退出匹配
		"""
		DEBUG_MSG("Matcher_exitMatch::avatar_entityId[%i] ,matchObjId[%i] " % (entityId, matchId))
		if not matchId in self.matchPools:
			DEBUG_MSG("Matcher_leaveMatch::self.matchPools not exit matchObjId[%i] " % (matchId))
			return True

		matchData = self.matchPools[matchId]
		if matchData["state"] > ID_MATCH_END:
			return False
		else:
			if entityId in matchData["playersData"].keys():
				self.broadcastExitMatch(matchData["playersData"], entityId)
				del matchData["playersData"][entityId]

				#如果当下没有玩家数据,则释放匹配池中对象的匹配对象
				if len(matchData["playersData"]) == 0:
					del self.matchPools[matchId]

				if matchId in self.matchIds:
					self.matchIds.remove(matchId)

			return True

	def createNewMatch(self, playerData):
		#没有可用资源，便创建一个新的匹配对象
		#loadTimeOfBefCreRoom:表示创建房间前的等待加载时间
		baseMatchArg = {"matchId": self.matchId,
						"matchName:": "defineName",
						"state": ID_MATCHING,
						"arriveMaxUser" : False,
						"loadTimeOfBefCreRoom": self.befCreRoomLoadTime,
						"autoOpenRoom": True,
						"playersData":{}}
		self.matchPools[self.matchId] = baseMatchArg
		self.matchIds.append(self.matchId)
		DEBUG_MSG("createNewMatch::self.matchId[%i][%i]" % (self.matchId, baseMatchArg["matchId"]))
		self.matchId = self.matchId + 1
		return baseMatchArg["matchId"]

	def randomJoinMatch(self, playerData):
		if self.matchIds:
			DEBUG_MSG("Matcher_randomJoinMatch_join_matchId[%i]" % (self.matchIds[0]))
			return self.matchIds[0]

		DEBUG_MSG("Matcher_randomJoinMatch_createNewMatch_len:::[%i]" % (len(self.matchPools)))
		return self.createNewMatch(playerData)

	def assignJoinMatch(self, matchId, playerData):
		return self.matchPools.get(matchId, INVALIDID_MATCHID)

	def checkMatchCondition(self, matchData, playerData):
		if self.checkBuildInCondition(matchData, playerData) and \
			self.checkMatchRules(matchData, playerData):
			return True
		return False

	def checkBuildInCondition(self, matchData, playerData):
		if self.maxPlayers < 0:
			return True
		elif self.maxPlayers == 0:
			return False
		elif self.minPlayers > self.maxPlayers or len(matchData["playersData"]) >= self.maxPlayers:
			return False
		return True

	def checkMatchRules(self, matchData, playerData):
		for matchRule in self.matchRules:
			if not matchRule.check(self, matchData["playersData"].values(), playerData):
				return False
		return True

	def checkCreateRoomRules(self, matchData):
		for rule in self.createRoomRules:
			if not rule.check(self, matchData["playersData"].values()):
				DEBUG_MSG("Matcher_checkCreateRoomRules::returns False!")
				return False
		DEBUG_MSG("Matcher_checkCreateRoomRules::returns True!")
		return True

	def checkMatchDataToJoinRoom(self, matchData):
		matchFlag   = self.ifArriveMinPlayers(matchData)
		creRoomflag = self.checkCreateRoomRules(matchData)
		if matchFlag and creRoomflag:
			#如果当前到达开启房间的条件,则状态设置为匹配结束ID_MATCH_END
			if matchData["state"] <= ID_MATCHING:
				matchData["state"] = ID_MATCH_END
			DEBUG_MSG("Matcher_checkMatchDataToJoinRoom::returns True!, matchData[state] = [%i]" % matchData["state"])
			return True
		elif matchFlag and not creRoomflag:
			#如果当前到达开启房间的条件,则状态设置为匹配结束ID_MATCH_END
			if matchData["state"] <= ID_MATCHING:
				matchData["state"] = ID_MATCH_CREROOMRULE

		return False

	def checkMatchDataToJoinRoomByMatchId(self, matchId):
		if matchId in self.matchPools:
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
			DEBUG_MSG("Matcher_ifArriveMinPlayers::maxPlayers is equal to 0!")
			return False
		if self.minPlayers >= 0 and len(matchData["playersData"]) < self.minPlayers:
			DEBUG_MSG("Matcher_ifArriveMinPlayers::len(matchDatamin) is less than y! minPlayers[%i]_(matchDatamin)len[%i]" % (self.minPlayers, len(matchData["playersData"])))
			return False
		DEBUG_MSG("Matcher_ifArriveMinPlayers::returns True!")
		return True

	def enterRoom(self, matchId, cmptObj, entityCall):

		matchData = self.matchPools[matchId]
		DEBUG_MSG("Matcher_enterRoom===============, matchId[%i], matchState[%i]" % (matchId, matchData["state"]))
		if matchData["state"] <= ID_MATCH_END:
			#表示房间仍然未创建
			if matchData["state"] != ID_LOADING_TIME and matchData["loadTimeOfBefCreRoom"] > 0:
				matchData["state"] = ID_LOADING_TIME
				#倒计时加载时间处理
				timeId = self.addTimer(matchData["loadTimeOfBefCreRoom"], 0, matchId)
				self.loadId[timeId] = matchId
				DEBUG_MSG("Matcher_enterRoom::::matchData[state] == ID_LOADING_TIME!")
			else:
				self.createRoom(matchId)
				DEBUG_MSG("Matcher_enterRoom::::createRoom")
		elif matchData["state"] >= ID_ROOM_CREATION_COMPLETE:
			#表示房间创建好了
			roomDatas = matchData["roomData"]
			roomEntityCall = roomDatas["roomCellEntityCall"]

			#创建成功后将玩家扔到baseRoom中
			players = {entityCall.id : entityCall}
			roomDatas["cmptObj"].onEnterRoom(players)

			if roomEntityCall:
				#加入房间中
				cmptObj.createCell(roomDatas["roomBaseEntityCall"], roomEntityCall, matchId, roomDatas["roomKey"])
				DEBUG_MSG("Matcher_enterRoom_exitCellRoom[%i]" % (roomEntityCall.id))

		#通知各个玩家现在为等待创建和进入房间时
		self.broadcastMatchState(matchData["playersData"], matchData["state"])

	def createRoom(self, matchId):
		DEBUG_MSG("Matcher_createRoom===============, matchId[%i]" % matchId)
		matchData = self.matchPools[matchId]
		matchData["state"] = ID_ROOM_CREATION_BEGIN
		newRoomKey = KBEngine.genUUID64()
		params = {
			"cmptBaseMatcherRoom": {"roomKey" : matchId},
			"cmptCellMatcherRoom": {"roomKeyC": matchId}
		}
		KBEngine.createEntityAnywhere(self.roomName, params, Functor.Functor(self.onRoomCreatedCB, matchId))
		matchData["arriveMaxUser"] = self.ifArriveMaxPlayers(self.matchPools[matchId])
		playersData = matchData["playersData"]
		self.broadcastMatchState(playersData, matchData["state"])
		pass

	def onRoomCreatedCB(self, matchId, roomEntityCall):
		DEBUG_MSG("Matcher_onRoomCreatedCB::Mather[%s], roomCellEntityCall[%s]::_onRoomCreatedCB::matchData!" % (self.name, roomEntityCall))
		#加载room的base部分成功后
		matchData = self.matchPools.get(matchId, None)
		if matchData:
			roomData  = {"roomBaseEntityCall":roomEntityCall, "roomCellEntityCall":None, "roomKey":matchId }
			matchData["roomData"] = roomData
			matchData["state"] = ID_MATCH_END

			#创建成功后将玩家扔到baseRoom中
			players = {}
			playersData = matchData["playersData"]
			for playerEntityId in playersData.keys():
				players[playerEntityId] = playersData[playerEntityId]["entityCall"]
			cmptObj = KBEngine.entities[roomEntityCall.id].getComponent("MatchBaseRoomReport")
			roomData["cmptObj"] = cmptObj
			DEBUG_MSG("Matcher_onRoomCreatedCB::basePlayers[%s]" % str(players))
			cmptObj.onEnterRoom(players)


	def onRoomGetCell(self, roomCellEntityCall, matchId, spaceID):

		matchData = self.matchPools.get(matchId, None)
		if not matchData:
			DEBUG_MSG("Matcher_component(Mather[%s])::_onRoomGetCell no matchData!, matchId[%i]" %(self.name, matchId))
			return

		DEBUG_MSG("Matcher_component(Mather[%s], roomCellEntityCall[%s])::_onRoomGetCell::matchData!"%(self.name, roomCellEntityCall) )
		matchData["state"] = ID_ROOM_CREATION_COMPLETE
		roomDatas   = matchData["roomData"]
		playersData = matchData["playersData"]

		roomBaseEntityCall = roomDatas["roomBaseEntityCall"]

		######为了方便访问，将base属性的roomEntityCall与当前的房间SpaceId联系保存起来######
		KBEngine.globalData["Room_%i" % spaceID] = roomBaseEntityCall

		#加载room的cell部分成功后
		roomDatas["roomCellEntityCall"] = roomCellEntityCall

		for playerEntityId in playersData.keys():
			DEBUG_MSG("Matcher_onRoomGerCell::entity[%i][%s], players.count(%i)" % (playerEntityId, playersData[playerEntityId]["cmptObj"], len(playersData)))
			cmptObj = playersData[playerEntityId]["cmptObj"]
			avatarCmptObj = playersData[playerEntityId]["cmptObj"]
			avatarCmptObj.createCell(roomBaseEntityCall, roomCellEntityCall, matchId, roomDatas["roomKey"])

	def playerEnterRoom(self, entityId, cmptName, roomEntityCall):
		DEBUG_MSG("Matcher_playerEnterRoom::entity[%i][%s]" % (entityId, playersData[entityId]["cmptObj"]))
		cmptObj = playerData["cmptObj"]
		avatarCmptObj = playersData[entityId]["cmptObj"]
		avatarCmptObj.createCell(roomEntityCall, roomCellEntityCall, matchId, roomDatas["roomKey"])
		pass

	def onRoomDestory(self, matchId, spaceID):
		if not matchId in self.matchPools:
			return True

		if matchId in self.matchIds:
			self.matchIds.remove(matchId)

		del self.matchPools[matchId]
		del KBEngine.globalData["Room_%i" % spaceID]
		DEBUG_MSG("Matcher_onRoomDestory::destory_matchId[%i], pools.len[%i]." % (matchId, len(self.matchPools)))
		return True

	def broadcastPlayerJoin(self, entityId, cmptObj, matchData):
		"""
			广播玩家匹配信息
		"""
		DEBUG_MSG("Mather_pushMatchPlayersData::entityCall_Id[%i]" % (entityId))
		playersData = matchData["playersData"]
		playerEntityIds = playersData.keys()
		state = matchData["state"]

		#推送消息
		for playerEntityId in playerEntityIds:
			if playerEntityId != entityId:
				avatarCmptObj = playersData[playerEntityId]["cmptObj"]
				avatarCmptObj.onJoinMatch({entityId:playersData[entityId]}, state)

		cmptObj.onJoinMatch(playersData, state)

	def broadcastMatchState(self, playersData, matchState):
		for playerEntityId in playersData.keys():
			DEBUG_MSG("Matcher_broadcastMatchState::players.count(%i), cmptObj[%s], matchState[%i]" %(len(playersData), playersData[playerEntityId]["cmptObj"], matchState))
			avatarCmptObj = playersData[playerEntityId]["cmptObj"]
			avatarCmptObj.onMatchStateChaned(matchState)

	def broadcastExitMatch(self, playersData, entityId):
		"""
			发送离开匹配的玩家信息
		"""
		DEBUG_MSG("Matcher_sendExitMatchMsg::self.enterGameAvatars.count(%i),exitEntitiyId[%i]" % (len(playersData), entityId))
		for playerEntityId in playersData.keys():
			# cmptName = playersData[entityCall]["cmptName"]
			# avatarCmptObj = getattr(entityCall, cmptName)
			avatarCmptObj = playersData[playerEntityId]["cmptObj"]
			avatarCmptObj.onExitMatch(entityId)
		pass

	def changePlayerMatchData(self, matchId, entityCall, playerData, allReplace = False):
		if matchId in self.matchPools:
			playersData = self.matchPools[matchId]["playersData"]
			if entityCall.id in playersData:
				srcPlayerData = playersData[entityCall.id]
				if allReplace == False:
					for keyValue in playerData.keys():
						srcPlayerData[keyValue] = playerData[keyValue]
				else:
					playerData["cmptObj"] = playerData.get("cmptObj", srcPlayerData["cmptObj"])
					playerData["playerData"] = playerData.get("entityCall", entityCall)
					playersData[entityCall.id] = playerData
			else:
				return False
		else:
			return False
		return True

	def matchDataChanged(self, matchId, entityCall, playerData, allReplace = False):
		"""
			玩家外部修改匹配数据
		"""
		if not self.changePlayerMatchData(matchId, entityCall, playerData, allReplace):
			return False

		#当修改成功后，需要重新判断匹配
		matchData = self.matchPools[matchId]
		playersData =  matchData["playersData"]

		#遍历当前在匹配池中的所有玩家对象，推动玩家改变的匹配信息
		DEBUG_MSG("matchDataChanged_num:::[%i]" % (len(playersData.keys())))
		for playerEntityId in playersData.keys():
			# avatarCmptObj  = getattr(playerEntity, playersData[playerEntity]["cmptObj"])
			avatarCmptObj  = playersData[playerEntityId]["cmptObj"]
			avatarCmptObj.onMatchDataChanged(entityCall.id, playerData)

		#查看是否满足创建房间或者加入房间的条件
		if self.checkMatchDataToJoinRoomByMatchId(matchId):
			self.enterRoom(matchId, playersData[entityCall.id]["cmptObj"], entityCall)
		return True

	def onTimer(self, id, userArg):
		if id in self.loadId:
			DEBUG_MSG("onTimer_createRoom is success!!")
			self.createRoom(self.loadId[id])
			self.loadId.pop(id)
			self.delTimer(id)

	def acquireAllPlayersMatchData(self, matchId):
		if matchId in self.matchPools:
			return self.matchPools[matchId]["playersData"]
		return {}

	def acquireOnePlayerMatchData(self, matchId, entityCall):
		'''
			获取matchPool中的指定匹配对象中的指定玩家数据
		'''
		if matchId in self.matchPools:
			return self.matchPools[matchId]["playersData"][entityCall]
		return {}
