<#
.SYNOPSIS
    Detecta automaticamente o módulo CP2102 e abre a sessão serial no PuTTY a 115200 bps.

.DESCRIPTION
    Prioriza portas USB-to-UART (CP210x, CH340, FTDI, etc.) e inicia o PuTTY configurado.
#>

try {
    Write-Host "=========================================================" -ForegroundColor Cyan
    Write-Host "   INICIADOR SERIAL CP2102 -> CONSOLE U-BOOT (115200)   " -ForegroundColor Cyan
    Write-Host "=========================================================" -ForegroundColor Cyan

    $puttyPath = "$PSScriptRoot\putty.exe"
    if (-not (Test-Path $puttyPath)) {
        Write-Host "[...] PuTTY não encontrado localmente. Baixando PuTTY portátil..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/putty.exe" -OutFile $puttyPath
        Write-Host "[OK] PuTTY pronto!" -ForegroundColor Green
    }

    # 1. Procurar por porta COM ativa
    Write-Host "[...] Buscando módulo CP2102 / USB-TTL conectado..." -ForegroundColor Yellow
    $allPorts = Get-CimInstance Win32_PnPEntity | Where-Object { $_.Name -match "\(COM(\d+)\)" }

    $selectedPort = $null

    # Filtra portas preferenciais USB (Silicon Labs, CP210x, CH340, FTDI, Prolific, USB Serial)
    $usbPorts = $allPorts | Where-Object { 
        $_.Name -match 'CP210|Silicon Labs|CH340|FTDI|Prolific|USB-to-Serial|USB Serial' 
    }

    if ($usbPorts) {
        $target = $usbPorts[0]
        if ($target.Name -match '\((COM\d+)\)') {
            $selectedPort = $Matches[1]
            Write-Host "`n[OK] Módulo USB-Serial identificado automaticamente:" -ForegroundColor Green
            Write-Host "     -> $($target.Name)" -ForegroundColor Green
        }
    } elseif ($allPorts.Count -eq 1) {
        if ($allPorts.Name -match '\((COM\d+)\)') {
            $selectedPort = $Matches[1]
            Write-Host "`n[OK] Porta COM detectada: $($allPorts.Name)" -ForegroundColor Green
        }
    } elseif ($allPorts.Count -gt 1) {
        Write-Host "`nMúltiplas portas COM encontradas no sistema:" -ForegroundColor Yellow
        for ($i = 0; $i -lt $allPorts.Count; $i++) {
            Write-Host " [$i] $($allPorts[$i].Name)"
        }
        $choice = Read-Host "`nSelecione o número correspondente ao seu módulo USB-TTL"
        if ($choice -match '^\d+$' -and [int]$choice -lt $allPorts.Count) {
            if ($allPorts[[int]$choice].Name -match '\((COM\d+)\)') {
                $selectedPort = $Matches[1]
            }
        }
    } else {
        Write-Host "`n[AVISO] Nenhuma porta COM detectada no momento." -ForegroundColor Red
        Write-Host "Verifique se o seu módulo CP2102 está plugado na USB." -ForegroundColor Yellow
        $comInput = Read-Host "`nSe você já souber o número da porta COM, digite aqui (ex: COM9) ou aperte Enter para sair"
        if ($comInput -match '^COM\d+$') {
            $selectedPort = $comInput.ToUpper()
        }
    }

    if ($selectedPort) {
        Write-Host "`nIniciando sessão serial no PuTTY:" -ForegroundColor Cyan
        Write-Host "  -> Porta: $selectedPort" -ForegroundColor Cyan
        Write-Host "  -> Velocidade: 115200 baud" -ForegroundColor Cyan
        Write-Host "  -> Parâmetros: 8-N-1" -ForegroundColor Cyan
        Write-Host "`n[INSTRUÇÃO IMPORTANTE]" -ForegroundColor Yellow
        Write-Host "1. A janela preta do PuTTY vai abrir agora." -ForegroundColor White
        Write-Host "2. Clique nela e FIQUE APERTANDO ESPAÇO repetidamente." -ForegroundColor White
        Write-Host "3. Ligue o cabo de força do projetor na tomada." -ForegroundColor White
        Write-Host "4. Quando o boot parar e aparecer o prompt '=>', digite: efex" -ForegroundColor Green
        
        Start-Process -FilePath $puttyPath -ArgumentList "-serial $selectedPort -sercfg 115200,8,n,1,N"
        Write-Host "`n[OK] PuTTY iniciado com sucesso na porta $selectedPort!" -ForegroundColor Green
    } else {
        Write-Host "`nNenhuma porta serial selecionada." -ForegroundColor Yellow
    }
} catch {
    Write-Host "`n[ERRO]: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nPressione Enter para fechar esta janela..." -ForegroundColor Gray
Read-Host | Out-Null
