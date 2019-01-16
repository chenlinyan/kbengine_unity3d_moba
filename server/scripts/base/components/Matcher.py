# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import Functor

# 代码标号
CODE_SUCCESS 									= 1 	# success
CODE_ERR_MAXPALYERS_EQUAL_ZERO 					= 2 	# MaxPlayers is equal to 0!
CODE_ERR_MAXPALYERS_LESS_THAN_MINPALYERS 		= 3 	# MaxPlayers is less than minPlayers!
CODE_ERR_ENTER_END_OF_MATCH 					= 4 	# The match has entered the end of the match!
CODE_ERR_NO_SATISY_MATCHRULE 					= 5 	# The match rule is not satisfied!
CODE_ERR_NO_SATISY_CREATEROOMRULE 				= 6 	# The createRoom rule is not satisfied!
CODE_ERR_NO_REACH_MINUSERS 						= 7 	# The minimum number has not been reached!
CODE_ERR_NO_REACH_MAXUSERS 						= 8 	# The maximum number has not been reached!
CODE_ERR_REACH_MAXUSERS 						= 9 	# The maximum number has been reached!
CODE_ERR_MATCHID_NO_EXIST_IN_MATCHPOOL			= 10 	# The matchId does no exist in the matchpool!
CODE_ERR_ENTIYTID_NO_EXIST_IN_PLAYERDATA 		= 11 	# The entityId does no exist in the playerData!

# 匹配状态
MATCH_STATE_BEGIN 					= 0
MATCH_STATE_MATCHING 				= 1
MATCH_STATE_MATCH_CREROOM_RULE 		= 2
MATCH_STATE_END 					= 3
MATCH_STATE_LOADING_TIME 			= 4
MATCH_STATE_ROOM_CREATION_BEGIN 	= 5
MATCH_STATE_ROOM_CREATION_COMPLETE 	= 6

