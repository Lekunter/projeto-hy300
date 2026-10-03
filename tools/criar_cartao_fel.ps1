<#
.SYNOPSIS
    Cria um cartao MicroSD "FEL" para o slot da placa do HY300.

.DESCRIPTION
    Grava o stub fel-sdboot.sunxi (sunxi-tools) no setor 16 (offset 8 KB) do cartao.
    O BootROM le o SD antes da eMMC; ao executar o stub ele salta para o modo FEL
    (USB VID_1F3A PID_EFE8), sem depender de botao, controle remoto ou UART.

    ATENCAO: apaga TODO o conteudo do cartao escolhido. Precisa de administrador.
#>

param (
    [Parameter(Mandatory = $false)]
    [int]$DiskNumber = -1
)

$ErrorActionPreference = 'Stop'
$stub = Join-Path $PSScriptRoot 'fel\fel-sdboot.sunxi'

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "   CARTAO MICROSD FEL (fel-sdboot) - HY300 / ALLWINNER   " -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

if (-not (Test-Path $stub)) { throw "Stub nao encontrado: $stub" }
$stubBytes = [IO.File]::ReadAllBytes($stub)
if ([Text.Encoding]::ASCII.GetString($stubBytes, 4, 8) -ne 'eGON.BT0' -or ($stubBytes.Length % 512) -ne 0) {
    throw "Arquivo $stub invalido (sem cabecalho eGON.BT0)."
}

# Apenas discos removiveis pequenos: nunca disco de sistema/boot
$candidates = @(Get-Disk | Where-Object {
    -not $_.IsSystem -and -not $_.IsBoot -and
    $_.BusType -in @('USB', 'SD', 'MMC') -and
    $_.Size -gt 0 -and $_.Size -le 64GB
})

if ($candidates.Count -eq 0) {
    throw "Nenhum cartao/adaptador removivel encontrado (USB/SD ate 64 GB). Plugue o cartao e tente de novo."
}

Write-Host "`nCartoes encontrados:" -ForegroundColor Yellow
$candidates | Format-Table Number, FriendlyName, BusType, @{n='Tamanho (GB)'; e={[math]::Round($_.Size / 1GB, 2)}}, PartitionStyle -AutoSize | Out-Host

if ($DiskNumber -lt 0) {
    if ($candidates.Count -eq 1) {
        $in = Read-Host "Pressione ENTER para usar o disco $($candidates[0].Number) (ou digite outro numero)"
        $DiskNumber = if ($in) { [int]$in } else { $candidates[0].Number }
    } else {
        $DiskNumber = [int](Read-Host "Digite o NUMERO do disco do cartao")
    }
}

$disk = $candidates | Where-Object Number -eq $DiskNumber
if (-not $disk) { throw "Disco $DiskNumber nao esta na lista de cartoes permitidos." }

Write-Host "`nTODO o conteudo de '$($disk.FriendlyName)' (disco $DiskNumber, $([math]::Round($disk.Size / 1GB, 2)) GB) sera APAGADO." -ForegroundColor Red
if ((Read-Host "Digite SIM para continuar") -ne 'SIM') { Write-Host "Cancelado."; exit 1 }

Write-Host "[1/3] Limpando e criando particao FAT32 (inicio em 1 MB)..." -ForegroundColor Yellow
if ($disk.PartitionStyle -ne 'RAW') { Clear-Disk -Number $DiskNumber -RemoveData -RemoveOEM -Confirm:$false }
Initialize-Disk -Number $DiskNumber -PartitionStyle MBR
$part = New-Partition -DiskNumber $DiskNumber -Offset 1MB -UseMaximumSize -AssignDriveLetter
Format-Volume -Partition $part -FileSystem FAT32 -NewFileSystemLabel 'HY300FEL' -Confirm:$false | Out-Null

Write-Host "[2/3] Gravando fel-sdboot.sunxi no offset 8 KB (setor 16)..." -ForegroundColor Yellow
$fs = New-Object IO.FileStream("\\.\PhysicalDrive$DiskNumber", [IO.FileMode]::Open, [IO.FileAccess]::ReadWrite, [IO.FileShare]::ReadWrite)
try {
    [void]$fs.Seek(8192, [IO.SeekOrigin]::Begin)
    $fs.Write($stubBytes, 0, $stubBytes.Length)
    $fs.Flush()

    Write-Host "[3/3] Conferindo gravacao..." -ForegroundColor Yellow
    $check = New-Object byte[] $stubBytes.Length
    [void]$fs.Seek(8192, [IO.SeekOrigin]::Begin)
    [void]$fs.Read($check, 0, $check.Length)
} finally {
    $fs.Close()
}

if ([Convert]::ToBase64String($check) -ne [Convert]::ToBase64String($stubBytes)) {
    throw "A leitura de conferencia nao bate com o stub. Tente outro leitor/adaptador."
}

Write-Host "`n[OK] Cartao FEL pronto." -ForegroundColor Green
Write-Host "Proximos passos (detalhes em docs/GUIA_RECUPERACAO.md, Metodo A):" -ForegroundColor Cyan
Write-Host "  1. Projetor FORA da tomada; cartao no slot MicroSD da placa."
Write-Host "  2. Cabo USB-A x USB-A entre o PC e a porta USB do projetor."
Write-Host "  3. Ligue na tomada e veja se o Windows mostra USB\VID_1F3A&PID_EFE8."
