# Projeto HY300: recuperação, engenharia reversa e upgrade

Repositório para recuperar de soft brick (após OTA) um projetor **HY300** com **Allwinner H713** (`sun50iw12p1`). A placa deste aparelho é a **`M11-REV1.3`**, diferente da placa de referência da pesquisa (`HY200_QZ713DF_A1`): tem módulo Wi-Fi `AW869A`, eMMC Samsung e slot MicroSD.

**Status atual e próximos passos:** [CONTEXTO.md](CONTEXTO.md)
**Passo a passo:** [docs/GUIA_RECUPERACAO.md](docs/GUIA_RECUPERACAO.md)

---

## Estrutura

```text
projeto-hy300/
├── CONTEXTO.md                    # Status, hardware real, histórico de tentativas, próximos passos
├── CRIAR_CARTAO_FEL.bat           # Cartão MicroSD que força modo FEL pelo slot da placa
├── ABRIR_PHOENIXSUIT.bat          # Flash por USB FEL
├── ABRIR_PHOENIXCARD.bat          # Cartão de produção (Product/Startup)
├── PREPARAR_CARTAO_MICROSD.bat    # Cartão/pendrive update/auto_update.txt (não confirmado)
├── ABRIR_SERIAL_CP2102.bat        # PuTTY 115200 no CP2102
├── docs/
│   ├── GUIA_RECUPERACAO.md        # Métodos A–G, com status de cada um
│   ├── ROTEIRO_PRATICO_BANCADA_CP2102.md
│   ├── HARDWARE_UPGRADE_TVBOX.md  # Mod híbrido e transplante com TV Box
│   └── VIDEOS_REFERENCIA.md
├── firmware/
│   ├── README.md                  # Origem e links das imagens
│   └── HY300 Pro+ - H713.img      # 1,91 GB, Git LFS (placa de referência!)
├── fotos placa/                   # Fotos reais desta placa
├── fotos_anotadas/                # Infográficos (baseados na referência)
├── tools/
│   ├── fel/fel-sdboot.sunxi       # Stub FEL (sunxi-tools)
│   ├── criar_cartao_fel.ps1
│   ├── PhoenixSuit/  PhoenixCard/  platform-tools/  CP210x_Driver/  putty.exe
│   ├── instalar_drivers_fel.ps1   # Drivers USB FEL
│   ├── preparar_pendrive_update.ps1
│   ├── abrir_serial_cp2102.ps1
│   └── setup_ambiente.ps1         # Baixa ferramentas/referências numa máquina nova
└── references/
    ├── HY300-H713-Research/       # YuujiLab: BROM, GPT, UART, FEL, AVB (placa HY200_QZ713DF_A1)
    ├── magcubic-root/             # awimg.py (desempacota/reempacota IMAGEWTY), debloat
    └── sunxi-tools/               # Fork YuujiLab com suporte ao H713 (submódulo)
```

---

## Hardware

| Item | Placa de referência (`HY200_QZ713DF_A1`) | Este aparelho (`M11-REV1.3`) |
| :--- | :--- | :--- |
| SoC | Allwinner H713, A53 x4, Mali-G31 MP2 | **H713 `PA251DA 9B70`** (confirmado) |
| RAM | 1 GB DDR3 (2x Elpida + 2x Samsung) | 1 GB DDR3, 4x SK Hynix `H5TQ2G83CFR` |
| eMMC | 8 GB Kioxia `THGBMHG6C1LBAIL` | 8 GB Samsung `KLM8G1WEPD-B031` |
| Wi-Fi/BT | AIC8800D40 | módulo `AW869A WiFi6` |
| MicroSD | não | **sim, slot na placa** (face inferior) |
| UART | pads `TX`/`RX` serigrafados | não localizada (candidato: 4 pads ao lado da eMMC) |
| Fonte | n/d | `GKY40W-TYY27A`: 27 V (LED) + 5 V/2 A (placa) |

ID USB em modo FEL: `USB\VID_1F3A&PID_EFE8`. Já foi visto uma vez no Windows do desktop.

---

## Recuperação (resumo)

1. **Entrar em FEL sem solda:** USB do PC + botão Power (o controle `Vol+` já falhou). Se não der, use o cartão FEL.
2. **Cartão FEL** no slot da placa (`CRIAR_CARTAO_FEL.bat`) + cabo USB-A×A → FEL garantido.
3. **PhoenixSuit** com a imagem **correta para a placa**.
4. Alternativas e status de cada uma: [docs/GUIA_RECUPERACAO.md](docs/GUIA_RECUPERACAO.md).

## Upgrade com TV Box

[docs/HARDWARE_UPGRADE_TVBOX.md](docs/HARDWARE_UPGRADE_TVBOX.md): TV Box ligada na entrada HDMI do projetor (se a placa for recuperada) ou placa controladora HDMI→LCD 40 vias (se não for).
