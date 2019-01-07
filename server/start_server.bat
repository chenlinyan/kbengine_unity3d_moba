@echo off
set curpath=%~dp0

cd ..
set KBE_ROOT=%cd%
set KBE_RES_PATH=%KBE_ROOT%/kbe/res/;%curpath%/;%curpath%/scripts/;%curpath%/res/
set KBE_BIN_PATH=%KBE_ROOT%/kbe/bin/server/

if defined uid (echo UID = %uid%)

cd %curpath%
call "kill_server.bat"

echo KBE_ROOT = %KBE_ROOT%
echo KBE_RES_PATH = %KBE_RES_PATH%
echo KBE_BIN_PATH = %KBE_BIN_PATH%

start %KBE_BIN_PATH%/machine.exe --cid=12340 --gus=1
start %KBE_BIN_PATH%/logger.exe --cid=23450 --gus=2
start %KBE_BIN_PATH%/interfaces.exe --cid=34560 --gus=3
start %KBE_BIN_PATH%/dbmgr.exe --cid=45670 --gus=4
start %KBE_BIN_PATH%/baseappmgr.exe --cid=56780 --gus=5
start %KBE_BIN_PATH%/cellappmgr.exe --cid=67890 --gus=6
start %KBE_BIN_PATH%/baseapp.exe --cid=78900 --gus=7
@rem start %KBE_BIN_PATH%/baseapp.exe --cid=7002 --gus=8 --hide=1
start %KBE_BIN_PATH%/cellapp.exe --cid=89010 --gus=9
@rem start %KBE_BIN_PATH%/cellapp.exe --cid=8002  --gus=10 --hide=1
start %KBE_BIN_PATH%/loginapp.exe --cid=90120 --gus=11