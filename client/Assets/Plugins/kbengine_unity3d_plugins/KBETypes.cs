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



	// defined in */scripts/entity_defs/types.xml

	public struct UINT8
	{
		Byte value;

		UINT8(Byte value)
		{
			this.value = value;
		}

		public static implicit operator Byte(UINT8 value)
		{
			return value.value;
		}

		public static implicit operator UINT8(Byte value)
		{
			Byte tvalue = (Byte)value;
			return new UINT8(tvalue);
		}

		public static Byte MaxValue
		{
			get
			{
				return Byte.MaxValue;
			}
		}

		public static Byte MinValue
		{
			get
			{
				return Byte.MinValue;
			}
		}
	}

	public struct UINT16
	{
		UInt16 value;

		UINT16(UInt16 value)
		{
			this.value = value;
		}

		public static implicit operator UInt16(UINT16 value)
		{
			return value.value;
		}

		public static implicit operator UINT16(UInt16 value)
		{
			UInt16 tvalue = (UInt16)value;
			return new UINT16(tvalue);
		}

		public static UInt16 MaxValue
		{
			get
			{
				return UInt16.MaxValue;
			}
		}

		public static UInt16 MinValue
		{
			get
			{
				return UInt16.MinValue;
			}
		}
	}

	public struct UINT64
	{
		UInt64 value;

		UINT64(UInt64 value)
		{
			this.value = value;
		}

		public static implicit operator UInt64(UINT64 value)
		{
			return value.value;
		}

		public static implicit operator UINT64(UInt64 value)
		{
			UInt64 tvalue = (UInt64)value;
			return new UINT64(tvalue);
		}

		public static UInt64 MaxValue
		{
			get
			{
				return UInt64.MaxValue;
			}
		}

		public static UInt64 MinValue
		{
			get
			{
				return UInt64.MinValue;
			}
		}
	}

	public struct UINT32
	{
		UInt32 value;

		UINT32(UInt32 value)
		{
			this.value = value;
		}

		public static implicit operator UInt32(UINT32 value)
		{
			return value.value;
		}

		public static implicit operator UINT32(UInt32 value)
		{
			UInt32 tvalue = (UInt32)value;
			return new UINT32(tvalue);
		}

		public static UInt32 MaxValue
		{
			get
			{
				return UInt32.MaxValue;
			}
		}

		public static UInt32 MinValue
		{
			get
			{
				return UInt32.MinValue;
			}
		}
	}

	public struct INT8
	{
		SByte value;

		INT8(SByte value)
		{
			this.value = value;
		}

		public static implicit operator SByte(INT8 value)
		{
			return value.value;
		}

		public static implicit operator INT8(SByte value)
		{
			SByte tvalue = (SByte)value;
			return new INT8(tvalue);
		}

		public static SByte MaxValue
		{
			get
			{
				return SByte.MaxValue;
			}
		}

		public static SByte MinValue
		{
			get
			{
				return SByte.MinValue;
			}
		}
	}

	public struct INT16
	{
		Int16 value;

		INT16(Int16 value)
		{
			this.value = value;
		}

		public static implicit operator Int16(INT16 value)
		{
			return value.value;
		}

		public static implicit operator INT16(Int16 value)
		{
			Int16 tvalue = (Int16)value;
			return new INT16(tvalue);
		}

		public static Int16 MaxValue
		{
			get
			{
				return Int16.MaxValue;
			}
		}

		public static Int16 MinValue
		{
			get
			{
				return Int16.MinValue;
			}
		}
	}

	public struct INT32
	{
		Int32 value;

		INT32(Int32 value)
		{
			this.value = value;
		}

		public static implicit operator Int32(INT32 value)
		{
			return value.value;
		}

		public static implicit operator INT32(Int32 value)
		{
			Int32 tvalue = (Int32)value;
			return new INT32(tvalue);
		}

		public static Int32 MaxValue
		{
			get
			{
				return Int32.MaxValue;
			}
		}

		public static Int32 MinValue
		{
			get
			{
				return Int32.MinValue;
			}
		}
	}

	public struct INT64
	{
		Int64 value;

		INT64(Int64 value)
		{
			this.value = value;
		}

		public static implicit operator Int64(INT64 value)
		{
			return value.value;
		}

		public static implicit operator INT64(Int64 value)
		{
			Int64 tvalue = (Int64)value;
			return new INT64(tvalue);
		}

		public static Int64 MaxValue
		{
			get
			{
				return Int64.MaxValue;
			}
		}

		public static Int64 MinValue
		{
			get
			{
				return Int64.MinValue;
			}
		}
	}

	public struct STRING
	{
		string value;

		STRING(string value)
		{
			this.value = value;
		}

		public static implicit operator string(STRING value)
		{
			return value.value;
		}

		public static implicit operator STRING(string value)
		{
			string tvalue = (string)value;
			return new STRING(tvalue);
		}
	}

	public struct UNICODE
	{
		string value;

		UNICODE(string value)
		{
			this.value = value;
		}

		public static implicit operator string(UNICODE value)
		{
			return value.value;
		}

		public static implicit operator UNICODE(string value)
		{
			string tvalue = (string)value;
			return new UNICODE(tvalue);
		}
	}

	public struct FLOAT
	{
		float value;

		FLOAT(float value)
		{
			this.value = value;
		}

		public static implicit operator float(FLOAT value)
		{
			return value.value;
		}

		public static implicit operator FLOAT(float value)
		{
			float tvalue = (float)value;
			return new FLOAT(tvalue);
		}

		public static float MaxValue
		{
			get
			{
				return float.MaxValue;
			}
		}

		public static float MinValue
		{
			get
			{
				return float.MinValue;
			}
		}
	}

	public struct DOUBLE
	{
		double value;

		DOUBLE(double value)
		{
			this.value = value;
		}

		public static implicit operator double(DOUBLE value)
		{
			return value.value;
		}

		public static implicit operator DOUBLE(double value)
		{
			double tvalue = (double)value;
			return new DOUBLE(tvalue);
		}

		public static double MaxValue
		{
			get
			{
				return double.MaxValue;
			}
		}

		public static double MinValue
		{
			get
			{
				return double.MinValue;
			}
		}
	}

	public struct PYTHON
	{
		byte[] value;

		PYTHON(byte[] value)
		{
			this.value = value;
		}

		public static implicit operator byte[](PYTHON value)
		{
			return value.value;
		}

		public static implicit operator PYTHON(byte[] value)
		{
			byte[] tvalue = (byte[])value;
			return new PYTHON(tvalue);
		}

		public Byte this[int ID]
		{
			get { return value[ID]; }
			set { this.value[ID] = value; }
		}
	}

	public struct PY_DICT
	{
		byte[] value;

		PY_DICT(byte[] value)
		{
			this.value = value;
		}

		public static implicit operator byte[](PY_DICT value)
		{
			return value.value;
		}

		public static implicit operator PY_DICT(byte[] value)
		{
			byte[] tvalue = (byte[])value;
			return new PY_DICT(tvalue);
		}

		public Byte this[int ID]
		{
			get { return value[ID]; }
			set { this.value[ID] = value; }
		}
	}

	public struct PY_TUPLE
	{
		byte[] value;

		PY_TUPLE(byte[] value)
		{
			this.value = value;
		}

		public static implicit operator byte[](PY_TUPLE value)
		{
			return value.value;
		}

		public static implicit operator PY_TUPLE(byte[] value)
		{
			byte[] tvalue = (byte[])value;
			return new PY_TUPLE(tvalue);
		}

		public Byte this[int ID]
		{
			get { return value[ID]; }
			set { this.value[ID] = value; }
		}
	}

	public struct PY_LIST
	{
		byte[] value;

		PY_LIST(byte[] value)
		{
			this.value = value;
		}

		public static implicit operator byte[](PY_LIST value)
		{
			return value.value;
		}

		public static implicit operator PY_LIST(byte[] value)
		{
			byte[] tvalue = (byte[])value;
			return new PY_LIST(tvalue);
		}

		public Byte this[int ID]
		{
			get { return value[ID]; }
			set { this.value[ID] = value; }
		}
	}

	public struct ENTITYCALL
	{
		byte[] value;

		ENTITYCALL(byte[] value)
		{
			this.value = value;
		}

		public static implicit operator byte[](ENTITYCALL value)
		{
			return value.value;
		}

		public static implicit operator ENTITYCALL(byte[] value)
		{
			byte[] tvalue = (byte[])value;
			return new ENTITYCALL(tvalue);
		}

		public Byte this[int ID]
		{
			get { return value[ID]; }
			set { this.value[ID] = value; }
		}
	}

	public struct BLOB
	{
		byte[] value;

		BLOB(byte[] value)
		{
			this.value = value;
		}

		public static implicit operator byte[](BLOB value)
		{
			return value.value;
		}

		public static implicit operator BLOB(byte[] value)
		{
			byte[] tvalue = (byte[])value;
			return new BLOB(tvalue);
		}

		public Byte this[int ID]
		{
			get { return value[ID]; }
			set { this.value[ID] = value; }
		}
	}

	public struct VECTOR2
	{
		Vector2 value;

		VECTOR2(Vector2 value)
		{
			this.value = value;
		}

		public static implicit operator Vector2(VECTOR2 value)
		{
			return value.value;
		}

		public static implicit operator VECTOR2(Vector2 value)
		{
			Vector2 tvalue = (Vector2)value;
			return new VECTOR2(tvalue);
		}

		public float x
		{
			get { return value.x; }
			set { this.value.x = value; }
		}

		public float y
		{
			get { return value.y; }
			set { this.value.y = value; }
		}

	}

	public struct VECTOR3
	{
		Vector3 value;

		VECTOR3(Vector3 value)
		{
			this.value = value;
		}

		public static implicit operator Vector3(VECTOR3 value)
		{
			return value.value;
		}

		public static implicit operator VECTOR3(Vector3 value)
		{
			Vector3 tvalue = (Vector3)value;
			return new VECTOR3(tvalue);
		}

		public float x
		{
			get { return value.x; }
			set { this.value.x = value; }
		}

		public float y
		{
			get { return value.y; }
			set { this.value.y = value; }
		}

		public float z
		{
			get { return value.z; }
			set { this.value.z = value; }
		}

	}

	public struct VECTOR4
	{
		Vector4 value;

		VECTOR4(Vector4 value)
		{
			this.value = value;
		}

		public static implicit operator Vector4(VECTOR4 value)
		{
			return value.value;
		}

		public static implicit operator VECTOR4(Vector4 value)
		{
			Vector4 tvalue = (Vector4)value;
			return new VECTOR4(tvalue);
		}

		public float x
		{
			get { return value.x; }
			set { this.value.x = value; }
		}

		public float y
		{
			get { return value.y; }
			set { this.value.y = value; }
		}

		public float z
		{
			get { return value.z; }
			set { this.value.z = value; }
		}

		public float w
		{
			get { return value.w; }
			set { this.value.w = value; }
		}
	}

	public struct OBJECT_ID
	{
		Int32 value;

		OBJECT_ID(Int32 value)
		{
			this.value = value;
		}

		public static implicit operator Int32(OBJECT_ID value)
		{
			return value.value;
		}

		public static implicit operator OBJECT_ID(Int32 value)
		{
			Int32 tvalue = (Int32)value;
			return new OBJECT_ID(tvalue);
		}

		public static Int32 MaxValue
		{
			get
			{
				return Int32.MaxValue;
			}
		}

		public static Int32 MinValue
		{
			get
			{
				return Int32.MinValue;
			}
		}
	}

	public struct BOOL
	{
		Byte value;

		BOOL(Byte value)
		{
			this.value = value;
		}

		public static implicit operator Byte(BOOL value)
		{
			return value.value;
		}

		public static implicit operator BOOL(Byte value)
		{
			Byte tvalue = (Byte)value;
			return new BOOL(tvalue);
		}

		public static Byte MaxValue
		{
			get
			{
				return Byte.MaxValue;
			}
		}

		public static Byte MinValue
		{
			get
			{
				return Byte.MinValue;
			}
		}
	}

	public struct DBID
	{
		UInt64 value;

		DBID(UInt64 value)
		{
			this.value = value;
		}

		public static implicit operator UInt64(DBID value)
		{
			return value.value;
		}

		public static implicit operator DBID(UInt64 value)
		{
			UInt64 tvalue = (UInt64)value;
			return new DBID(tvalue);
		}

		public static UInt64 MaxValue
		{
			get
			{
				return UInt64.MaxValue;
			}
		}

		public static UInt64 MinValue
		{
			get
			{
				return UInt64.MinValue;
			}
		}
	}

	public struct UID
	{
		UInt64 value;

		UID(UInt64 value)
		{
			this.value = value;
		}

		public static implicit operator UInt64(UID value)
		{
			return value.value;
		}

		public static implicit operator UID(UInt64 value)
		{
			UInt64 tvalue = (UInt64)value;
			return new UID(tvalue);
		}

		public static UInt64 MaxValue
		{
			get
			{
				return UInt64.MaxValue;
			}
		}

		public static UInt64 MinValue
		{
			get
			{
				return UInt64.MinValue;
			}
		}
	}

	public struct ENTITY_ID
	{
		Int32 value;

		ENTITY_ID(Int32 value)
		{
			this.value = value;
		}

		public static implicit operator Int32(ENTITY_ID value)
		{
			return value.value;
		}

		public static implicit operator ENTITY_ID(Int32 value)
		{
			Int32 tvalue = (Int32)value;
			return new ENTITY_ID(tvalue);
		}

		public static Int32 MaxValue
		{
			get
			{
				return Int32.MaxValue;
			}
		}

		public static Int32 MinValue
		{
			get
			{
				return Int32.MinValue;
			}
		}
	}

	public struct ROLE_ID
	{
		Byte value;

		ROLE_ID(Byte value)
		{
			this.value = value;
		}

		public static implicit operator Byte(ROLE_ID value)
		{
			return value.value;
		}

		public static implicit operator ROLE_ID(Byte value)
		{
			Byte tvalue = (Byte)value;
			return new ROLE_ID(tvalue);
		}

		public static Byte MaxValue
		{
			get
			{
				return Byte.MaxValue;
			}
		}

		public static Byte MinValue
		{
			get
			{
				return Byte.MinValue;
			}
		}
	}

	public struct WEAPON_ID
	{
		Int32 value;

		WEAPON_ID(Int32 value)
		{
			this.value = value;
		}

		public static implicit operator Int32(WEAPON_ID value)
		{
			return value.value;
		}

		public static implicit operator WEAPON_ID(Int32 value)
		{
			Int32 tvalue = (Int32)value;
			return new WEAPON_ID(tvalue);
		}

		public static Int32 MaxValue
		{
			get
			{
				return Int32.MaxValue;
			}
		}

		public static Int32 MinValue
		{
			get
			{
				return Int32.MinValue;
			}
		}
	}

	public struct NAME
	{
		string value;

		NAME(string value)
		{
			this.value = value;
		}

		public static implicit operator string(NAME value)
		{
			return value.value;
		}

		public static implicit operator NAME(string value)
		{
			string tvalue = (string)value;
			return new NAME(tvalue);
		}
	}

	public struct TEAM_ID
	{
		Int32 value;

		TEAM_ID(Int32 value)
		{
			this.value = value;
		}

		public static implicit operator Int32(TEAM_ID value)
		{
			return value.value;
		}

		public static implicit operator TEAM_ID(Int32 value)
		{
			Int32 tvalue = (Int32)value;
			return new TEAM_ID(tvalue);
		}

		public static Int32 MaxValue
		{
			get
			{
				return Int32.MaxValue;
			}
		}

		public static Int32 MinValue
		{
			get
			{
				return Int32.MinValue;
			}
		}
	}

	public struct HERO_ID
	{
		Int32 value;

		HERO_ID(Int32 value)
		{
			this.value = value;
		}

		public static implicit operator Int32(HERO_ID value)
		{
			return value.value;
		}

		public static implicit operator HERO_ID(Int32 value)
		{
			Int32 tvalue = (Int32)value;
			return new HERO_ID(tvalue);
		}

		public static Int32 MaxValue
		{
			get
			{
				return Int32.MaxValue;
			}
		}

		public static Int32 MinValue
		{
			get
			{
				return Int32.MinValue;
			}
		}
	}

	public struct SPACE_ID
	{
		UInt32 value;

		SPACE_ID(UInt32 value)
		{
			this.value = value;
		}

		public static implicit operator UInt32(SPACE_ID value)
		{
			return value.value;
		}

		public static implicit operator SPACE_ID(UInt32 value)
		{
			UInt32 tvalue = (UInt32)value;
			return new SPACE_ID(tvalue);
		}

		public static UInt32 MaxValue
		{
			get
			{
				return UInt32.MaxValue;
			}
		}

		public static UInt32 MinValue
		{
			get
			{
				return UInt32.MinValue;
			}
		}
	}

	public struct ROOMPOSITION_ID
	{
		UInt32 value;

		ROOMPOSITION_ID(UInt32 value)
		{
			this.value = value;
		}

		public static implicit operator UInt32(ROOMPOSITION_ID value)
		{
			return value.value;
		}

		public static implicit operator ROOMPOSITION_ID(UInt32 value)
		{
			UInt32 tvalue = (UInt32)value;
			return new ROOMPOSITION_ID(tvalue);
		}

		public static UInt32 MaxValue
		{
			get
			{
				return UInt32.MaxValue;
			}
		}

		public static UInt32 MinValue
		{
			get
			{
				return UInt32.MinValue;
			}
		}
	}

	public struct POSITION3D
	{
		Vector3 value;

		POSITION3D(Vector3 value)
		{
			this.value = value;
		}

		public static implicit operator Vector3(POSITION3D value)
		{
			return value.value;
		}

		public static implicit operator POSITION3D(Vector3 value)
		{
			Vector3 tvalue = (Vector3)value;
			return new POSITION3D(tvalue);
		}

		public float x
		{
			get { return value.x; }
			set { this.value.x = value; }
		}

		public float y
		{
			get { return value.y; }
			set { this.value.y = value; }
		}

		public float z
		{
			get { return value.z; }
			set { this.value.z = value; }
		}

	}

	public struct DIRECTION3D
	{
		Vector3 value;

		DIRECTION3D(Vector3 value)
		{
			this.value = value;
		}

		public static implicit operator Vector3(DIRECTION3D value)
		{
			return value.value;
		}

		public static implicit operator DIRECTION3D(Vector3 value)
		{
			Vector3 tvalue = (Vector3)value;
			return new DIRECTION3D(tvalue);
		}

		public float x
		{
			get { return value.x; }
			set { this.value.x = value; }
		}

		public float y
		{
			get { return value.y; }
			set { this.value.y = value; }
		}

		public float z
		{
			get { return value.z; }
			set { this.value.z = value; }
		}

	}

	public struct SPACE_KEY
	{
		UInt64 value;

		SPACE_KEY(UInt64 value)
		{
			this.value = value;
		}

		public static implicit operator UInt64(SPACE_KEY value)
		{
			return value.value;
		}

		public static implicit operator SPACE_KEY(UInt64 value)
		{
			UInt64 tvalue = (UInt64)value;
			return new SPACE_KEY(tvalue);
		}

		public static UInt64 MaxValue
		{
			get
			{
				return UInt64.MaxValue;
			}
		}

		public static UInt64 MinValue
		{
			get
			{
				return UInt64.MinValue;
			}
		}
	}

	public struct ROOMSTATE
	{
		Int32 value;

		ROOMSTATE(Int32 value)
		{
			this.value = value;
		}

		public static implicit operator Int32(ROOMSTATE value)
		{
			return value.value;
		}

		public static implicit operator ROOMSTATE(Int32 value)
		{
			Int32 tvalue = (Int32)value;
			return new ROOMSTATE(tvalue);
		}

		public static Int32 MaxValue
		{
			get
			{
				return Int32.MaxValue;
			}
		}

		public static Int32 MinValue
		{
			get
			{
				return Int32.MinValue;
			}
		}
	}

	public struct FRAMEID
	{
		UInt32 value;

		FRAMEID(UInt32 value)
		{
			this.value = value;
		}

		public static implicit operator UInt32(FRAMEID value)
		{
			return value.value;
		}

		public static implicit operator FRAMEID(UInt32 value)
		{
			UInt32 tvalue = (UInt32)value;
			return new FRAMEID(tvalue);
		}

		public static UInt32 MaxValue
		{
			get
			{
				return UInt32.MaxValue;
			}
		}

		public static UInt32 MinValue
		{
			get
			{
				return UInt32.MinValue;
			}
		}
	}

	public struct CMD_TYPE
	{
		Byte value;

		CMD_TYPE(Byte value)
		{
			this.value = value;
		}

		public static implicit operator Byte(CMD_TYPE value)
		{
			return value.value;
		}

		public static implicit operator CMD_TYPE(Byte value)
		{
			Byte tvalue = (Byte)value;
			return new CMD_TYPE(tvalue);
		}

		public static Byte MaxValue
		{
			get
			{
				return Byte.MaxValue;
			}
		}

		public static Byte MinValue
		{
			get
			{
				return Byte.MinValue;
			}
		}
	}

	public struct PLAYERS_NUM
	{
		Int32 value;

		PLAYERS_NUM(Int32 value)
		{
			this.value = value;
		}

		public static implicit operator Int32(PLAYERS_NUM value)
		{
			return value.value;
		}

		public static implicit operator PLAYERS_NUM(Int32 value)
		{
			Int32 tvalue = (Int32)value;
			return new PLAYERS_NUM(tvalue);
		}

		public static Int32 MaxValue
		{
			get
			{
				return Int32.MaxValue;
			}
		}

		public static Int32 MinValue
		{
			get
			{
				return Int32.MinValue;
			}
		}
	}

	public struct MATCH_ID
	{
		UInt32 value;

		MATCH_ID(UInt32 value)
		{
			this.value = value;
		}

		public static implicit operator UInt32(MATCH_ID value)
		{
			return value.value;
		}

		public static implicit operator MATCH_ID(UInt32 value)
		{
			UInt32 tvalue = (UInt32)value;
			return new MATCH_ID(tvalue);
		}

		public static UInt32 MaxValue
		{
			get
			{
				return UInt32.MaxValue;
			}
		}

		public static UInt32 MinValue
		{
			get
			{
				return UInt32.MinValue;
			}
		}
	}

	public struct MATCHTIME
	{
		Int32 value;

		MATCHTIME(Int32 value)
		{
			this.value = value;
		}

		public static implicit operator Int32(MATCHTIME value)
		{
			return value.value;
		}

		public static implicit operator MATCHTIME(Int32 value)
		{
			Int32 tvalue = (Int32)value;
			return new MATCHTIME(tvalue);
		}

		public static Int32 MaxValue
		{
			get
			{
				return Int32.MaxValue;
			}
		}

		public static Int32 MinValue
		{
			get
			{
				return Int32.MinValue;
			}
		}
	}

	public class HERO_IDS_LIST : List<Int32>
	{

	}

	public class HERO_INFOS
	{
		public Int32 id = 0;
		public string name = "";
		public string nick_name = "";
		public Int32 race = 0;
		public string race_desc = "";
		public Int32 skill_1 = 0;
		public Int32 skill_2 = 0;
		public Int32 skill_3 = 0;
		public Int32 skill_4 = 0;
		public Int32 hero_hp = 0;
		public Int32 hero_mp = 0;
		public Int32 hero_strength = 0;
		public Int32 hero_agile = 0;
		public Int32 hero_intelligence = 0;
		public Int32 hero_attacktime = 0;
		public Int32 hero_speed = 0;
		public Int32 hero_attackfront = 0;
		public Int32 hero_attackback = 0;
		public Int32 hero_skillfront = 0;
		public Int32 hero_skillback = 0;
		public Int32 hero_scope = 0;
		public Int32 hero_attack = 0;
		public Int32 hero_armor = 0;
		public Int32 hero_unarmor = 0;
		public Int32 hero_magic = 0;
		public Int32 hero_magicresist = 0;
		public Int32 hero_hprestored = 0;
		public Int32 hero_mprestored = 0;
		public Int32 hero_crit = 0;
		public Int32 hero_uncrit = 0;
		public Int32 hero_critunmber = 0;
		public Int32 hero_evade = 0;
		public Int32 hero_unevade = 0;
		public Int32 hero_parry = 0;
		public Int32 hero_unparry = 0;
		public Int32 hero_parrynumber = 0;
		public Int32 hero_xixue = 0;
		public Int32 atk_power = 0;
		public Int32 hurt_power = 0;
		public Int32 kill_power = 0;
		public Int32 hero_energe = 0;

	}

	public class SKILL_INFOS
	{
		public Int32 id = 0;
		public string name = "";
		public string skill_icon = "";
		public Int32 skill_damage_chushi = 0;
		public Int32 skill_damage_growth = 0;
		public Int32 skill_ad_chushi = 0;
		public Int32 skill_ad_growth = 0;
		public Int32 skill_ap_chushi = 0;
		public Int32 skill_ap_growth = 0;
		public Int32 skill_type = 0;
		public Int32 skill_ongoing = 0;
		public Int32 skill_sing_time = 0;
		public Int32 skill_cutdown = 0;
		public Int32 skill_cutdownif = 0;
		public Int32 skill_cd = 0;

	}

	public class SKILL_INFOS_LIST : List<SKILL_INFOS>
	{

	}

	public class SHOP_INFOS
	{
		public Int32 shop_id = 0;
		public string shop_des = "";
		public Int32 shop_refreshstart = 0;
		public Int32 shop_refreshtime = 0;
		public Int32 shop_needid = 0;
		public string shop_needdes = "";
		public Int32 shop_amount = 0;
		public string shop_refreshtime1 = "";
		public Int32 open_lv = 0;

	}

	public class SHOP_INFOS_LIST : List<SHOP_INFOS>
	{

	}

	public class PROPS_INFOS
	{
		public Int32 prop_id = 0;
		public string prop_name = "";
		public string prop_icon = "";
		public Int32 prop_type = 0;
		public Int32 prop_quality = 0;
		public Int32 prop_order = 0;
		public Int32 prop_max = 0;
		public Int32 prop_resale = 0;
		public Int32 prop_diamond = 0;
		public Int32 prop_hanbing = 0;
		public Int32 prop_moba = 0;
		public Int32 prop_jjc = 0;
		public Int32 prop_maoxian = 0;
		public string prop_describe = "";
		public Int32 prop_function = 0;
		public Int32 prop_parameters1 = 0;
		public Int32 prop_parameters2 = 0;
		public Int32 prop_parameters3 = 0;
		public Int32 prop_parameters4 = 0;
		public Int32 prop_parameters5 = 0;
		public Int32 prop_parameters6 = 0;
		public Int32 prop_drop1 = 0;
		public Int32 prop_drop2 = 0;
		public Int32 prop_drop3 = 0;
		public Int32 prop_drop4 = 0;
		public Int32 prop_gm = 0;
		public Int32 prop_buy = 0;

	}

	public class PROPS_INFOS_LIST : List<PROPS_INFOS>
	{

	}

	public class AVATAR_INFOS
	{
		public UInt64 dbid = 0;
		public string name = "";
		public Byte roleType = 0;
		public Int32 weaponId = 0;

	}

	public class AVATAR_INFOS_LIST
	{
		public List<AVATAR_INFOS> values = new List<AVATAR_INFOS>();

	}

	public class MATCHING_INFOS
	{
		public Int32 id = 0;
		public string name = "";
		public Int32 teamId = 0;
		public Int32 heroId = 0;
		public List<Int32> heroIdLst = new List<Int32>();

	}

	public class MATCHING_INFOS_LIST
	{
		public List<MATCHING_INFOS> values = new List<MATCHING_INFOS>();

	}

	public class FS_ENTITY_DATA
	{
		public Int32 entityid = 0;
		public Byte cmd_type = 0;
		public byte[] datas = new byte[0];

	}

	public class FS_FRAME_DATA
	{
		public UInt32 frameid = 0;
		public List<FS_ENTITY_DATA> operation = new List<FS_ENTITY_DATA>();

	}

	public class FS_FRAME_LIST
	{
		public List<FS_FRAME_DATA> values = new List<FS_FRAME_DATA>();

	}


}