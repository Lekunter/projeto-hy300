<#
.SYNOPSIS
    Prepara um pendrive USB em FAT32 para recuperação automática do projetor HY300 (Allwinner H713).

.DESCRIPTION
    Cria a estrutura de pastas e o script de execução do U-Boot na raiz do pendrive:
    [LetraDoPendrive]:\update\auto_update.txt -> 'sunxi_flash write update/update.img firmware'
    [LetraDoPendrive]:\update\update.img
#>

param (
    [Parameter(Mandatory = $false)]
    [string]$DriveLetter,

    [Parameter(Mandatory = $false)]
    [string]$FirmwarePath
)

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "  PREPARADOR DE PENDRIVE DE RECUPERACAO - HY300 H713     " -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# 1. Obter unidade USB
if (-not $DriveLetter) {
    Write-Host "`nUnidades removíveis detectadas no sistema:" -ForegroundColor Yellow
    Get-Volume | Where-Object { $_.DriveType -eq 'Removable' } | Format-Table DriveLetter, FriendlyName, FileSystemType, SizeRemaining, DriveType

    $DriveLetter = Read-Host "Digite a letra da unidade do pendrive (ex: E)"
}

$DriveLetter = $DriveLetter.TrimEnd(':').ToUpper() + ":"
if (-not (Test-Path "$DriveLetter\")) {
    Write-Error "A unidade $DriveLetter não foi encontrada ou não está acessível."
    exit 1
}

# 2. Localizar Firmware
if (-not $FirmwarePath) {
    $localFirmwares = Get-ChildItem -Path "$PSScriptRoot\..\firmware" -Filter "*.img" -File
    if ($localFirmwares.Count -gt 0) {
        Write-Host "`nFirmwares encontrados localmente:" -ForegroundColor Green
        for ($i = 0; $i -lt $localFirmwares.Count; $i++) {
            Write-Host " [$i] $($localFirmwares[$i].Name)"
        }
        $choice = Read-Host "Escolha o índice da imagem ou digite o caminho completo"
        if ($choice -match '^\d+$' -and [int]$choice -lt $localFirmwares.Count) {
            $FirmwarePath = $localFirmwares[[int]$choice].FullName
        } else {
            $FirmwarePath = $choice
        }
    } else {
        $FirmwarePath = Read-Host "Digite o caminho completo do arquivo de firmware .img"
    }
}

if (-not (Test-Path $FirmwarePath)) {
    Write-Error "Arquivo de firmware não encontrado em: $FirmwarePath"
    exit 1
}

# 3. Criar diretório update no pendrive
$targetDir = "$DriveLetter\update"
if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

# 4. Criar auto_update.txt (em minúsculas, com quebra de linha UNIX padrão)
$scriptContent = "sunxi_flash write update/update.img firmware`n"
$scriptPath = "$targetDir\auto_update.txt"
[System.IO.File]::WriteAllText($scriptPath, $scriptContent, [System.Text.Encoding]::ASCII)

Write-Host "`n[OK] Criado script de U-Boot: $scriptPath" -ForegroundColor Green

# 5. Copiar firmware renomeando para update.img
$targetImg = "$targetDir\update.img"
Write-Host "[...] Copiando firmware para o pendrive como 'update.img' (isso pode levar alguns minutos)..." -ForegroundColor Yellow
Copy-Item -Path $FirmwarePath -Destination $targetImg -Force

Write-Host "`n=========================================================" -ForegroundColor Green
Write-Host " [SUCESSO] PENDRIVE PRONTO PARA UNBRICK!" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
Write-Host "Passos para recuperar o projetor:" -ForegroundColor Cyan
Write-Host " 1. Desconecte o cabo de energia da tomada."
Write-Host " 2. Conecte o pendrive na porta USB do projetor HY300."
Write-Host " 3. Ligue o cabo de energia na tomada (NAO aperte o botao power)."
Write-Host " 4. O U-Boot detectara o pendrive e iniciara a barra de progresso verde."
Write-Host " 5. Ao concluir 100%, desconecte a energia, remova o pendrive e ligue normalmente."
