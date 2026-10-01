<#
.SYNOPSIS
    Prepara um pendrive USB ou cartão MicroSD em FAT32 para recuperação automática do projetor HY300 (Allwinner H713).

.DESCRIPTION
    Cria a estrutura de pastas e o script de execução do U-Boot na raiz do pendrive/cartão:
    [LetraDoCartao]:\update\auto_update.txt -> 'sunxi_flash write update/update.img firmware'
    [LetraDoCartao]:\update\update.img
#>

param (
    [Parameter(Mandatory = $false)]
    [string]$DriveLetter,

    [Parameter(Mandatory = $false)]
    [string]$FirmwarePath
)

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "  PREPARADOR DE MICROSD / USB AUTO-BOOT - HY300 H713     " -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# 1. Detectar unidades disponíveis
if (-not $DriveLetter) {
    Write-Host "`nUnidades disponíveis detectadas no sistema:" -ForegroundColor Yellow
    $allVolumes = Get-Volume | Where-Object { $_.DriveLetter -and $_.DriveLetter -notin @('C', 'D') }
    if ($allVolumes) {
        $allVolumes | Format-Table DriveLetter, FriendlyName, FileSystemType, SizeRemaining, DriveType
    } else {
        Get-Volume | Where-Object { $_.DriveLetter } | Format-Table DriveLetter, FriendlyName, FileSystemType, SizeRemaining, DriveType
    }

    $DriveLetter = Read-Host "Digite a letra da unidade do cartão/adaptador (ex: E ou F)"
}

$DriveLetter = $DriveLetter.TrimEnd(':').ToUpper() + ":"
if (-not (Test-Path "$DriveLetter\")) {
    Write-Error "A unidade $DriveLetter não foi encontrada ou não está acessível."
    exit 1
}

# 2. Verificar Sistema de Arquivos (FAT32 Obrigatório)
$vol = Get-Volume -DriveLetter ($DriveLetter.TrimEnd(':'))
if ($vol.FileSystemType -ne 'FAT32') {
    Write-Host "`n[AVISO] A unidade $DriveLetter está formatada como $($vol.FileSystemType)." -ForegroundColor Yellow
    Write-Host "O bootloader U-Boot do projetor Allwinner H713 EXIGE estritamente o formato FAT32." -ForegroundColor Yellow
    $fmtChoice = Read-Host "Deseja formatar a unidade $DriveLetter em FAT32 agora? (S/N)"
    if ($fmtChoice -match '^[sSyY]') {
        Write-Host "[...] Formatando unidade $DriveLetter em FAT32..." -ForegroundColor Yellow
        Format-Volume -DriveLetter ($DriveLetter.TrimEnd(':')) -FileSystem FAT32 -NewFileSystemLabel "HY300_BOOT" -Force | Out-Null
        Write-Host "[OK] Unidade $DriveLetter formatada com sucesso em FAT32!" -ForegroundColor Green
    }
}

# 3. Localizar Firmware (.img)
if (-not $FirmwarePath) {
    # Buscar em firmware/, Downloads, Desktop
    $searchPaths = @(
        "$PSScriptRoot\..\firmware",
        "$HOME\Downloads",
        "$HOME\Desktop"
    )
    $foundImgs = @()
    foreach ($p in $searchPaths) {
        if (Test-Path $p) {
            $foundImgs += Get-ChildItem -Path $p -Filter "*.img" -File -Recurse -Depth 2 -ErrorAction SilentlyContinue | Where-Object { $_.Length -gt 500MB }
        }
    }

    if ($foundImgs.Count -gt 0) {
        Write-Host "`nArquivos de firmware (.img) encontrados:" -ForegroundColor Green
        for ($i = 0; $i -lt $foundImgs.Count; $i++) {
            $sizeGB = [math]::Round($foundImgs[$i].Length / 1GB, 2)
            Write-Host " [$i] $($foundImgs[$i].Name) ($sizeGB GB) - em $($foundImgs[$i].DirectoryName)"
        }
        $choice = Read-Host "`nEscolha o número do firmware ou arraste o arquivo .img aqui"
        if ($choice -match '^\d+$' -and [int]$choice -lt $foundImgs.Count) {
            $FirmwarePath = $foundImgs[[int]$choice].FullName
        } else {
            $FirmwarePath = $choice.Trim('"').Trim("'")
        }
    } else {
        $FirmwarePath = Read-Host "Arraste o arquivo .img do firmware para esta janela ou digite o caminho completo"
        $FirmwarePath = $FirmwarePath.Trim('"').Trim("'")
    }
}

if (-not (Test-Path $FirmwarePath)) {
    Write-Error "Arquivo de firmware não encontrado em: $FirmwarePath"
    exit 1
}

# 4. Criar diretório update na unidade
$targetDir = "$DriveLetter\update"
if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

# 5. Criar auto_update.txt (minúsculo, ASCII, UNIX newline)
$scriptContent = "sunxi_flash write update/update.img firmware`n"
$scriptPath = "$targetDir\auto_update.txt"
[System.IO.File]::WriteAllText($scriptPath, $scriptContent, [System.Text.Encoding]::ASCII)
Write-Host "`n[OK] Criado script de U-Boot: $scriptPath" -ForegroundColor Green

# 6. Copiar firmware renomeando para update.img
$targetImg = "$targetDir\update.img"
Write-Host "[...] Copiando firmware para o cartão como 'update.img'..." -ForegroundColor Yellow
Write-Host "    Origem: $FirmwarePath" -ForegroundColor Gray
Write-Host "    Destino: $targetImg" -ForegroundColor Gray
Write-Host "    (Isso pode levar de 1 a 3 minutos dependendo da velocidade do MicroSD)..." -ForegroundColor Yellow

Copy-Item -Path $FirmwarePath -Destination $targetImg -Force

Write-Host "`n=========================================================" -ForegroundColor Green
Write-Host " [SUCESSO] CARTÃO MICROSD PRONTO PARA O BOOT DO PROJETOR!" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
Write-Host "`nComo fazer a recuperação no projetor:" -ForegroundColor Cyan
Write-Host " 1. Deixe o projetor DESCONECTADO da tomada."
Write-Host " 2. Conecte o adaptador USB com o MicroSD na porta USB do projetor."
Write-Host " 3. Ligue o cabo de força do projetor na tomada."
Write-Host "    (NAO aperte nenhum botão. Deixe ele ligar sozinho)."
Write-Host " 4. O U-Boot detectará o cartão e projetará a barra de progresso verde de gravação."
Write-Host " 5. Quando chegar em 100%, tire da tomada, remova o adaptador USB e ligue normalmente!" -ForegroundColor Green
