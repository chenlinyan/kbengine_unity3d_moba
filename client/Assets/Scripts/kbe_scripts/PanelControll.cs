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
        KBEngine.Event.registerOut("onPlayerHeroIdChanged", this, "onPlayerHeroIdChanged");

        KBEngine.Event.registerOut("onReadyBattle", this, "onReadyBattle");
        KBEngine.Event.registerOut("onLoadingToReadyBattleState", this, "onLoadingToReadyBattleState");
        KBEngine.Event.registerOut("onExitMatchMsg", this, "onExitMatchMsg");

        KBEngine.Event.registerOut("onKicked", this, "onKicked");

    }

    public void OnDestroy()
    {
        KBEngine.Event.deregisterOut(this);
    }

    //当前客户端被踢掉操作
    public void onKicked(UInt16 failedcode)
    {
        SceneManager.LoadScene("start");
        ActivePanel(PanelType.Login);
       //释放所有数据等等
        KBEngine.KBEngineApp.app.reset();
        Debug.LogError("onKicked_onKicked_onKicked::" + failedcode.ToString());
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
            KBEngine.Event.fireIn("reqJoinGame", (Byte)1);

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
            KBEngine.Event.fireIn("reqExitGame");
            Debug.Log("reqExitGamereqExitGamereqExitGamereqExitGame");
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

    public void onGameStateChanged(Int32 gameState)
    {
        //登录1, 大厅中2, 匹配中3, 选择英雄4, 匹配结束5, 进入游戏前等待6, 准备开始游戏7, 开始游戏8, 游戏中9, 游戏結束10, 统计结果11
        if (gameState == 3 || gameState == 4)
        {
            ActivePanel(PanelType.Match);
        }
        else if (gameState > 4 && gameState < 9)
        {
            ActivePanel(PanelType.Room);
            loadFlag = true; //loadFlag表示加载过程，其中所有的按钮都不能操作
        }
        else if (gameState == 9)
        {
            SceneManager.LoadScene("Battlefield");
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
