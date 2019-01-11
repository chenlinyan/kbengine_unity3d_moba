namespace KBEngine
{
    using UnityEngine;
    using System;
    using System.Collections;
    using System.Collections.Generic;
    using System.Linq;


    public class Avatar : AvatarBase
    {
        public Dictionary<Int32, MATCHING_INFOS> matchInfosDict = new Dictionary<Int32, MATCHING_INFOS>();
        public Avatar()
        {
            KBEngine.Event.registerOut("onKicked", this, "onKicked");
        }

        public override void __init__()
        {
            // 触发登陆成功事件
            Event.fireOut("onLoginSuccessfully", new object[] { KBEngineApp.app.entity_uuid, id, this });

            KBEngine.Event.registerIn("reqJoinGame", this, "reqJoinGame");
            KBEngine.Event.registerIn("reqExitGame", this, "reqExitGame");
            KBEngine.Event.registerIn("reqHeroInfoByHeroId", this, "reqHeroInfoByHeroId");
            //KBEngine.Event.registerIn("reqSkillLst", this, "reqSkillLst");

        }

        public void reqJoinGame(Byte ready)
        {
            baseEntityCall.reqJoinGame();
        }
        public void reqExitGame()
        {
            baseEntityCall.reqExitGame();
        }

        public void reqHeroInfoByHeroId(int heroId)
        {
            baseEntityCall.reqHeroInfosByHeroId(heroId);
        }

        //public void reqSkillLst()
        //{
        //    baseEntityCall.reqSkillLst();
        //}

      
        public override void onDestroy()
        {

        }
        public override void onJoinGameResult(Byte flag)
        {
            if (flag > 0)
            {
                onGameStateChanged(4);
            }
        }
        public override void onExitGameResult(Byte flag)
        {

        }

        public override void onHeroIdChanged(Int32 entityId, Int32 heroId)
        {
            if (matchInfosDict.ContainsKey(entityId))
            {
                matchInfosDict[entityId].heroId = heroId;
                Debug.Log("onHeroIdChanged_onHeroIdChanged_onHeroIdChanged_onHeroIdChanged___" + heroId);
                Event.fireOut("onPlayerHeroIdChanged", new object[] { entityId, heroId });
            }
            else
            {
                Debug.Log("onHeroIdChanged_no_key::entityId_" + entityId);
                Dictionary<Int32, MATCHING_INFOS>.KeyCollection keyColl = matchInfosDict.Keys;
                foreach(Int32 num in keyColl)
                {
                    Debug.Log("onHeroIdChanged_exit_key::entityId_" + num);
                }
            }
        }

        public override void onPushMatchPlayersData(MATCHING_INFOS_LIST infos)
        {
            for (int i = 0; i < infos.values.Count; i++)
            {
                MATCHING_INFOS info = infos.values[i];
                Debug.Log("i::" + i + "info.id:::" + info.id);
                matchInfosDict[info.id] = info;
            }
            Debug.Log("matchInfosDict::::count" + matchInfosDict.Count + ",infos::::count:::" + infos.values.Count);
        }

        public override void onPushStatisticalResult(Int32 arg1)
        {
        }
        public override void onReqsChooseHeroResult(HERO_INFOS heroInfos, SKILL_INFOS_LIST skillLst)
        {
            Debug.Log("onReqsChooseHeroResult::" + heroInfos.name + "," + heroInfos.id + "," + heroInfos.skill_3 + ",onReqsSkillLstResult::" + skillLst.Count);
            for (int i = 0; i < skillLst.Count; i++)
            {
                Debug.Log("skillId[" + skillLst[i].id + "]" + ",name::" + skillLst[i].name + ",other::" + skillLst[i].skill_ap_growth);
            }
        }

        //public override void onReqsSkillLstResult(SKILL_INFOS_LIST skillLst)
        //{
        //    Debug.Log("onReqsSkillLstResult::" + skillLst.Count);
        //    for (int i = 0; i < skillLst.Count; i++)
        //    {
        //        Debug.Log("skillId[" + skillLst[i].id + "]" + ",name::" + skillLst[i].name + ",other::" + skillLst[i].skill_ap_growth);
        //    }
        //}

        public override void onNameChanged(string old)
        {
            //Debug.Log(className + "::set_name: " + old + " => " + v); 
            Event.fireOut("set_name", new object[] { this, this.name });
        }


        public override void onReadyBattle()
        {
            Event.fireOut("onReadyBattle", new object[] { });
        }

        public override void onLoadingToReadyBattleState()
        {
            Event.fireOut("onLoadingToReadyBattleState", new object[] { });
        }

        public override void onExitMatch(Int32 entityId)
        {
            Debug.Log("entityId::" + entityId + ",baseEntityCall.id::" + baseEntityCall.id + ",matchInfosDict::" + matchInfosDict.Count);
            if (matchInfosDict.ContainsKey(entityId))
            {
                bool oneSelfFlag = false;
                if (entityId == baseEntityCall.id)
                {   //删除之前保存的字典数据，并请求退出游戏
                    matchInfosDict.Clear();
                    oneSelfFlag = true;

                }
                else
                {
                    matchInfosDict.Remove(entityId);
                }
                Debug.Log("entityId::" + entityId + ",oneSelfFlag::" + oneSelfFlag);
                Event.fireOut("onExitMatchMsg", new object[] { entityId, oneSelfFlag });
            }
            else
            {
                Dictionary<Int32, MATCHING_INFOS>.KeyCollection keyColl = matchInfosDict.Keys;
                foreach (Int32 num in keyColl)
                {

                    Debug.Log("onExitMatch_exit_key::entityId_" + num);
                }

            }
        }

        /// <summary>
        /// 异地登录处理后推送的信息
        /// </summary>
        /// <param name="infos"></param>
        /// <param name="heroInfos"></param>
        /// <param name="skillLst"></param>
        /// <param name="gameState"></param>
        public override void onNonLocalLogin(MATCHING_INFOS_LIST infos, HERO_INFOS heroInfos, SKILL_INFOS_LIST skillLst, Int32 gameState)
        {
            onPushMatchPlayersData(infos);
            onReqsChooseHeroResult(heroInfos,skillLst);
            onGameStateChanged(gameState);
            Debug.Log("gameState" + gameState);
        }

        public override void onGameStateChanged(Int32 gameState)
        {
            Event.fireOut("onGameStateChanged", new object[] { gameState });
        }
        //当前客户端被踢掉操作
        public void onKicked(UInt16 failedcode)
        { 
            //释放所有数据等等
            matchInfosDict.Clear();
        }

    }
}
