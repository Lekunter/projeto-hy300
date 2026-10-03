@echo off
title Cartao MicroSD FEL - HY300
rem Precisa de administrador para gravar setores brutos no cartao
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    powershell.exe -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\criar_cartao_fel.ps1"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [AVISO] Ocorreu um erro ao criar o cartao FEL.
)
pause
