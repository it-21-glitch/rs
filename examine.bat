@echo off
setlocal
setlocal enabledelayedexpansion
cd C:\Program Files\rs\
:: 设置远程仓地址
set REMOTE_REPO=origin
:: 分支名称
set BRANCH=main

:: 使用WMIC获取本地日期和时间
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "datetime=%%a"

:: 提取年、月、日、时、分、秒
set "year=%datetime:~0,4%"
set "month=%datetime:~4,2%"
set "day=%datetime:~6,2%"
set "hour=%datetime:~8,2%"
set "minute=%datetime:~10,2%"
set "second=%datetime:~12,2%"

:: 更新远程分支sha值
git fetch origin >>  gitlog.txt
:: 获取远程分支的最新ha值
for /f "tokens=*" %%i in ('git rev-parse --short origin/main') do set remoteHead=%%i

:: 获取本地分支的最新ha值
for /f "tokens=*" %%i in ('git rev-parse --short HEAD') do set localHead=%%i

if "%remoteHead%"=="%localHead%" (
    echo '本地HEAD：%localHead%，远程HEAD：%remoteHead%，origin远程仓库未更新，时间：%year%-%month%-%day% %hour%:%minute%:%second%' >> gitlog.txt
) else (
    git pull %REMOTE_REPO% %BRANCH% >>  gitlog.txt
    echo '本地HEAD：%localHead%，远程HEAD：%remoteHead%，origin远程仓库更新，时间：%year%-%month%-%day% %hour%:%minute%:%second%' >> gitlog.txt
)

:: 检查python进程
tasklist | findstr "python" > NUL 2> NUL
if %errorlevel% equ 0 (
    echo "程序正常启动" %DATE% %TIME%. >> gitlog.txt
) else (
    echo "程序异常重启程序"  %DATE% %TIME%. >> gitlog.txt
    ::start "Flask App" /B  python main.py
     cmd /c start /B python main.py & exit
)

pause
:: 脚本的其他部分...


