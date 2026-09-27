# Projeto HY300 — Contexto de Recuperação e Engenharia Reversa

> **Repositório:** [projeto-hy300](https://github.com/Lekunter/projeto-hy300)  
> **Status:** Diagnóstico concluído, ferramentas mapeadas, aguardando download da ROM e conexão física.

---

## 1. O Problema e Causa Raiz

### Sintoma
- Projetor smart genérico modelo **HY300** (marcas Magcubic / Transpeed / OEM).
- Sofreu **soft brick** após atualização de firmware via OTA (Over-The-Air).
- O aparelho liga (LED acende, cooler gira), mas não inicia o sistema Android (tela preta ou travado no logo).

### Diagnóstico Técnico e Causa Raiz
Graças à engenharia reversa detalhada da comunidade (projeto *HY300-H713-Research* por YuujiLab/lolmam), a falha típica de OTA neste projetor foi identificada:
- **Tabela de Partições Virtual A/B Falsa:** A tabela GPT do HY300 define partições duplas (`_a` e `_b`), porém **apenas o Slot A é funcional e populado**.
- As partições do Slot B (`boot_b`, `vendor_boot_b`, `dtbo_b`, `vbmeta_b`, etc.) de fábrica são dummies completamente preenchidos com zeros (`0x00`).
- Ao realizar uma atualização OTA padrão do Android, o serviço tenta gravar no slot inativo (Slot B) e alterar o slot ativo no bootloader. Ao reiniciar, o U-Boot tenta carregar o Slot B vazio, resultando em loop de boot ou falha total de inicialização.

---

## 2. Especificações de Hardware

- **SoC:** Allwinner H713 (`sun50iw12p1` / plataforma TV303)
- **CPU:** Quad-Core ARM Cortex-A53
- **GPU:** ARM Mali-G31 MP2
- **Memória RAM:** 1GB DDR3 SDRAM
- **Armazenamento:** 8GB eMMC Kioxia / Toshiba (`THGBMHG6C1LBAIL`, ~7.3GB utilizável)
- **Controlador Wi-Fi/BT:** AIC8800D40 (Wi-Fi 6 802.11ax + Bluetooth 5.4 Dual-Mode)
- **Sistema Operacional Original:** Android 11 (Kernel Linux 4.9.170 ARM64, Userspace 32-bit `armeabi-v7a`)
- **Identificação da Placa-Mãe Comum:** `HY200_QZ713DF_A1` (e variações de lote)

> [!IMPORTANT]
> Existem unidades do HY300 no mercado com SoCs diferentes (ex: Rockchip RK3326-S ou Allwinner H726). A recuperação descrita aqui é exclusiva para variantes baseadas no **Allwinner H713**.

---

## 3. Modos de Operação e Disparo (Boot Modes)

O bootloader U-Boot do Allwinner avalia gatilhos de entrada antes de iniciar o kernel Android:

| Modo | Mecanismo de Entrada | Finalidade |
| :--- | :--- | :--- |
| **Normal Boot** | Inicialização padrão | Carregamento do Android |
| **Recovery** | Botão `Home` no controle IR ao ligar | Wipe de fábrica / Atualização local |
| **FEL Mode** | Tecla `Vol+` no controle IR ao ligar **OU** botão oculto no conector P2/HDMI | Gravação USB de baixo nível (PhoenixSuit) |
| **UART Shell** | Pinos TX/RX na placa (115200 8-N-1) | Console de depuração e comando `efex` |

### Como colocar o projetor em Modo FEL (Modo de Recuperação USB):
O dispositivo em modo FEL é identificado no Windows como `USB\VID_1F3A&PID_EFE8`.

1. **Método 1 (Controle Remoto IR - Não invasivo):**
   - Conecte o cabo USB-A Macho x Macho entre o PC e o projetor.
   - Pressione e mantenha pressionado repetidamente o botão **Volume + (Vol+)** do controle remoto apontado para o sensor IR ao conectar o cabo de energia.
2. **Método 2 (Botão Oculto Reset/FEL):**
   - Com um palito não metálico ou clipe de papel, verifique o orifício do conector de áudio 3.5mm (P2) ou orifício próximo à porta HDMI.
   - Mantenha o botão interno pressionado, insira o cabo USB-A conectado ao PC e depois ligue a energia.
3. **Método 3 (Pinos UART / Linha de Comando):**
   - Conexão serial 3.3V nos pads TX/RX da placa a 115200 bps.
   - Interrompa a contagem do U-Boot e execute o comando `efex`.

---

## 4. Ferramentas e Softwares de Flash

### 1. PhoenixSuit (Recomendado)
- **Versão padrão:** PhoenixSuit v1.19 / v2.0.2
- **Função:** Utilitário oficial da Allwinner para envio da imagem completa `.img` através do protocolo USB FEL.
- **Drivers integrados:** Já inclui os drivers USB FEL (`usbdrv.inf` para VID_1F3A & PID_EFE8).

### 2. LiveSuit / PhoenixUSBPro
- Alternativas caso o PhoenixSuit apresente falha de handshake com o chip H713.
- PhoenixUSBPro é a ferramenta de produção usada em fábricas Allwinner.

---

## 5. Repositórios e Fontes de Pesquisa

1. **Comunidade 4PDA (Transpeed / Magcubic HY300):**
   - Tópico principal: `https://4pda.to/forum/index.php?showtopic=1087405`
   - Concentra dumps de eMMC, discussões sobre revisões de placa e compatibilidade de drivers de vídeo/Wi-Fi.
2. **Engenharia Reversa GitHub (YuujiLab / lolmam):**
   - Repositório: `https://github.com/lolmam/HY300-H713-Research`
   - Documentação de baixo nível, particionamento GPT, desmontagem e análise do BROM.
3. **AndroidPCtv Firmware Hub:**
   - Repositório de imagens completas de fábrica (.img) e firmwares customizados debloated com Projectivy Launcher.

---

## 6. Procedimento de Recuperação (Checklist)

- [ ] Cabo USB-A Macho para USB-A Macho pronto.
- [ ] PhoenixSuit instalado no Windows em modo Administrador.
- [ ] Drivers Allwinner USB FEL verificados no Gerenciador de Dispositivos (`USB\VID_1F3A&PID_EFE8`).
- [ ] Imagem Stock ROM compatível (`.img`) baixada e selecionada na aba **Firmware** do PhoenixSuit.
- [ ] Dispositivo reconhecido em FEL Mode.
- [ ] Gravação iniciada com opção de formatação total (**Upgrade / Format**).
- [ ] Validação do primeiro boot (pode levar até 5 minutos).
