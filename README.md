# Projeto HY300 — Recuperação, Engenharia Reversa e Upgrade (Allwinner H713)

Repositório completo dedicado à recuperação de soft brick, documentação técnica de baixo nível, ferramentas de regravação, links de firmware e projetos de engenharia de hardware/upgrade com placas de TV Box para o projetor smart **HY300 / HY300 Pro** (baseado no processador **Allwinner H713**, `sun50iw12p1`, placa **`HY200_QZ713DF_A1`**).

---

## 📁 Estrutura do Projeto

```text
projeto-hy300/
├── docs/
│   ├── GUIA_RECUPERACAO.md        # Passo a passo completo dos 4 métodos de unbrick
│   └── HARDWARE_UPGRADE_TVBOX.md  # Arquitetura, mod híbrido e transplante com TV Box
├── tools/
│   ├── PhoenixSuit/               # Utilitário oficial de flash USB FEL + drivers
│   ├── platform-tools/            # Google Android Platform-Tools (adb, fastboot v37.0.1)
│   ├── preparar_pendrive_update.ps1  # Script automático para criar pendrive de unbrick
│   └── instalar_drivers_fel.ps1   # Script de instalação de drivers Allwinner no Windows
├── firmware/
│   └── README.md                  # Catálogo de ROMs, hashes e links (Mega, GDrive)
├── references/
│   ├── HY300-H713-Research/       # Teardown, BROM, GPT, AVB bypass, pinagem UART
│   ├── magcubic-root/             # awimg.py (unpacker/repacker com checksum) e debloat
│   └── sunxi-tools/               # Ferramentas sunxi com suporte ao Allwinner H713
├── CONTEXTO.md                    # Diagnóstico detalhado da falha Virtual A/B pós-OTA
└── README.md                      # Este sumário geral
```

---

## ⚙️ Especificações de Hardware Confirmadas

- **SoC:** Allwinner H713 (`sun50iw12p1` / plataforma TV303)
- **CPU:** Quad-Core ARM Cortex-A53
- **GPU:** ARM Mali-G31 MP2
- **Memória RAM:** 1GB DDR3 (2x Elpida topo + 2x Samsung base)
- **Armazenamento:** 8GB eMMC Kioxia / Toshiba (`THGBMHG6C1LBAIL`)
- **Wi-Fi / BT:** AIC8800D40 (Wi-Fi 6 + Bluetooth 5.4 Dual-Mode)
- **Painel LCD:** TFT transmissivo de ~2.69 polegadas (1280x720 nativo) com flat de 40 pinos
- **Entrada de Vídeo:** HDMI Type-A Female
- **ID USB FEL:** `USB\VID_1F3A&PID_EFE8`

---

## 🛠️ Métodos de Recuperação Prontos para Uso

1. **Unbrick por Pendrive USB (Sem PC):**
   Execute o script `tools/preparar_pendrive_update.ps1` no PowerShell com um pendrive FAT32 e uma imagem stock. Insira o pendrive e ligue o projetor na tomada para iniciar a regravação automática pelo U-Boot. Detalhes em [docs/GUIA_RECUPERACAO.md](docs/GUIA_RECUPERACAO.md).
2. **Flash USB em Modo FEL (Via Computador):**
   Instale os drivers com `tools/instalar_drivers_fel.ps1`, abra o `tools/PhoenixSuit/PhoenixSuit v1.10/PhoenixSuit.exe`, segure o botão oculto de Reset (abaixo da porta HDMI) e conecte o cabo USB-A x USB-A.
3. **Console Serial UART (3.3V 115200 8-N-1):**
   Interrompa o boot e execute `efex` no U-Boot para entrar em modo FEL direto por software.
4. **Hard Unbrick por Curto de Linha de Dados da eMMC:**
   Curto momentâneo entre CLK/DAT0 e GND durante o power on para forçar o BROM em modo FEL caso os botões falhem.

---

## 💡 Opções de Upgrade com Placas de TV Box

Consulte o documento completo em [docs/HARDWARE_UPGRADE_TVBOX.md](docs/HARDWARE_UPGRADE_TVBOX.md):
- **Opção 1 (Mod Híbrido Interno):** Integrar a placa de uma TV Box rápida (Amlogic S905X/W com 2GB/4GB de RAM) dentro da carcaça do HY300, alimentada pela fonte interna (via conversor Step-Down 5V) e conectada à porta HDMI IN do projetor.
- **Opção 2 (Transplante Total):** Se a placa original estiver inutilizada, utilizar uma **Placa Controladora Universal HDMI para LCD de 40 pinos** (baseada em Realtek RTD2660) ligada diretamente no flat do display óptico do projetor.
