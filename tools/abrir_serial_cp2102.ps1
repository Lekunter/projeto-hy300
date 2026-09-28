<#
.SYNOPSIS
    Detecta automaticamente o módulo CP2102 e abre a sessão serial no PuTTY a 115200 bps.

.DESCRIPTION
    Procura por dispositivos com "CP210" ou portas COM ativas e inicia o PuTTY configurado.
#>

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "   INICIADOR SERIAL CP2102 -> CONSOLE U-BOOT (115200)   " -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

$puttyPath = "$PSScriptRoot\putty.exe"
if (-not (Test-Path $puttyPath)) {
    Write-Error "putty.exe não encontrado em: $puttyPath"
    exit 1
}

# 1. Procurar por porta COM ativa
Write-Host "[...] Buscando módulo CP2102 ou porta COM conectada..." -ForegroundColor Yellow
$ports = Get-CimInstance Win32_PnPEntity | Where-Object { $_.Name -match "\(COM(\d+)\)" }

if (-not $ports) {
    Write-Host "`n[AVISO] Nenhuma porta COM detectada no momento." -ForegroundColor Red
    Write-Host "Por favor, conecte o módulo CP2102 na porta USB do computador e tente novamente." -ForegroundColor Yellow
    $comInput = Read-Host "Se você já souber o número da porta COM, digite aqui (ex: COM3) ou aperte Enter para sair"
    if ($comInput -match '^COM\d+$') {
        $selectedPort = $comInput.ToUpper()
    } else {
        exit 0
    }
} elseif ($ports.Count -eq 1) {
    if ($ports.Name -match '\((COM\d+)\)') {
        $selectedPort = $Matches[1]
        Write-Host "`n[OK] Módulo detectado com sucesso: $($ports.Name)" -ForegroundColor Green
    }
} else {
    Write-Host "`nMúltiplas portas COM encontradas:" -ForegroundColor Yellow
    for ($i = 0; $i -lt $ports.Count; $i++) {
        Write-Host " [$i] $($ports[$i].Name)"
    }
    $choice = Read-Host "Selecione o número da porta correspondente ao CP2102"
    if ($choice -match '^\d+$' -and [int]$choice -lt $ports.Count) {
        if ($ports[[int]$choice].Name -match '\((COM\d+)\)') {
            $selectedPort = $Matches[1]
        }
    }
}

if ($selectedPort) {
    Write-Host "`nIniciando sessão serial no PuTTY:" -ForegroundColor Cyan
    Write-Host "  -> Porta: $selectedPort" -ForegroundColor Cyan
    Write-Host "  -> Velocidade: 115200 baud" -ForegroundColor Cyan
    Write-Host "  -> Parâmetros: 8-N-1" -ForegroundColor Cyan
    Write-Host "`n[INSTRUÇÃO IMPORTANTE]" -ForegroundColor Yellow
    Write-Host "Assim que o PuTTY abrir, ligue a tomada do projetor e fique apertando Enter/Espaço para interromper o U-Boot." -ForegroundColor Yellow
    Write-Host "Quando aparecer o prompt '=>', digite: efex" -ForegroundColor Green
    
    Start-Process -FilePath $puttyPath -ArgumentList "-serial $selectedPort -sercfg 115200,8,n,1,N"
}
