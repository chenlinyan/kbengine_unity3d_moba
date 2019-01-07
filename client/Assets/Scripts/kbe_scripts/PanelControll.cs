using KBEngine;
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class PanelControll : MonoBehaviour {

    public enum PanelType { Info, Login, Match, Room, Chat};

    [Header("Login Panel")]
    public GameObject loginPanel;
    public Text accountText;
    public Text passwdText;
    public Button loginBtn;

    [Header("Match Panel")]
    public GameObject matchPanel;


    [Header("Room Panel")]
    public GameObject roomPanel;
    public Transform[] playerBoxes;

    [Header("Chat Panel")]
    public GameObject chatPanel;
    public Text chatText;
    public InputField chatInput;
    private ScrollRect chatScroll;

    [Header("Info Panel")]
    public GameObject infoPanel;

    bool loadFlag = false;
    private void InitEvent()
    {
       
        KBEngine.Event.registerOut("onLoginFailed", this, "onLoginFailed");
        KBEngine.Event.registerOut("onLoginSuccessfully", this, "onLoginSuccessfully");

        KBEngine.Event.registerOut("onAvatarEnterWorld", this, "onAvatarEnterWorld");
        KBEngine.Event.registerOut("onAvatarLeaveWorld", this, "onAvatarLeaveWorld");

        KBEngine.Event.registerOut("readyResult", this, "readyResult");

        KBEngine.Event.registerOut("onGameStateChanged", this, "onGameStateChanged");
        KBEngine.Event.registerOut("onChangeLoadScene", this, "onChangeLoadScene");
        KBEngine.Event.registerOut("onPlayerHeroIdChanged", this, "onPlayerHeroIdChanged");

        KBEngine.Event.registerOut("onReadyBattle", this, "onReadyBattle");
        KBEngine.Event.registerOut("onLoadingToReadyBattleState", this, "onLoadingToReadyBattleState");
        KBEngine.Event.registerOut("onExitMatchMsg", this, "onExitMatchMsg");

    }

    public void OnDestroy()
    {
        KBEngine.Event.deregisterOut(this);
    }


    private void ShowTips(Vector2 postion, string tip)
    {
        if (!infoPanel.activeSelf)
        {
            infoPanel.SetActive(true);
        }

        RectTransform Rect = infoPanel.GetComponent<RectTransform>();
        Rect.localPosition = postion;
        Text text = infoPanel.GetComponent<Text>();
        text.text = tip;
    }

    public void OnLoginClick()
    {

        //用户名密码为空
        if (accountText.text == "" || passwdText.text == "")
        {
            ShowTips(new Vector2(10.2f,228), "用户名密码不能为空!");
            return;
        }
        //连接服务器

        KBEngine.Event.fireIn("login", accountText.text, passwdText.text, System.Text.Encoding.UTF8.GetBytes("kbegine_moba_demo"));
    }

    public void OnStarClick()
    {
        if (!loadFlag)
            KBEngine.Event.fireIn("reqReady", (Byte)1);

    }

    public void OnChooseHeroClick()
    {
        if (!loadFlag)
        {
            KBEngine.Event.fireIn("reqHeroInfoByHeroId", 10001);
            Debug.Log("OnChooseHeroClickOnChooseHeroClickOnChooseHeroClick");
        }
    }

    public void onExitMatchClick()
    {
        if (!loadFlag)
        {
            KBEngine.Event.fireIn("reqExitMatch");
            Debug.Log("reqExitMatchreqExitMatchreqExitMatchreqExitMatch");
        }

    }

    public void OnGetSkillListClick()
    {
        if (!loadFlag)
            KBEngine.Event.fireIn("reqSkillLst");
        Debug.Log("OnGetSkillListClickOnGetSkillListClickOnGetSkillListClick");
    }


    #region  引擎返回信息推送

    public void onLoginFailed(UInt16 failedcode)
    {
        if (failedcode == 20)
        {
            ShowTips(new Vector2(10.2f, 228), "login is failed(登陆失败), err=" + KBEngineApp.app.serverErr(failedcode) + ", " + System.Text.Encoding.ASCII.GetString(KBEngineApp.app.serverdatas()));
        }
        else
        {
            ShowTips(new Vector2(10.2f, 228), "login is failed(登陆失败), err=" + KBEngineApp.app.serverErr(failedcode));
        }
    }

    public void onLoginSuccessfully(UInt64 rndUUID, Int32 eid, KBEngine.Avatar accountEntity)
    {
        Debug.Log("accountText.text:" + accountText.text);
        ShowTips(new Vector2(10.2f, 228), "Welcome "+ accountText.text);

        ActivePanel(PanelType.Room);
    }

    public void onGameStateChanged(SByte gameState)
    {
        //游戏状态::  登录1, 大厅中2, 等待匹配3, 匹配中4, 匹配结束5, 
        //选择英雄6, 准备进入游戏7, 开始游戏8, 游戏中9, 游戏結束10, 统计结果11
        if (gameState == 6) //选择英雄
        {
            ActivePanel(PanelType.Match);
        }
        else if (gameState == 7)// 准备进入游戏
        {

        }
        else if (gameState == 8)//开始游戏
        {
            SceneManager.LoadScene("Battlefield");
        }
    }

    public void onChangeLoadScene(int gameState)
    {
        //选择英雄1, 准备进入游戏2, 开始游戏3, 游戏中4, 游戏結束5, 统计结果5
        if (gameState == 1)
        {
            ActivePanel(PanelType.Match);
        }
         
    }

    /// <summary>
    /// 推送玩家改变英雄Id的消息
    /// </summary>
    /// <param name="entityId"></param>
    /// <param name="heroId"></param>
    public void onPlayerHeroIdChanged(Int32 entityId, Int32 heroId)
    {
        Debug.Log("onPlayerHeroIdChanged__entityId:::" + entityId + ", heroId:: " + heroId);
    }

    /// <summary>
    /// 游戏进入等待加载状态
    /// </summary>
    public void onLoadingToReadyBattleState()
    {
        loadFlag = true;
    }
    /// <summary>
    /// 开始游戏，跳转界面
    /// </summary>
    public void onReadyBattle()
    {
        SceneManager.LoadScene("Battlefield");
    }

    public void onExitMatchMsg(Int32 entityId, bool oneSelfFlag)
    {
        //处理界面上退出的玩家信息
        if (oneSelfFlag)
        {
            ActivePanel(PanelType.Room);
        }
        else
        {
            //处理非当前玩家界面对退出的玩家的信息处理
        }

    }

    #endregion
    private void ClearPlayersGUI()
    {
        foreach (Transform playerBox in playerBoxes)
        {
            playerBox.GetComponent<Image>().enabled = false;
            playerBox.Find("PlayerNameText").GetComponent<Text>().text = "";
        }
    }

    public void UpdatePlayerList()
    {
        ClearPlayersGUI();

        for (int index = 0; index < SpaceData.Instance.SpacePlayers.Count; index++)
        {
            KBEngine.Avatar player = SpaceData.Instance.SpacePlayers[index].owner as KBEngine.Avatar;

            Transform playerBox = playerBoxes[index];

            playerBox.GetComponent<Image>().enabled = true;

            Text playerNameText = playerBox.Find("PlayerNameText").GetComponent<Text>();

            playerNameText.text = player.name.Trim();
        }
    }

    public void readyResult(byte result)
    {
        if(result == 0)
        {
            SceneManager.LoadScene("Battlefield");
        }
    }

    public void onAvatarEnterWorld()
    {
        UpdatePlayerList();
    }

    public void onAvatarLeaveWorld()
    {
        UpdatePlayerList();
    }
    private void ActivePanel(PanelType panelType)
    {
        loginPanel.SetActive(panelType == PanelType.Login);
        matchPanel.SetActive(panelType == PanelType.Match);
        roomPanel.SetActive(panelType == PanelType.Room);
        chatPanel.SetActive(panelType == PanelType.Chat);
        
    }

    private void Awake()
    {
        Debug.Log("awake_awake_awake_awake_awake");
    }

    // Use this for initialization
    void Start ()
    {
        Debug.Log("initinitinitintnint");
        InitEvent();

        ActivePanel(PanelType.Login);
    }
	
	// Update is called once per frame
	void Update () {
		
	}


}
