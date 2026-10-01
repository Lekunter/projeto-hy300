@echo off
title Preparador de MicroSD / Pendrive para Boot HY300
chcp 65001 >nul

echo =========================================================
echo    PREPARADOR DE CARTAO MICROSD / USB - HY300 H713       
echo =========================================================
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\preparar_pendrive_update.ps1"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [AVISO] Ocorreu um erro durante a preparacao da unidade.
    pause
) else (
    echo.
    echo [SUCESSO] Concluido! Pode remover o adaptador e colocar no projetor.
    pause
)
