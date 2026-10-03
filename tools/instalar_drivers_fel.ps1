<#
.SYNOPSIS
    Instala os drivers Allwinner USB FEL (VID_1F3A PID_EFE8) no Windows.

.DESCRIPTION
    Adiciona ao repositorio de drivers do Windows (pnputil) o driver FEL do PhoenixSuit
    (Drivers\AW_Driver\usbdrv.inf) e o driver ADB/fastboot Allwinner (Drivers\ADB_Driver).
    Pede administrador. Funciona com o projetor desconectado: o Windows usa o driver
    automaticamente quando o aparelho aparecer em FEL.
#>

$driversDir = "$PSScriptRoot\PhoenixSuit\PhoenixSuit v1.10\Drivers"
$infs = @(
    "$driversDir\AW_Driver\usbdrv.inf",
    "$driversDir\ADB_Driver\android_winusb.inf"
)

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Pedindo permissao de administrador..." -ForegroundColor Yellow
    Start-Process powershell.exe -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "    INSTALADOR DE DRIVERS ALLWINNER USB FEL (pnputil)    " -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

$falhou = $false
foreach ($inf in $infs) {
    if (-not (Test-Path $inf)) {
        Write-Host "[ERRO] Nao encontrado: $inf" -ForegroundColor Red
        $falhou = $true
        continue
    }
    Write-Host "`n[...] Instalando $(Split-Path $inf -Leaf)" -ForegroundColor Yellow
    pnputil.exe /add-driver "$inf" /install
    # 0 = ok, 259 = nenhum dispositivo conectado agora (driver fica no repositorio mesmo assim)
    if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne 259) {
        Write-Host "[ERRO] pnputil retornou $LASTEXITCODE para $inf" -ForegroundColor Red
        $falhou = $true
    }
}

Write-Host "`nDrivers Allwinner no repositorio do Windows:" -ForegroundColor Cyan
pnputil.exe /enum-drivers | Select-String -Context 1, 4 -Pattern 'usbdrv.inf|android_winusb.inf' | Out-Host

if ($falhou) {
    Write-Host "`n[AVISO] Algum driver falhou. Veja as mensagens acima." -ForegroundColor Red
} else {
    Write-Host "`n[OK] Drivers instalados." -ForegroundColor Green
}
Write-Host "Com o projetor em FEL, o Gerenciador de Dispositivos deve mostrar:"
Write-Host "  'USB Device(VID_1f3a_PID_efe8)'  ->  ID de hardware USB\VID_1F3A&PID_EFE8"
Read-Host "`nPressione ENTER para fechar"
