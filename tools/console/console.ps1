# Console serial interativo para o HY300.
# - Salva tudo em console_log.txt.
# - Imprime so o que nao for log do kernel/boot (saida do shell).
# - Ao ver o prompt "console:/" pela 1a vez em cada boot, envia o conteudo de autocmd.txt.
# - Envia o conteudo de cmd.txt sempre que esse arquivo aparecer (e apaga o arquivo).
# - Se o CP2102 for desconectado, espera ele voltar e reabre a porta.
param([int]$Baud = 115200, [int]$Minutos = 30)
$dir = $PSScriptRoot
$log = Join-Path $dir "console_log.txt"
$auto = Join-Path $dir "autocmd.txt"
$cmd = Join-Path $dir "cmd.txt"
$fim = (Get-Date).AddMinutes($Minutos)
$sp = $null
$buf = ""
$enviouAuto = $true   # so dispara no proximo boot visto (evita reenviar ao reiniciar o script no meio de um boot)
$promptVisto = $false
function Abrir {
    $dev = Get-CimInstance Win32_PnPEntity | Where-Object { $_.Name -match 'CP210|Silicon Labs|CH340' -and $_.Name -match '\((COM\d+)\)' } | Select-Object -First 1
    if (-not $dev) { return $null }
    $p = New-Object System.IO.Ports.SerialPort $Matches[1], $Baud, 'None', 8, 'One'
    try { $p.Open() } catch { return $null }
    "$(Get-Date -Format HH:mm:ss) ABERTO $($Matches[1]) a $Baud"
    return $p
}
function Enviar($texto) {
    # Um caractere por vez: a UART da placa perde letras quando recebe a linha inteira de uma vez.
    foreach ($l in ($texto -split "`r?`n")) {
        if (-not $l.Trim()) { continue }
        foreach ($ch in ($l + "`r").ToCharArray()) { $sp.Write([string]$ch); Start-Sleep -Milliseconds 12 }
        Start-Sleep -Milliseconds 300
    }
}
while ((Get-Date) -lt $fim) {
    if (-not $sp -or -not $sp.IsOpen) {
        $r = Abrir
        if ($r -is [System.IO.Ports.SerialPort]) { $sp = $r } elseif ($r) { $r[0]; $sp = $r[1] }
        if (-not $sp) { Start-Sleep 2; continue }
    }
    try {
        if (Test-Path $cmd) { $c = Get-Content $cmd -Raw; Remove-Item $cmd; "$(Get-Date -Format HH:mm:ss) >> $($c.Trim())"; Enviar $c }
        $buf += $sp.ReadExisting()
    } catch {
        "$(Get-Date -Format HH:mm:ss) CP2102 desconectado, esperando voltar"
        try { $sp.Close() } catch {}
        $sp = $null; Start-Sleep 2; continue
    }
    while ($buf -match "^(.*?)\r?\n") {
        $l = $Matches[1]; $buf = $buf.Substring($Matches[0].Length)
        $l = ($l.ToCharArray() | Where-Object { [int]$_ -ge 32 -and [int]$_ -lt 127 }) -join ''
        Add-Content $log $l
        if ($l -match 'console:/') { $promptVisto = $true }  # o prompt pode vir colado numa linha do kernel
        if ($l -match 'HELLO! BOOT0') { $enviouAuto = $false; $promptVisto = $false; "$(Get-Date -Format HH:mm:ss) --- novo boot ---" }
        elseif ($l -notmatch '^\s*\[\s*[\d.]+\]' -and $l.Trim() -and ($l.Length - $l.Replace('?','').Length) -lt 0.2 * $l.Length) { "$(Get-Date -Format HH:mm:ss) $l" }
    }
    if (-not $enviouAuto -and ($promptVisto -or $buf -match 'console:/')) {
        $enviouAuto = $true
        if (Test-Path $auto) { "$(Get-Date -Format HH:mm:ss) >> (auto) $((Get-Content $auto -Raw).Trim())"; Enviar (Get-Content $auto -Raw) }
    }
    Start-Sleep -Milliseconds 50
}
if ($sp) { $sp.Close() }
