/*
	Generated by KBEngine!
	Please do not modify this file!
	
	tools = kbcmd
*/

namespace KBEngine
{
	using UnityEngine;
	using System;
	using System.Collections;
	using System.Collections.Generic;

	// defined in */scripts/entity_defs/MatchAvatarReport.def
	public class EntityBaseEntityCall_MatchAvatarReportBase : EntityCall
	{
		public UInt16 entityComponentPropertyID = 0;

		public EntityBaseEntityCall_MatchAvatarReportBase(UInt16 ecpID, Int32 eid) : base(eid, "MatchAvatarReport")
		{
			entityComponentPropertyID = ecpID;
			type = ENTITYCALL_TYPE.ENTITYCALL_TYPE_BASE;
		}

	}

	public class EntityCellEntityCall_MatchAvatarReportBase : EntityCall
	{
		public UInt16 entityComponentPropertyID = 0;

		public EntityCellEntityCall_MatchAvatarReportBase(UInt16 ecpID, Int32 eid) : base(eid, "MatchAvatarReport")
		{
			entityComponentPropertyID = ecpID;
			className = "MatchAvatarReport";
			type = ENTITYCALL_TYPE.ENTITYCALL_TYPE_CELL;
		}

	}
	}