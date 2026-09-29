@echo off
title Console Serial CP2102 - U-Boot HY300
chcp 65001 >nul
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\abrir_serial_cp2102.ps1"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [AVISO] O script encerrou com codigo %ERRORLEVEL%.
    pause
)
