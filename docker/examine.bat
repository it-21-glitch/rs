@echo off
setlocal
setlocal enabledelayedexpansion
cd C:\Program Files\rs\
:: ����Զ�ֵ̲�ַ
set REMOTE_REPO=origin
:: ��֧����
set BRANCH=main

:: ʹ��WMIC��ȡ�������ں�ʱ��
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "datetime=%%a"

:: ��ȡ�ꡢ�¡��ա�ʱ���֡���
set "year=%datetime:~0,4%"
set "month=%datetime:~4,2%"
set "day=%datetime:~6,2%"
set "hour=%datetime:~8,2%"
set "minute=%datetime:~10,2%"
set "second=%datetime:~12,2%"

:: ����Զ�̷�֧shaֵ
git fetch origin >>  gitlog.txt
:: ��ȡԶ�̷�֧������haֵ
for /f "tokens=*" %%i in ('git rev-parse --short origin/main') do set remoteHead=%%i

:: ��ȡ���ط�֧������haֵ
for /f "tokens=*" %%i in ('git rev-parse --short HEAD') do set localHead=%%i

if "%remoteHead%"=="%localHead%" (
    echo '����HEAD��%localHead%��Զ��HEAD��%remoteHead%��originԶ�ֿ̲�δ���£�ʱ�䣺%year%-%month%-%day% %hour%:%minute%:%second%' >> gitlog.txt
) else (
    git pull %REMOTE_REPO% %BRANCH% >>  gitlog.txt
    echo '����HEAD��%localHead%��Զ��HEAD��%remoteHead%��originԶ�ֿ̲���£�ʱ�䣺%year%-%month%-%day% %hour%:%minute%:%second%' >> gitlog.txt
)

:: ���python����
tasklist | findstr "python" > NUL 2> NUL
if %errorlevel% equ 0 (
    echo "������������" %DATE% %TIME%. >> gitlog.txt
) else (
    echo "�����쳣��������"  %DATE% %TIME%. >> gitlog.txt
    ::start "Flask App" /B  python main.py
     cmd /c start /B python main.py & exit
)

pause
:: �ű�����������...


