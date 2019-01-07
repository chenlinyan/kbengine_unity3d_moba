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
            
        }

        public override void __init__()
        {
            // 触发登陆成功事件
            Event.fireOut("onLoginSuccessfully", new object[] { KBEngineApp.app.entity_uuid, id, this });

            KBEngine.Event.registerIn("reqReady", this, "startGame");
            KBEngine.Event.registerIn("reqHeroInfoByHeroId", this, "reqHeroInfoByHeroId");
            KBEngine.Event.registerIn("reqSkillLst", this, "reqSkillLst");
            KBEngine.Event.registerIn("reqExitMatch", this, "reqExitMatch");

        }

        public void startGame(Byte ready)
        {
            baseEntityCall.startGame();
        }

        public void reqHeroInfoByHeroId(int heroId)
        {
            baseEntityCall.reqHeroInfosByHeroId(heroId);
        }

        public void reqSkillLst()
        {
            baseEntityCall.reqSkillLst();
        }

        public void reqExitMatch()
        {
            baseEntityCall.reqExitMatch();
        }
        public override void onDestroy()
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
            if (matchInfosDict.Count > 0)
            {
                Event.fireOut("onChangeLoadScene", new object[] {1});
            }
        }

        public override void onPushAvatarCurrentScene(UInt32 arg1)
        {
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

        public override void onReqsSkillLstResult(SKILL_INFOS_LIST skillLst)
        {
            Debug.Log("onReqsSkillLstResult::" + skillLst.Count);
            for (int i = 0; i < skillLst.Count; i++)
            {
                Debug.Log("skillId[" + skillLst[i].id + "]" + ",name::" + skillLst[i].name + ",other::" + skillLst[i].skill_ap_growth);
            }
        }

        public override void onNameChanged(string old)
        {
            //Debug.Log(className + "::set_name: " + old + " => " + v); 
            Event.fireOut("set_name", new object[] { this, this.name });
        }

        //public override void onTeamIDChanged(SByte old)
        //{
        //    Debug.Log(className + "::set_name: " + old + " => " + teamID);
        //    Event.fireOut("set_teamID", new object[] { this, this.teamID });
        //}
        //public override void onGameStateCChanged(SByte oldValue)
        //{
        //    //游戏状态::  登录1, 大厅中2, 等待匹配3, 匹配中4, 匹配结束5, 
        //    //选择英雄6, 准备进入游戏7, 开始游戏8, 游戏中9, 游戏結束10, 统计结果11
        //    Event.fireOut("onGameStateChanged", new object[] {this.gameStateC}); 
        //}

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
    }
}
