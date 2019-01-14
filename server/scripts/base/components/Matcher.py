# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import Functor

#错误码
ERRCODE_MAXPALYERS_EQUAL_ZERO 			= "MaxPlayers is equal to 0!"
ERRCODE_MAXPALYERS_LESS_THAN_MINPALYERS = "MaxPlayers is less than minPlayers!"
ERRCODE_ENTER_END_OF_MATCH 				= "The match has entered the end of the match!"
ERRCODE_NO_SATISY_MATCHRULE 			= "The match rule is not satisfied!"
ERRCODE_NO_SATISY_CREATEROOMRULE		= "The createRoom rule is not satisfied!"


#代码标号
CODE_CHECK_BUILDIN_CONDITION 	= "Build-In conditions checked successfully!"
CODE_CHECK_MATCH_RULE 			= "MatchRule checked successfully!"
CODE_CHECK_CREATEROOM_RULE 		= "CrateRoomRule checked successfully!"
CODE_CHECK_MATCH_CONDITION 		= "Match conditions checked successfully!"
CODE_JOIN_MATCH_SUCCESS 		= "Join match successfully!"
CODE_EXIT_MATCH_SUCCESS 		= "Exit match successfully!"
CODE_JOIN_ROOM_SUCCESS 			= "Join room successfully!"

CODE_REACH_MINUSERS 			= "The minimum number has been reached!"
CODE_REACH_MAXUSERS 			= "The maximum number has been reached!"
CODE_NO_REACH_MINUSERS 			= "The minimum number has not been reached!"
CODE_NO_REACH_MAXUSERS 			= "The maximum number has not been reached!"


# 匹配状态
ID_MATCH_BEGIN 				= 0
ID_MATCHING 				= 1
ID_MATCH_CREROOMRULE 		= 2
ID_MATCH_END 				= 3
ID_LOADING_TIME 			= 4
ID_ROOM_CREATION_BEGIN 		= 5
ID_ROOM_CREATION_COMPLETE 	= 6

