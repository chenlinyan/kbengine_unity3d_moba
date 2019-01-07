# -*- coding: utf-8 -*-
import KBEngine
import Functor
from KBEDebug import *
import traceback
import GameConfigs
import GameConstants

from MATCHING_INFOS import TMatchingInfos
from MATCHING_INFOS import TMatchingInfosList
from Matcher import *

FIND_ROOM_NOT_FOUND = 0
FIND_ROOM_CREATING = 1

class TeamMatchRule(MatchRule):
	def check(self, matcher, existPlayersData, playerData):
		teamACount = 0
		teamBCount = 0
		DEBUG_MSG("TeamMatchRule_check:: str(%s)" % str(existPlayersData))
		for existPlayer in existPlayersData:
			if existPlayer["teamId"] == GameConfigs.TEAM_A_ID:
				teamACount = teamACount + 1
			else:
				teamBCount = teamBCount + 1

		arriveMaxPlayers_A = False
		arriveMaxPlayers_B = False

		maxPlayerCounts = matcher.maxPlayers/2
		#防止maxPlayerCounts为单数，以双数相除来规定玩家队伍个数
		if matcher.maxPlayers/2 != 0:
			maxPlayerCounts = maxPlayerCounts + 1

		if matcher.maxPlayers > 0:
			arriveMaxPlayers_A = (maxPlayerCounts == teamACount)
			arriveMaxPlayers_B = (maxPlayerCounts == teamBCount)

		if arriveMaxPlayers_A and arriveMaxPlayers_B:
			return False

		if not arriveMaxPlayers_A and teamACount <= teamBCount:
			playerData["teamId"] = GameConfigs.TEAM_A_ID
		elif  not arriveMaxPlayers_B:
			playerData["teamId"] = GameConfigs.TEAM_B_ID
		else:
			return False
		return True


class HeroChooseRule(CreateRoomRule):
	def check(self, matcher, existPlayersData):
		DEBUG_MSG("HeroChooseRule_check:: str(%s)" % str(existPlayersData))
		for existPlayer in existPlayersData:
			if existPlayer["heroId"] == 0:
				return False
		return True

class Halls(KBEngine.Entity):
	"""
	这是一个脚本层封装的房间管理器
	"""
	def __init__(self):
		KBEngine.Entity.__init__(self)

		# 向全局共享数据中注册这个管理器的entityCall以便在所有逻辑进程中可以方便的访问
		KBEngine.globalData["Halls"] = self

		#進入大廳中所有的avatars
		#self.avatars = {}

		#大厅位置屬性
		self.position = 0;

		self.configMatherCondition()

	#设置匹配器条件
	def configMatherCondition(self):
		DEBUG_MSG("Hall::configMatherCondition:::componentMatcher")
		self.componentMatcher.minPlayers = 2
		self.componentMatcher.maxPlayers = 10
		self.componentMatcher.addMatchRule(TeamMatchRule())
		self.componentMatcher.addCreateRoomRule(HeroChooseRule())
		pass

	#注冊进入大廳
	# def registerHalls(self, entityCall, name):
	# 	if(not self.avatars.__contains__(entityCall.id)):
	# 		self.avatars[entityCall.id] = {}
	# 	avatarInfos = self.avatars[entityCall.id]

	# 	#属性赋值
	# 	avatarInfos["entityCall"] = entityCall
	# 	avatarInfos["name"] 	  = name
	# 	DEBUG_MSG("registerHalls_success_avatar[%i]" % entityCall.id)

	# #反注册退出大廳
	# def deregisterHalls(self, entityId):
	# 	DEBUG_MSG("Halls_deregisterHalls_entityId(%i)" % (entityId))
	# 	if(self.avatars.__contains__(entityId)):
	# 		del self.avatars[entityId]
	# 	else:
	# 		DEBUG_MSG("Halls_deregisterHalls_entityId(%i)  is no exit(avatars)" % (entityId))

	# def ifExitHalls(self, entityId):
	# 	if(self.avatars.__contains__(entityId)):
	# 		return True
	# 	else:
	# 		return False

	def startGame(self, entityCall, cmptName, playerData):
		#if self.ifExitHalls(entityCall.id):
		matchObjId = self.componentMatcher.joinMatch(entityCall, 0, cmptName, playerData)
		if matchObjId < 0:
			DEBUG_MSG("Halls_enterStartGame: avatar[%i] match failed!" % (entityCall.id))
		#self.avatars[entityCall.id]["matchId"] = matchObjId
		#else:
		#	DEBUG_MSG("Halls_enterStartGame: avatar[%i] is no regist halls!" % (entityCall.id))
		return matchObjId

	def leaveGame(self, entityCall, matchId):
		# avatarData = self.avatars[entityId]
		# if not avatarData.__contains__("matchId"):
		# 	return
		# matchId    = avatarData["matchId"]
		DEBUG_MSG("Halls_leaveGame_entityId[%i], matchObjId::[%i]" % (entityCall.id, matchId))

		if matchId < 0:
			return
		else:
			#如果该玩家所处的匹配池正处于匹配状态，那么该玩家是被允许退出匹配的
			#若匹配池状态为已完成匹配，那是不允许退出的
			if self.componentMatcher.leaveMatch(entityCall, matchId):
				DEBUG_MSG("Halls_leaveGame_result[true]::[%i]" % entityCall.id)

	def acquireAllPlayersMatchData(self, matchId):
		return self.componentMatcher.acquireAllPlayersMatchData(matchId)
		pass

	def acquireOnePlayerMatchData(self, matchId, entityCall):
		return self.componentMatcher.acquireOnePlayerMatchData(matchId, entityCall)
		pass

	def matchDataChanged(self, matchId, entityCall, playerData):
		#当前需改玩家数据属性成功
		self.componentMatcher.matchDataChanged(matchId, entityCall, playerData)


	def returnHalls(self, entityId):
		self.leaveGame(entityId)











