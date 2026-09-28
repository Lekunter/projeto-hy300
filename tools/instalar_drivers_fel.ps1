<#
.SYNOPSIS
    Instala os drivers Allwinner USB FEL (VID_1F3A PID_EFE8) no Windows.

.DESCRIPTION
    Executa o instalador de drivers de 64 bits do PhoenixSuit com privilégios de administrador.
#>

$driversDir = "$PSScriptRoot\PhoenixSuit\PhoenixSuit v1.10\Drivers"
$dpinst64 = "$PSScriptRoot\PhoenixSuit\PhoenixSuit v1.10\DPInst64.exe"

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "    INSTALADOR DE DRIVERS ALLWINNER USB FEL (64-BIT)    " -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

if (-not (Test-Path $dpinst64)) {
    Write-Error "Instalador DPInst64.exe não encontrado em: $dpinst64"
    exit 1
}

Write-Host "[...] Iniciando instalação dos drivers Allwinner USB..." -ForegroundColor Yellow
Start-Process -FilePath $dpinst64 -ArgumentList "/path `"$driversDir`" /sa" -Verb RunAs -Wait

Write-Host "`n[OK] Processo de instalação finalizado!" -ForegroundColor Green
Write-Host "Ao conectar o projetor em modo FEL, verifique no Gerenciador de Dispositivos:" -ForegroundColor Cyan
Write-Host "  -> 'Dispositivos USB' ou 'Universal Serial Bus controllers'"
Write-Host "  -> Dispositivo identificado com Hardware ID: USB\VID_1F3A&PID_EFE8"
