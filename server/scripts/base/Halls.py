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
	def check(self, matcher, allPlayersData, playerData):
		teamACount = 0
		teamBCount = 0
		DEBUG_MSG("TeamMatchRule_check:: str(%s)" % str(allPlayersData))
		for existPlayer in allPlayersData:
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
	def check(self, matcher, allPlayersData):
		DEBUG_MSG("HeroChooseRule_check:: str(%s)" % str(allPlayersData))
		for existPlayer in allPlayersData:
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
		self.configMatherCondition()

	#设置匹配器条件
	def configMatherCondition(self):
		DEBUG_MSG("Hall::configMatherCondition:::componentMatcher")
		self.componentMatcher.minPlayers = 2
		self.componentMatcher.maxPlayers = 10
		self.componentMatcher.addMatchRule(TeamMatchRule())
		self.componentMatcher.addCreateRoomRule(HeroChooseRule())
		pass

	def joinMatch(self, entityCall, playerData):
		matchObjId = self.componentMatcher.joinMatch(entityCall, 0, playerData)
		if matchObjId < 0:
			DEBUG_MSG("Halls_enterStartGame: avatar[%i] match failed!" % (entityCall.id))
		return matchObjId

	def exitMatch(self, entityId, matchId):
		DEBUG_MSG("Halls_exitMatch_entityId[%i], matchObjId::[%i]" % (entityId, matchId))

		if matchId < 0:
			return False
		else:
			#如果该玩家所处的匹配池正处于匹配状态，那么该玩家是被允许退出匹配的
			#若匹配池状态为已完成匹配，那是不允许退出的
			if self.componentMatcher.exitMatch(entityId, matchId):
				DEBUG_MSG("Halls_exitMatch_result[true]::[%i]" % entityId)
				return True
			else:
				return False

	def acquireAllPlayersMatchData(self, matchId):
		return self.componentMatcher.acquireAllPlayersMatchData(matchId)
		pass

	def acquireOnePlayerMatchData(self, matchId, entityId):
		return self.componentMatcher.acquireOnePlayerMatchData(matchId, entityId)
		pass

	def matchDataChanged(self, matchId, entityCall, playerData):
		#当前需改玩家数据属性成功
		self.componentMatcher.matchDataChanged(matchId, entityCall, playerData)












