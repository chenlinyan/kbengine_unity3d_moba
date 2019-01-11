# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import GameConfigs
import GameConstants
import GameUtils
import random
from MATCHING_INFOS import TMatchingInfos
from MATCHING_INFOS import TMatchingInfosList
import MatchAvatarReport
from CSV_Helper import *

TIMER_TYPE_DESTROY = 1
TIMER_TYPE_LEAVEROOM = 2
TIMER_TYPE_ADJUST_FRAMEID = 3

class Avatar(KBEngine.Proxy):
	def __init__(self):
		KBEngine.Proxy.__init__(self)

		self.cellData["dbid"] = self.databaseID

		# 随机一个角色模型
		self.cellData["modelID"] = random.randint(0, 1)

		# 获取账户名称
		self.cellData["name"]      = self.__ACCOUNT_NAME__
		self.cellData["teamId"]    = 0
		self.cellData["heroId"]    = 0
		self.cellData["heroIdLst"] = [10001, 10002]

		self.heroId = 0
		self.disconnectFlag = False

		# 获取cvs的配置数据对象
		self.conf = CSV_Helper()

		# 初始化为登录状态
		self.gameState = GameConstants.GAMESTATE_LOGIN

		self._destroyTimer = 0
		self._adjustFrameIdTimer = 0


		self.registerEvent(MatchAvatarReport.eventNameJoinMatch,	 	 self.onRecvPlayersJoinMatch)
		self.registerEvent(MatchAvatarReport.eventNameMatchStateChanged, self.onRecvPlayerMatchStateChanged)
		self.registerEvent(MatchAvatarReport.eventNameMatchDataChanged,	 self.onRecvPlayerMatchDataChanged)
		self.registerEvent(MatchAvatarReport.eventNameExitMatch,	 	 self.onRecvPlayerExitMatch)

	def destroySelf(self):
		"""
		"""
		if self.client is not None:
			return

		# 必须先销毁cell实体，才能销毁base
		if self.cell is not None:
			self.destroyCellEntity()
			return

		# 销毁base
		self.destroy()
		self._destroyTimer = 0
		self._adjustFrameIdTimer = 0

	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		if TIMER_TYPE_DESTROY == userArg:
			self.onDestroyTimer()

		if TIMER_TYPE_ADJUST_FRAMEID == userArg:
			# 异地重登后,玩家重新调整逻辑帧数
			# 修改帧数的功能暂时屏蔽带掉
			if self.cell:
				self.cell.adjustFrameId(0)
				self.delTimer(id)
				self._adjustFrameIdTimer = 0

				DEBUG_MSG("Avatat_base_onTimer::TIMER_TYPE_ADJUST_FRAMEID_____self.cell.adjustFrameId is 0")

	def onClientEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		INFO_MSG("Avatar[%i] entities enable. EntityCall:%s" % (self.id, self.client))

		# 如果异地重登调整帧数的计时器已经开启了，而玩家再次上线了,那么应该取消计时器
		if self._adjustFrameIdTimer > 0:
			self.delTimer(self._adjustFrameIdTimer)
			self._adjustFrameIdTimer = 0

		# 如果销毁玩家计时器已经开启了，此处玩家又上线了那么应该取消计时器
		if self._destroyTimer > 0:
			self.delTimer(self._destroyTimer)
			self._destroyTimer = 0
			self.disconnectFlag = False

		# 防止异地登录或者重连，将数据主动推送给客户端
		self.dealClientEnabled()

	def onClientDeath(self):
		"""
		KBEngine method.
		客户端对应实体已经销毁
		"""
		DEBUG_MSG("Avatar_base.onClientDeath::Avatar[%i]" % self.id)

		self.dealDisconnect()

	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		客户端登陆失败时会回调到这里
		"""
		INFO_MSG(ip, port, password)

		return KBEngine.LOG_ON_ACCEPT

	def onGetCell(self):

		"""
		KBEngine method.
		entity的cell部分实体被创建成功
		"""
		DEBUG_MSG('Avatar::onGetCell: %s' % self.cell)

	def onLoseCell(self):
		"""
		KBEngine method.
		entity的cell部分实体丢失
		"""
		DEBUG_MSG("%s::onLoseCell: %i" % (self.className, self.id))

		# 如果self._destroyTimer大于0说明之前已经由base请求销毁，通常是客户端断线了
		if self._destroyTimer > 0:
			self.destroySelf()
		else:
			# 否则由cell发起销毁， 那么说明游戏结束了
			self.gameState = GameConstants.GAMESTATE_HALL

	def onRestore(self):
		"""
		KBEngine method.
		entity的cell部分实体被恢复成功
		"""
		DEBUG_MSG("Avatar_base_onRestore::%s_onRestore: %s" % (self.getScriptName(), self.cell))

	def onDestroyTimer(self):
		DEBUG_MSG("Avatar_base_onDestroyTimer::avatarId[%i]" % (self.id))

		self.destroySelf()

	def reqJoinGame(self):
		"""
		加入游戏
		"""
		DEBUG_MSG("Avatar_base_reqJoinGame::[%s][%i]" %(self.cellData["name"], self.id))

		resultId = self.joinMatch()
		if self.client:
			self.client.onJoinGameResult(resultId)

	def reqExitGame(self):
		"""
		退出游戏
		"""
		resultId = self.exitMatch()
		if self.client:
			self.client.onExitGameResult(resultId)

	def joinMatch(self):
		"""
		加入匹配
		"""
		self.gameState = GameConstants.GAMESTATE_MATCHING
		playerData = {"entityCall":self, "id":self.id, "name":self.cellData["name"], "teamId": 0, "heroId": 0, "heroIdLst":self.cellData["heroIdLst"] }
		self.matchId  = KBEngine.globalData["Halls"].joinMatch(self, playerData)

		if self.matchId == -1:
			# 返回-1,表明匹配失败
			self.gameState = GameConstants.GAMESTATE_HALL
			return False

		return True

	def exitMatch(self):
		"""
		退出匹配
		"""
		if KBEngine.globalData["Halls"].exitMatch(self.id, self.matchId):
			self.cellData["heroId"] = 0
			self.cellData["teamId"] = 0
			self.heroId = 0
			self.gameState = GameConstants.GAMESTATE_HALL
			return True

		return False

	def onRecvPlayersJoinMatch(self, playersData, state):
		'''
			接收玩家匹配信息的推送
		'''
		DEBUG_MSG("Avatar_base_onRecvPlayersJoinMatch::entityCall[%i], playersData.len[%i],\
			str(playerData)[%s]" % (self.id, len(playersData), str(playersData)))

		tmpState = self.gameState
		matchInfoLst = TMatchingInfosList()

		for playerEntityId in playersData.keys():
			matchInfo = TMatchingInfos()
			matchInfoLst[playerEntityId] = matchInfo.createFromDict(playersData[playerEntityId])
			if playerEntityId == self.id:
				# 转换匹配状态为当前的游戏状态
				tmpState = self.transformMatchStateToGameState(state)

				# 在这里将分配好给玩家的team数值给赋值上
				teamId = playersData[playerEntityId]["teamId"]

				if self.cell is None:
					self.cellData["teamId"]  = teamId

				DEBUG_MSG("Avatar_base_onRecvPlayersJoinMatch::self.teamId_self.name::[%i]，[%s]" % (teamId, self.cellData["name"]))

		self.client.onPushMatchPlayersData(matchInfoLst)

	def onRecvPlayerMatchStateChanged(self, matchState):
		"""
		当前匹配对象状态发生改变，推送当前匹配对象状态
		"""
		self.gameState = self.transformMatchStateToGameState(matchState)

		if self.gameState == GameConstants.GAMESTATE_LOAD_TO_GAME:
			# 表示匹配成功后等待加载房间时段::ID_LOADING_TIME
			if self.client:
				self.client.onLoadingToReadyBattleState()

	def onRecvPlayerMatchDataChanged(self, entityId, playerData):
		'''
			接收玩家匹配信息的改变
		'''
		if playerData is None:
			return

		if playerData.__contains__("heroId") and self.client:
			self.client.onHeroIdChanged(entityId, playerData["heroId"])

	def onRecvPlayerExitMatch(self, entityId):
		DEBUG_MSG("Avatar_base_onRecvPlayerExitMatch::entityId[%i]" % entityId)

		if self.client:
			self.client.onExitMatch(entityId)
		pass

	def acquireAllPlayersMatchData(self):
		if self.matchId < 0:
			return {}

		return KBEngine.globalData["Halls"].acquireAllPlayersMatchData(self.matchId)

	def acquireOnePlayerMatchData(self):
		if self.matchId < 0:
			return {}

		return KBEngine.globalData["Halls"].acquireOnePlayerMatchData(self.matchId, self)

	def matchDataChanged(self, entityCall, playerData):
		if self.matchId < 0:
			return False

		KBEngine.globalData["Halls"].matchDataChanged(self.matchId, entityCall, playerData)

		return True

	def reqHeroInfosByHeroId(self, heroId):
		"""
		提交选择的英雄Id
		"""
		DEBUG_MSG("Avatar_base_reqHeroInfosByHeroId::avatar[%i]" % self.id)

		if self.cellData["heroId"] == heroId:
			return

		self.heroId = heroId
		self.cellData["heroId"] = heroId

		# 返回当前的英雄信息
		if self.client and self.cell is None:
			self.cellData["heroInfo"] = self.getHeroInfo(heroId)
			self.cellData["skillInfosLst"] = self.getSkillList(self.cellData["heroInfo"])
			self.client.onReqsChooseHeroResult(self.cellData["heroInfo"], self.cellData["skillInfosLst"])

		#需要向当前的玩家所在的匹配池中修改数据
		self.matchDataChanged(self, {"heroId":heroId})

	def getHeroInfo(self, heroId):
		return self.conf.getTable('d_hero.csv').get(heroId, None)

	def getSkillList(self, heroInfo):
		if self.cell or heroInfo is None:
			DEBUG_MSG("Avatar_base_getSkillIdList:: heroInfos is None!!!")
			return []

		skillIdList = []
		skillIdList.append(heroInfo["skill_1"])
		skillIdList.append(heroInfo["skill_2"])
		skillIdList.append(heroInfo["skill_3"])
		skillIdList.append(heroInfo["skill_4"])

		if len(skillIdList) <= 0:
			DEBUG_MSG("Avatar_base_getSkillIdList:: skillIdList len <= 0!!!")
			return []

		skillList = []
		tableInfos = self.conf.getTable('d_skill.csv')
		for skillId in skillIdList:
			skillList.append(tableInfos.get(skillId, None))

		DEBUG_MSG("skillList.len [%i]" % len(skillList))

		return skillList

	def dealNonLocalLogin(self):
		'''
		处理异地登录
		'''
		# 推送当前匹配池中的所有的玩家匹配数据、当前玩家选择的英雄的相关信息和技能、self.gameState
		playersData = self.acquireAllPlayersMatchData()
		matchInfoLst = TMatchingInfosList()

		for playerEntityId in playersData.keys():
			matchInfo = TMatchingInfos()
			matchInfoLst[playerEntityId] = matchInfo.createFromDict(playersData[playerEntityId])

		DEBUG_MSG("Avatar_base_dealNonLocalLogin::playersData[%s], gameState[%i]" % (str(playersData), self.gameState))

		if self.cell is None:
			heroInfo = self.cellData["heroInfo"]
			skillInfosLst = self.cellData["skillInfosLst"]
		else:
			heroInfo = self.getHeroInfo(self.heroId)
			skillInfosLst = self.getSkillList(heroInfo)

		if self.client:
			self.client.onNonLocalLogin(matchInfoLst, heroInfo, skillInfosLst, self.gameState)

		# 玩家需要将帧数从0开始重新推送给客户端,为了确保玩家调整到battle界面并准备好,倒计数1秒后再调整帧数
		self.setAdjustFrameIdTimer()

	def dealDisconnect(self):
		'''
		处理断线重连==>情况：断线情况包括主动关闭客户端、客户端断线未在规定时间内登录
		'''
		DEBUG_MSG("Avatar_base_dealDisconnect::gameState[%i]" % (self.gameState))

		if self.gameState < GameConstants.GAMESTATE_MATCH_END:
			if self.gameState >= GameConstants.GAMESTATE_MATCHING:
				self.reqExitGame()
			self._destroyTimer = self.addTimer(GameConfigs.GAME_EXTEND_DESTORY_TIME, 0, TIMER_TYPE_DESTROY)

		self.disconnectFlag = True

	def dealReconnection(self):
		'''
		处理重连问题
		'''
		self.disconnectFlag = False

		if self.gameState < GameConstants.GAMESTATE_PLAYING and self.cell:
			# 表示游戏断线时处于游戏还未开始状态, 但重连时服务器已进入游戏中
			self.gameState = GameConstants.GAMESTATE_PLAYING
			self.client.onGameStateChanged(self.gameState)

			self.setAdjustFrameIdTimer()
		elif self.gameState == GameConstants.GAMESTATE_PLAYING:
			# 表示游戏断线时处于游戏进行状态
			# 通过客户端推上来的帧数,把当前帧数改为实际渲染帧数
			# 待处理
			pass

	def dealClientEnabled(self):
		'''
		处理客户端连接 如果当前玩家状态不处于登录状态，即需要推送当前状态给玩家
		'''
		if self.gameState != GameConstants.GAMESTATE_LOGIN:
			if self.disconnectFlag:
				# 处理断线重连
				self.dealReconnection()
			else:
				# 处理异地登录
				self.dealNonLocalLogin()
		else:
			# 客户端登录成功后会直接跳转到大厅
			self.gameState = GameConstants.GAMESTATE_HALL


	def transformMatchStateToGameState(self, matchState):
		# 当前匹配对象中的匹配状态
		# ID_MATCH_BEGIN = 0
		# ID_MATCHING    = 1
		# ID_MATCH_CREROOMRULE   = 2
		# ID_MATCH_END   = 3
		# ID_LOADING_TIME   = 4
		# ID_ROOM_CREATION_BEGIN       = 5
		# ID_ROOM_CREATION_COMPLETE    = 6
		state = GameConstants.GAMESTATE_HALL

		if matchState == 1:
			state = GameConstants.GAMESTATE_MATCHING
		elif matchState == 2:
			state = GameConstants.GAMESTATE_SELECT_HERO
		elif matchState == 3:
			state = GameConstants.GAMESTATE_MATCH_END
		elif matchState == 4:
			# 表示匹配成功后等待加载房间时段::ID_LOADING_TIME
			state = GameConstants.GAMESTATE_LOAD_TO_GAME
		elif matchState == 5:
			state = GameConstants.GAMESTATE_READY_GAME
		elif matchState == 6:
			state = GameConstants.GAMESTATE_PLAYING

		return state

	def setAdjustFrameIdTimer(self):
		# 玩家需要将帧数从0开始重新推送给客户端，为了确保玩家调整到battle界面并准备好,倒计数1秒后再调整帧数
		if self._adjustFrameIdTimer != 0:
			self.delTimer(self._adjustFrameIdTimer)
		if self.cell:
			self._adjustFrameIdTimer = self.addTimer(1, 0, TIMER_TYPE_ADJUST_FRAMEID)