# 常量标识
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

		# 存储未满人数的matchId
		self.matchIds = []

		self.roomName = "Room"
		self.createRoomRules = []
		self.befCreRoomLoadTime = 3
		self.loadId = {}

	def onAttached(self, owner):
		matcherObj = KBEngine.globalData.get("HallsMatcher", None)
		assert matcherObj == None,'同时挂载了多个Matcher组件'

		KBEngine.globalData["HallsMatcher"] = self.owner
		DEBUG_MSG("Matcher_onAttached::Matcher instances:%s" % (KBEngine.globalData["HallsMatcher"]))

	def onDetached(self, owner):
		pass

	def addMatchRule(self, ruleObj: MatchRule):
		self.matchRules.append(ruleObj)

	def addCreateRoomRule(self, ruleObj: CreateRoomRule):
		self.createRoomRules.append(ruleObj)

	def joinMatch(self, entityCall, matchId, playerData = {}):
		"""
		加入匹配
		"""
		DEBUG_MSG("Matcher_joinMatch::avatar[%i], matchId[%i] " % (entityCall.id, matchId))

		reqsMatchId = INVALIDID_MATCHID
		matchResult = self.checkSettingsForError()
		if matchResult[0]:
			return reqsMatchId, matchResult[1]

		# matchId <  0: 表示总要创建一个新的匹配对象
		# matchId == 0: 表示随机加入的匹配池的任意匹配对象
		# matchId > 0 : 表示加入指定的匹配对象
		if matchId < 0:
			reqsMatchId, matchResult = self.createNewMatch(playerData)
		elif matchId == 0:
			reqsMatchId, matchResult = self.randomJoinMatch(playerData)
		else:
			reqsMatchId, matchResult = self.assignJoinMatch(matchId, playerData)

		if reqsMatchId < 0:
			return reqsMatchId, matchResult[1]

		DEBUG_MSG("Matcher_joinMatch::avatar[%i], matchId[%i], reqsMatchId[%i] " % (entityCall.id, matchId, reqsMatchId))

		# 获取entity对应的相应组件MatchAvatarReport
		cmptObj = entityCall.getComponent("MatchAvatarReport")
		assert cmptObj != None,'avatar 没有挂载MatchAvatarReport组件'

		matchData = self.matchPools[reqsMatchId]
		playerData["cmptObj"] = cmptObj
		playerData["entityCall"] = playerData.get("entityCall", entityCall)
		matchData["playersData"][entityCall.id] = playerData

		# 再次判断匹配池中是否到达最大人数，到达人数则移除
		matchResult = self.ifArriveMaxPlayers(matchData)
		if matchResult[0]:
			if reqsMatchId in self.matchIds:
				self.matchIds.remove(reqsMatchId)

		# 推送匹配信息
		self.broadcastPlayerJoin(entityCall.id, cmptObj, matchData)

		# 检查条件是否达到可以加入房间
		matchResult = self.checkMatchDataToJoinRoom(matchData)
		if matchResult[0]:
			self.enterRoom(reqsMatchId, cmptObj, entityCall)

		return reqsMatchId, CODE_JOIN_MATCH_SUCCESS

	def exitMatch(self, entityId, matchId):
		"""
		退出匹配
		"""
		DEBUG_MSG("Matcher_exitMatch::avatar_entityId[%i], matchObjId[%i] " % (entityId, matchId))

		matchData = self.matchPools.get(matchId)
		if matchData is None:
			DEBUG_MSG("Matcher_exitMatch::self.matchPools not exit matchObjId[%i] " % (matchId))

			return True, CODE_EXIT_MATCH_SUCCESS

		playersData = matchData["playersData"]
		if matchData["state"] > ID_MATCH_END:
			return False, ERRCODE_ENTER_END_OF_MATCH
		else:
			if entityId in playersData.keys():
				self.broadcastExitMatch(playersData, entityId)
				del playersData[entityId]

				# 如果当下没有玩家数据，则释放匹配池中对象的匹配对象
				if len(playersData) == 0:
					del self.matchPools[matchId]
					if matchId in self.matchIds:
						self.matchIds.remove(matchId)

			return True, CODE_EXIT_MATCH_SUCCESS

	def createNewMatch(self, playerData):
		'''
		没有可用资源，便创建一个新的匹配对象
		'''
		#如果不符合匹配条件，则不创建新的匹配对象
		matchResult = self.checkMatchCondition({}, playerData)
		if not matchResult[0]:
			return INVALIDID_MATCHID, matchResult[1]

		# loadTimeOfBefCreRoom：表示创建房间前的等待加载时间
		baseMatchArg = {"matchId": self.matchId,
						"matchName:": "defineName",
						"state": ID_MATCHING,
						"arriveMaxUser" : False,
						"loadTimeOfBefCreRoom": self.befCreRoomLoadTime,
						"autoOpenRoom": True,
						"playersData":{}}

		self.matchPools[self.matchId] = baseMatchArg
		self.matchIds.append(self.matchId)

		DEBUG_MSG("Matcher_createNewMatch::self.matchId[%i][%i]" % (self.matchId, baseMatchArg["matchId"]))

		self.matchId = self.matchId + 1
		return baseMatchArg["matchId"], matchResult[1]

	def randomJoinMatch(self, playerData):
		DEBUG_MSG("Matcher_randomJoinMatch::self.matchIds[%s]" % (str(self.matchIds)))

		if self.matchIds:
			matchId = self.matchIds[0]
			matchResult = self.checkMatchCondition(self.matchPools[matchId], playerData)
			if matchResult[0]:
				return matchId, matchResult[1]
			return INVALIDID_MATCHID, matchResult[1]
		else:
			return self.createNewMatch(playerData)

	def assignJoinMatch(self, matchId, playerData):
		matchId = self.matchPools.get(matchId, INVALIDID_MATCHID)
		matchResult = self.checkMatchCondition(self.matchPools[matchId], playerData)
		if matchId != INVALIDID_MATCHID and matchResult[0]:
			return matchId, matchResult[1]

		return INVALIDID_MATCHID, matchResult[1]

	def checkMatchCondition(self, matchData, playerData):
		allPlayersData = (matchData.get("playersData", {})).values()
		matchResult = self.checkMatchRules(allPlayersData, playerData)
		bulidInResult = self.checkBuildInCondition(allPlayersData, playerData)

		DEBUG_MSG("Matcher_checkMatchCondition::matchResult[%s], bulidInResult[%s]" % (str(matchResult), str(bulidInResult)))

		if bulidInResult[0]:
			if matchResult[0]:
				return True, CODE_CHECK_MATCH_CONDITION
			else:
				return matchResult
		else:
			return bulidInResult


	def checkSettingsForError(self):
		'''
		检查常规设置是否出错
		'''
		if self.maxPlayers == 0:
			return True, ERRCODE_MAXPALYERS_EQUAL_ZERO
		elif self.maxPlayers > 0 and self.minPlayers > self.maxPlayers:
			return True, ERRCODE_MAXPALYERS_LESS_THAN_MINPALYERS
		else:
			return False, CODE_CHECK_MATCH_CONDITION

	def checkBuildInCondition(self, allPlayersData, playerData):
		if self.maxPlayers > 0 and len(allPlayersData) >= self.maxPlayers:
			return False, CODE_REACH_MAXUSERS

		return True, CODE_CHECK_BUILDIN_CONDITION

	def checkMatchRules(self, allPlayersData, playerData):
		for matchRule in self.matchRules:
			if not matchRule.check(self, allPlayersData, playerData):
				return False, ERRCODE_NO_SATISY_MATCHRULE

		return True, CODE_CHECK_MATCH_RULE

	def checkCreateRoomRules(self, matchData):
		for rule in self.createRoomRules:
			if not rule.check(self, matchData["playersData"].values()):
				return False, ERRCODE_NO_SATISY_CREATEROOMRULE

		DEBUG_MSG("Matcher_checkCreateRoomRules::returns True!")

		return True, CODE_CHECK_CREATEROOM_RULE

	def checkMatchDataToJoinRoom(self, matchData):
		matchFlag, matchResult = self.ifArriveMinPlayers(matchData)
		creRoomflag, creRoomResult = self.checkCreateRoomRules(matchData)

		DEBUG_MSG("Matcher_checkMatchDataToJoinRoom::matchFlag[%i], creRoomflag[%i]" % (matchFlag, creRoomflag))

		if matchFlag and creRoomflag:
			# 如果当前到达开启房间的条件，则状态设置为匹配结束ID_MATCH_END
			if matchData["state"] <= ID_MATCHING:
				matchData["state"] = ID_MATCH_END

			return True, CODE_JOIN_ROOM_SUCCESS
		elif matchFlag and not creRoomflag:
			# 如果当前到达开启房间的条件，则状态设置为匹配结束ID_MATCH_END
			if matchData["state"] <= ID_MATCHING:
				matchData["state"] = ID_MATCH_CREROOMRULE
			return False, creRoomResult

		return False, matchResult

	def checkMatchDataToJoinRoomByMatchId(self, matchId):
		if matchId in self.matchPools:
			matchFlag, matchResult = self.checkMatchDataToJoinRoom(self.matchPools[matchId])
			return matchFlag
		else:
			return False

	def ifArriveMaxPlayers(self, matchData):
		if self.maxPlayers < 0:
			return False, CODE_NO_REACH_MAXUSERS

		if len(matchData["playersData"]) < self.maxPlayers:
			return False, CODE_NO_REACH_MAXUSERS

		return True, CODE_REACH_MAXUSERS

	def ifArriveMinPlayers(self, matchData):
		if self.minPlayers >= 0 and len(matchData["playersData"]) < self.minPlayers:
			return False, CODE_NO_REACH_MINUSERS

		return True, CODE_REACH_MINUSERS

	def enterRoom(self, matchId, cmptObj, entityCall):
		matchData = self.matchPools[matchId]
		matchState = matchData["state"]
		DEBUG_MSG("Matcher_enterRoom::matchId[%i], matchState[%i]" % (matchId, matchState))

		if matchState <= ID_MATCH_END:
			# 表示房间仍然未创建
			if matchState != ID_LOADING_TIME and matchData["loadTimeOfBefCreRoom"] > 0:
				matchState = ID_LOADING_TIME
				# 倒计时加载时间处理
				timeId = self.addTimer(matchData["loadTimeOfBefCreRoom"], 0, matchId)
				self.loadId[timeId] = matchId

				DEBUG_MSG("Matcher_enterRoom::::matchData[state] is equal to ID_LOADING_TIME!")
			else:
				self.createRoom(matchId)

				DEBUG_MSG("Matcher_enterRoom::::createRoom")
		elif matchState >= ID_ROOM_CREATION_COMPLETE:
			# 表示房间创建好了
			roomDatas = matchData["roomData"]
			roomEntityCall = roomDatas["roomCellEntityCall"]

			# 创建成功后将玩家扔到baseRoom中
			players = {entityCall.id : entityCall}
			roomDatas["cmptObj"].onEnterRoom(players)

			if roomEntityCall:
				# 加入房间中
				cmptObj.createCell(roomDatas["roomBaseEntityCall"], roomEntityCall, matchId, roomDatas["roomKey"])
				DEBUG_MSG("Matcher_enterRoom::exitCellRoom[%i]" % (roomEntityCall.id))

		# 通知各个玩家现在为等待创建和进入房间时
		self.broadcastMatchState(matchData["playersData"], matchState)

	def createRoom(self, matchId):
		DEBUG_MSG("Matcher_createRoom::matchId[%i]" % matchId)

		matchData = self.matchPools[matchId]
		matchData["state"] = ID_ROOM_CREATION_BEGIN
		newRoomKey = KBEngine.genUUID64()

		params = {
			"cmptMatcherRoom": {"roomKey" : matchId, "roomKeyC": matchId}
		}

		KBEngine.createEntityAnywhere(self.roomName, params, Functor.Functor(self.onRoomCreatedCB, matchId))
		matchData["arriveMaxUser"] = self.ifArriveMaxPlayers(self.matchPools[matchId])
		playersData = matchData["playersData"]
		self.broadcastMatchState(playersData, matchData["state"])

	def onRoomCreatedCB(self, matchId, roomEntityCall):
		'''
		加载room的base部分成功后
		'''
		DEBUG_MSG("Matcher_onRoomCreatedCB::Mather[%s], roomCellEntityCall[%s]::_onRoomCreatedCB::matchData!" % (self.name, roomEntityCall))

		matchData = self.matchPools.get(matchId, None)
		if matchData:
			roomData  = {"roomBaseEntityCall":roomEntityCall, "roomCellEntityCall":None, "roomKey":matchId }
			matchData["roomData"] = roomData
			matchData["state"] = ID_MATCH_END

			# 创建成功后将玩家扔到baseRoom中
			players = {}
			playersData = matchData["playersData"]

			for playerEntityId in playersData.keys():
				players[playerEntityId] = playersData[playerEntityId]["entityCall"]

			cmptObj = roomEntityCall.getComponent("MatchRoomReport")
			roomData["cmptObj"] = cmptObj

			DEBUG_MSG("Matcher_onRoomCreatedCB::basePlayers[%s]" % str(players))

			cmptObj.onEnterRoom(players)

	def onRoomGetCell(self, roomCellEntityCall, matchId, spaceID):
		'''
		加载room的cell部分成功后
		'''
		matchData = self.matchPools.get(matchId, None)

		if not matchData:
			DEBUG_MSG("Matcher_onRoomGetCell::component_Mather[%s] no matchData! matchId[%i]" % (self.name, matchId))
			return

		matchData["state"] = ID_ROOM_CREATION_COMPLETE
		roomDatas   = matchData["roomData"]
		playersData = matchData["playersData"]

		roomBaseEntityCall = roomDatas["roomBaseEntityCall"]

		# ######为了方便访问，将base属性的roomEntityCall与当前的房间SpaceId联系保存起来######
		KBEngine.globalData["Room_%i" % spaceID] = roomBaseEntityCall
		DEBUG_MSG("Matcher_Matcher_onRoomGetCell::Mather[%s], roomCellEntityCall[%s], KBEngine.globalData[Room_%i] = [%s]" % (self.name, roomCellEntityCall, spaceID, str(KBEngine.globalData["Room_%i" % spaceID])))

		# 加载room的cell部分成功后
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

	def onRoomDestory(self, matchId, spaceID):
		'''
		room的cell部分销毁时调用
		'''
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

		# 推送消息
		for playerEntityId in playerEntityIds:
			if playerEntityId != entityId:
				avatarCmptObj = playersData[playerEntityId]["cmptObj"]
				avatarCmptObj.onJoinMatch({entityId:playersData[entityId]}, state)

		cmptObj.onJoinMatch(playersData, state)

	def broadcastMatchState(self, playersData, matchState):
		'''
		广播匹配状态
		'''
		for playerEntityId in playersData.keys():
			avatarCmptObj = playersData[playerEntityId]["cmptObj"]
			avatarCmptObj.onMatchStateChaned(matchState)

			DEBUG_MSG("Matcher_broadcastMatchState::players.count(%i), cmptObj[%s], matchState[%i]" %(len(playersData), playersData[playerEntityId]["cmptObj"], matchState))

	def broadcastExitMatch(self, playersData, entityId):
		"""
		发送离开匹配的玩家信息
		"""
		DEBUG_MSG("Matcher_broadcastExitMatch::self.enterGameAvatars.count(%i),exitEntitiyId[%i]" % (len(playersData), entityId))

		for playerEntityId in playersData.keys():
			avatarCmptObj = playersData[playerEntityId]["cmptObj"]
			avatarCmptObj.onExitMatch(entityId)

	def changePlayerMatchData(self, matchId, entityCall, playerData, allReplace = False):
		'''
		改变玩家匹配信息
		'''
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

		# 当修改成功后，需要重新判断匹配
		matchData = self.matchPools[matchId]
		playersData =  matchData["playersData"]

		# 遍历当前在匹配池中的所有玩家对象，推动玩家改变的匹配信息
		DEBUG_MSG("Matcher_matchDataChanged::playersData.len(%i)" % (len(playersData.keys())))

		for playerEntityId in playersData.keys():
			avatarCmptObj  = playersData[playerEntityId]["cmptObj"]
			avatarCmptObj.onMatchDataChanged(entityCall.id, playerData)

		# 查看是否满足创建房间或者加入房间的条件
		if self.checkMatchDataToJoinRoomByMatchId(matchId):
			self.enterRoom(matchId, playersData[entityCall.id]["cmptObj"], entityCall)

		return True

	def onTimer(self, id, userArg):
		if id in self.loadId:
			self.createRoom(self.loadId[id])
			self.loadId.pop(id)
			self.delTimer(id)

			DEBUG_MSG("Matcher_onTimer::createRoom is success!!")

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