# 常量标识
INVALIDID_MATCHID 	 = -1

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

		self.minPlayers = -1
		self.maxPlayers = -1
		self.matchTime  = -1
		self.matchRules = []
		self.matchPools = {}
		self.lastMatchId = 1
		self.lastErrorCode = CODE_SUCCESS

		# 存储未满人数的matchId
		self.matchIds = []

		self.roomName = "Room"
		self.createRoomRules = []
		self.befCreRoomLoadTime = 3
		self.creatingRoomForMatchIDs = {}

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
		if self.checkSettingsForError():
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

		# 获取entity对应的相应组件MatchAvatarReport
		compObj = entityCall.getComponent("MatchAvatarReport")
		assert compObj != None,'avatar 没有挂载MatchAvatarReport组件'

		matchData = self.matchPools[reqsMatchId]
		playerData["compObj"] = compObj
		playerData["entityCall"] = playerData.get("entityCall", entityCall)
		matchData["playersData"][entityCall.id] = playerData

		# 再次判断匹配池中是否到达最大人数，到达人数则移除
		if self.ifArriveMaxPlayers(matchData):
			if reqsMatchId in self.matchIds:
				self.matchIds.remove(reqsMatchId)

		# 推送匹配信息
		self.broadcastPlayerJoin(entityCall.id, compObj, matchData)

		# 检查条件是否达到可以加入房间
		if self.checkMatchDataToJoinRoom(matchData):
			self.enterRoom(reqsMatchId, compObj, entityCall)

		self.lastErrorCode = CODE_SUCCESS
		return reqsMatchId

	def exitMatch(self, entityId, matchId):
		"""
		退出匹配
		"""
		DEBUG_MSG("Matcher_exitMatch::avatar_entityId[%i], matchObjId[%i] " % (entityId, matchId))

		matchData = self.matchPools.get(matchId)
		if matchData is None:
			DEBUG_MSG("Matcher_exitMatch::self.matchPools not exit matchObjId[%i], self.matchPools[%s] " % (matchId, str(self.matchPools)))
			return True

		playersData = matchData["playersData"]
		if matchData["state"] > MATCH_STATE_END:
			self.lastErrorCode = CODE_ERR_ENTER_END_OF_MATCH
			return False
		else:
			if entityId in playersData.keys():
				self.broadcastExitMatch(playersData, entityId)
				del playersData[entityId]

				# 如果当下没有玩家数据，则释放匹配池中对象的匹配对象
				if len(playersData) == 0:
					del self.matchPools[matchId]
					if matchId in self.matchIds:
						self.matchIds.remove(matchId)

			return True

	def createNewMatch(self, playerData):
		'''
		没有可用资源，便创建一个新的匹配对象
		'''
		#如果不符合匹配条件，则不创建新的匹配对象
		if not self.checkMatchCondition({}, playerData):
			return INVALIDID_MATCHID

		# loadTimeOfBefCreRoom：表示创建房间前的等待加载时间
		baseMatchArg = {"matchId": self.lastMatchId,
						"matchName:": "defineName",
						"state": MATCH_STATE_MATCHING,
						"arriveMaxUser" : False,
						"loadTimeOfBefCreRoom": self.befCreRoomLoadTime,
						"autoOpenRoom": True,
						"playersData":{}}

		self.matchPools[self.lastMatchId] = baseMatchArg
		self.matchIds.append(self.lastMatchId)

		DEBUG_MSG("Matcher_createNewMatch::self.lastMatchId[%i][%i]" % (self.lastMatchId, baseMatchArg["matchId"]))

		self.lastMatchId = self.lastMatchId + 1
		return baseMatchArg["matchId"]

	def randomJoinMatch(self, playerData):
		DEBUG_MSG("Matcher_randomJoinMatch::self.matchIds[%s]" % (str(self.matchIds)))

		if self.matchIds:
			matchId = self.matchIds[0]
			if self.checkMatchCondition(self.matchPools[matchId], playerData):
				return matchId

			return INVALIDID_MATCHID
		else:
			return self.createNewMatch(playerData)

	def assignJoinMatch(self, matchId, playerData):
		matchId = self.matchPools.get(matchId, INVALIDID_MATCHID)
		if self.checkMatchCondition(self.matchPools[matchId], playerData):
			return matchId

		return INVALIDID_MATCHID

	def checkMatchCondition(self, matchData, playerData):
		allPlayersData = (matchData.get("playersData", {})).values()
		if self.checkMatchRules(allPlayersData, playerData) and \
			self.checkBuildInCondition(allPlayersData, playerData):
			return True
		else:
			DEBUG_MSG("Matcher_checkMatchCondition::matchResult is false!")
			return False

	def checkSettingsForError(self):
		'''
		检查常规设置是否出错
		'''
		if self.maxPlayers == 0:
			self.lastErrorCode = CODE_ERR_MAXPALYERS_EQUAL_ZERO
			return True
		elif self.maxPlayers > 0 and self.minPlayers > self.maxPlayers:
			self.lastErrorCode = CODE_ERR_MAXPALYERS_LESS_THAN_MINPALYERS
			return True
		else:
			return False

	def checkBuildInCondition(self, allPlayersData, playerData):
		if self.maxPlayers > 0 and len(allPlayersData) >= self.maxPlayers:
			self.lastErrorCode = CODE_ERR_REACH_MAXUSERS
			return False

		return True

	def checkMatchRules(self, allPlayersData, playerData):
		for matchRule in self.matchRules:
			if not matchRule.check(self, allPlayersData, playerData):
				self.lastErrorCode = CODE_ERR_NO_SATISY_MATCHRULE
				return False

		return True

	def checkCreateRoomRules(self, matchData):
		for rule in self.createRoomRules:
			if not rule.check(self, matchData["playersData"].values()):
				self.lastErrorCode = CODE_ERR_NO_SATISY_CREATEROOMRULE
				return False

		DEBUG_MSG("Matcher_checkCreateRoomRules::returns True!")

		return True

	def checkMatchDataToJoinRoom(self, matchData):
		matchFlag = self.ifArriveMinPlayers(matchData)

		DEBUG_MSG("Matcher_checkMatchDataToJoinRoom::matchFlag[%i]" % (matchFlag))

		if matchFlag and self.checkCreateRoomRules(matchData):
			# 如果当前到达开启房间的条件，则状态设置为匹配结束MATCH_STATE_END
			if matchData["state"] <= MATCH_STATE_MATCHING:
				matchData["state"] = MATCH_STATE_END
			return True
		elif matchFlag:
			# 如果当前到达开启房间的条件，则状态设置为匹配结束MATCH_STATE_END
			if matchData["state"] <= MATCH_STATE_MATCHING:
				matchData["state"] = MATCH_STATE_MATCH_CREROOM_RULE
			return False

		return False

	def checkMatchDataToJoinRoomByMatchId(self, matchId):
		if matchId in self.matchPools:
			return self.checkMatchDataToJoinRoom(self.matchPools[matchId])
		else:
			self.lastErrorCode = CODE_ERR_MATCHID_NO_EXIST_IN_MATCHPOOL
			return False

	def ifArriveMaxPlayers(self, matchData):
		if self.maxPlayers < 0:
			self.lastErrorCode = CODE_ERR_NO_REACH_MAXUSERS
			return False

		if len(matchData["playersData"]) < self.maxPlayers:
			self.lastErrorCode = CODE_ERR_NO_REACH_MAXUSERS
			return False

		return True

	def ifArriveMinPlayers(self, matchData):
		if self.minPlayers >= 0 and len(matchData["playersData"]) < self.minPlayers:
			self.lastErrorCode = CODE_ERR_NO_REACH_MINUSERS
			return False

		return True

	def enterRoom(self, matchId, compObj, entityCall):
		matchData = self.matchPools[matchId]
		matchState = matchData["state"]
		DEBUG_MSG("Matcher_enterRoom::matchId[%i], matchState[%i]" % (matchId, matchState))

		if matchState <= MATCH_STATE_END:
			# 表示房间仍然未创建
			if matchState != MATCH_STATE_LOADING_TIME and matchData["loadTimeOfBefCreRoom"] > 0:
				matchState = MATCH_STATE_LOADING_TIME
				# 倒计时加载时间处理
				timeId = self.addTimer(matchData["loadTimeOfBefCreRoom"], 0, matchId)
				self.creatingRoomForMatchIDs[timeId] = matchId

				DEBUG_MSG("Matcher_enterRoom::::matchData[state] is equal to MATCH_STATE_LOADING_TIME!")
			else:
				self.createRoom(matchId)

				DEBUG_MSG("Matcher_enterRoom::::createRoom")
		elif matchState >= MATCH_STATE_ROOM_CREATION_COMPLETE:
			# 表示房间创建好了
			roomDatas = matchData["roomData"]
			roomEntityCall = roomDatas["roomCellEntityCall"]

			# 创建成功后将玩家扔到baseRoom中
			players = {entityCall.id : entityCall}
			roomDatas["compObj"].onEnterRoom(players)

			if roomEntityCall:
				# 加入房间中
				compObj.createCell(roomDatas["roomBaseEntityCall"], roomEntityCall, matchId, roomDatas["roomKey"])
				DEBUG_MSG("Matcher_enterRoom::exitCellRoom[%i]" % (roomEntityCall.id))

		# 通知各个玩家现在为等待创建和进入房间时
		self.broadcastMatchState(matchData["playersData"], matchState)

	def createRoom(self, matchId):
		DEBUG_MSG("Matcher_createRoom::matchId[%i]" % matchId)

		matchData = self.matchPools[matchId]
		matchData["state"] = MATCH_STATE_ROOM_CREATION_BEGIN

		params = {
			"compMatcherRoom": {"roomKey" : matchId, "roomKeyC": matchId}
		}

		KBEngine.createEntityAnywhere(self.roomName, params, Functor.Functor(self.onRoomCreatedCB, matchId))
		playersData = matchData["playersData"]
		self.broadcastMatchState(playersData, matchData["state"])

	def onRoomCreatedCB(self, matchId, roomEntityCall):
		'''
		加载room的base部分成功后
		'''
		DEBUG_MSG("Matcher_onRoomCreatedCB::Mather[%s], roomCellEntityCall[%s]::_onRoomCreatedCB::matchData!" % (self.name, roomEntityCall))

		matchData = self.matchPools.get(matchId, None)
		if matchData:
			roomData = {"roomBaseEntityCall":roomEntityCall, "roomCellEntityCall":None, "roomKey":matchId }
			matchData["roomData"] = roomData
			matchData["state"] = MATCH_STATE_END

			# 创建成功后将玩家扔到baseRoom中
			players = {}
			playersData = matchData["playersData"]

			for playerData in playersData.values():
				playerEntity = playerData["entityCall"]
				players[playerEntity.id] = playerEntity

			compObj = roomEntityCall.getComponent("MatchRoomReport")
			roomData["compObj"] = compObj

			DEBUG_MSG("Matcher_onRoomCreatedCB::basePlayers[%s]" % str(players))

			compObj.onEnterRoom(players)

	def onRoomGetCell(self, roomCellEntityCall, matchId):
		'''
		加载room的cell部分成功后
		'''
		matchData = self.matchPools.get(matchId, None)

		if not matchData:
			DEBUG_MSG("Matcher_onRoomGetCell::component_Mather[%s] no matchData! matchId[%i]" % (self.name, matchId))
			return

		matchData["state"] = MATCH_STATE_ROOM_CREATION_COMPLETE
		roomDatas = matchData["roomData"]
		playersData = matchData["playersData"]

		roomBaseEntityCall = roomDatas["roomBaseEntityCall"]

		# 加载room的cell部分成功后
		roomDatas["roomCellEntityCall"] = roomCellEntityCall

		for playerEntityId in playersData.keys():
			avatarCompObj = playersData[playerEntityId]["compObj"]
			avatarCompObj.createCell(roomBaseEntityCall, roomCellEntityCall, matchId, roomDatas["roomKey"])

			DEBUG_MSG("Matcher_onRoomGerCell::entity[%i][%s], players.count(%i)" % (playerEntityId, avatarCompObj, len(playersData)))

	def onRoomDestory(self, matchId):
		'''
		room的cell部分销毁时调用
		'''
		if not matchId in self.matchPools:
			return True

		if matchId in self.matchIds:
			self.matchIds.remove(matchId)

		del self.matchPools[matchId]

		DEBUG_MSG("Matcher_onRoomDestory::destory_matchId[%i], pools.len[%i]." % (matchId, len(self.matchPools)))

		return True

	def broadcastPlayerJoin(self, entityId, compObj, matchData):
		"""
		广播玩家匹配信息
		"""
		DEBUG_MSG("Mather_pushMatchPlayersData::entityCall_Id[%i]" % (entityId))

		state = matchData["state"]
		playersData = matchData["playersData"]
		joinPlayerData = playersData.get(entityId, None)

		# 推送消息
		for playerData in playersData.values():
			if playerData["entityCall"].id != entityId:
				avatarCompObj = playerData["compObj"]
				avatarCompObj.onJoinMatch({entityId:joinPlayerData}, state)

		compObj.onJoinMatch(playersData, state)

	def broadcastMatchState(self, playersData, matchState):
		'''
		广播匹配状态
		'''
		for playerData in playersData.values():
			avatarCompObj = playerData["compObj"]
			avatarCompObj.onMatchStateChaned(matchState)

			DEBUG_MSG("Matcher_broadcastMatchState::players.count(%i), compObj[%s], matchState[%i]" %(len(playersData), avatarCompObj, matchState))

	def broadcastExitMatch(self, playersData, entityId):
		"""
		发送离开匹配的玩家信息
		"""
		DEBUG_MSG("Matcher_broadcastExitMatch::self.enterGameAvatars.count(%i),exitEntitiyId[%i]" % (len(playersData), entityId))

		for playerData in playersData.values():
			avatarCompObj = playerData["compObj"]
			avatarCompObj.onExitMatch(entityId)

	def changePlayerMatchData(self, matchId, entityCall, playerData, allReplace = False):
		'''
		改变玩家匹配信息
		'''
		if matchId in self.matchPools:
			playersData = self.matchPools[matchId]["playersData"]
			if entityCall.id in playersData:
				srcPlayerData = playersData[entityCall.id]
				if allReplace == False:
					srcPlayerData.update(playerData)
				else:
					playerData["compObj"] = playerData.get("compObj", srcPlayerData["compObj"])
					playerData["playerData"] = playerData.get("entityCall", entityCall)
					playersData[entityCall.id] = playerData
			else:
				self.lastErrorCode = CODE_ERR_ENTIYTID_NO_EXIST_IN_PLAYERDATA
				return False
		else:
			self.lastErrorCode = CODE_ERR_MATCHID_NO_EXIST_IN_MATCHPOOL
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
		playersData = matchData["playersData"]

		# 遍历当前在匹配池中的所有玩家对象，推动玩家改变的匹配信息
		DEBUG_MSG("Matcher_matchDataChanged::playersData.len(%i)" % (len(playersData.keys())))

		for playerData in playersData.values():
			avatarCompObj = playerData["compObj"]
			avatarCompObj.onMatchDataChanged(entityCall.id, playerData)

		# 查看是否满足创建房间或者加入房间的条件
		if self.checkMatchDataToJoinRoomByMatchId(matchId):
			self.enterRoom(matchId, playersData[entityCall.id]["compObj"], entityCall)

		return True

	def onTimer(self, id, userArg):
		if id in self.creatingRoomForMatchIDs:
			self.createRoom(self.creatingRoomForMatchIDs[id])
			self.creatingRoomForMatchIDs.pop(id)
			self.delTimer(id)

			DEBUG_MSG("Matcher_onTimer::createRoom is success!!")

	def acquireAllPlayersMatchData(self, matchId):
		return self.matchPools.get(matchId, {}).get("playersData", {})

	def acquireOnePlayerMatchData(self, matchId, entityCall):
		'''
		获取matchPool中的指定匹配对象中的指定玩家数据
		'''
		matchData = self.matchPools.get(matchId, {})
		if matchData:
			return matchData.get("playersData", {}).get(entityCall, {})

		return {}

	def getLastErrorCode(self):
		return self.lastErrorCode