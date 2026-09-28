<#
.SYNOPSIS
    Inicializa o ambiente de trabalho e baixa todas as ferramentas necessárias na máquina de casa.

.DESCRIPTION
    Clona os repositórios de referência se ausentes, baixa o PuTTY portátil, o PhoenixSuit e o Platform-Tools.
#>

$baseDir = Split-Path -Parent $PSScriptRoot

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "   SETUP DO AMBIENTE DE RECUPERAÇÃO - HY300 H713        " -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# 1. PuTTY
$puttyPath = "$PSScriptRoot\putty.exe"
if (-not (Test-Path $puttyPath)) {
    Write-Host "[...] Baixando PuTTY portátil..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/putty.exe" -OutFile $puttyPath
    Write-Host "[OK] PuTTY baixado!" -ForegroundColor Green
} else {
    Write-Host "[OK] PuTTY já está presente." -ForegroundColor Green
}

# 2. PhoenixSuit
$phoenixZip = "$PSScriptRoot\PhoenixSuit_v1.10.zip"
$phoenixDir = "$PSScriptRoot\PhoenixSuit"
if (-not (Test-Path "$phoenixDir\PhoenixSuit v1.10\PhoenixSuit.exe")) {
    if (-not (Test-Path $phoenixZip)) {
        Write-Host "[...] Baixando PhoenixSuit v1.10 com drivers..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri "https://github.com/Nahd33Network/android-x86-tools/raw/master/PhoenixSuit%20v1.10.zip" -OutFile $phoenixZip
    }
    Write-Host "[...] Extraindo PhoenixSuit..." -ForegroundColor Yellow
    Expand-Archive -Path $phoenixZip -DestinationPath $phoenixDir -Force
    Write-Host "[OK] PhoenixSuit pronto!" -ForegroundColor Green
} else {
    Write-Host "[OK] PhoenixSuit já está pronto." -ForegroundColor Green
}

# 3. Google Android Platform Tools
$ptZip = "$PSScriptRoot\platform-tools.zip"
$ptDir = "$PSScriptRoot\platform-tools"
if (-not (Test-Path "$ptDir\adb.exe")) {
    if (-not (Test-Path $ptZip)) {
        Write-Host "[...] Baixando Google Android Platform Tools..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri "https://dl.google.com/android/repository/platform-tools-latest-windows.zip" -OutFile $ptZip
    }
    Write-Host "[...] Extraindo Platform Tools..." -ForegroundColor Yellow
    Expand-Archive -Path $ptZip -DestinationPath $PSScriptRoot -Force
    Write-Host "[OK] Platform Tools pronto!" -ForegroundColor Green
} else {
    Write-Host "[OK] Platform Tools já está pronto." -ForegroundColor Green
}

# 4. Clonar repositórios de referência se ausentes
$refDir = "$baseDir\references"
if (-not (Test-Path $refDir)) {
    New-Item -ItemType Directory -Path $refDir -Force | Out-Null
}

$repos = @(
    @{ Name = "HY300-H713-Research"; Url = "https://github.com/lolmam/HY300-H713-Research.git" },
    @{ Name = "magcubic-root"; Url = "https://github.com/well0nez/magcubic-root.git" },
    @{ Name = "sunxi-tools"; Url = "https://github.com/YuujiLab/sunxi-tools.git" }
)

foreach ($repo in $repos) {
    $target = "$refDir\$($repo.Name)"
    if (-not (Test-Path "$target\.git")) {
        Write-Host "[...] Clonando $($repo.Name)..." -ForegroundColor Yellow
        git clone $repo.Url $target
        Write-Host "[OK] $($repo.Name) pronto!" -ForegroundColor Green
    } else {
        Write-Host "[OK] $($repo.Name) já presente." -ForegroundColor Green
    }
}

Write-Host "`n=========================================================" -ForegroundColor Green
Write-Host "   [SUCESSO] AMBIENTE TOTALMENTE SINCRONIZADO E PRONTO!  " -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
