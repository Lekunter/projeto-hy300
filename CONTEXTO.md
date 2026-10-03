# Projeto HY300: contexto de recuperação

> **Repositório:** [projeto-hy300 (GitHub: Lekunter)](https://github.com/Lekunter/projeto-hy300)
> **Última atualização:** 03/10/2026
> **Status:** projetor ainda em brick. O PhoenixCard (modo Product) no slot MicroSD da placa **não recuperou**. Próximo passo: identificar o SoC/placa e entrar em FEL pelo cartão FEL (`CRIAR_CARTAO_FEL.bat`).

---

## 1. Sintoma atual (confirmado em 03/10/2026)

| Situação | Comportamento |
| :--- | :--- |
| **Sem cartão**, liga na tomada | Pula o standby, liga direto (LED/cooler), projeta **tela vazia** (luz sem imagem). Igual ao brick original. |
| **Com o cartão PhoenixCard (Product)** no slot da placa | Fica em **standby**, não liga, não responde ao botão Power nem a nada. |

**Leitura técnica:**
- O comportamento **muda** com o cartão → o BootROM **lê o slot MicroSD** antes da eMMC. Isso é ótimo: o slot é um caminho garantido para executar código nosso (cartão FEL).
- Com o cartão Product, o boot0 do cartão foi carregado, mas o processo **travou ou não tem saída de vídeo** (não houve barra de progresso). Possíveis causas, em ordem de probabilidade:
  1. **A imagem não é desta placa.** O `HY300 Pro+ - H713.img` foi feito para a placa de referência `HY200_QZ713DF_A1` (RAM Elpida/Samsung, Wi-Fi AIC8800). A placa deste aparelho é **outra revisão** (ver seção 3). Parâmetros de DRAM, painel e Wi-Fi podem não bater, e o boot0 do cartão pode travar ao iniciar a RAM.
  2. **O SoC nem é H713.** Ele está sob o dissipador e **nunca foi visto**. "H713" veio da pesquisa de referência, não desta placa.
  3. O cartão estava gravando "às cegas" (o gravador de cartão não liga o painel LCD) e foi retirado antes do fim. Menos provável: o comportamento sem cartão continua idêntico ao de antes.
- **A eMMC muito provavelmente não foi alterada**, porque sem cartão o aparelho se comporta exatamente como antes.

---

## 2. Causa raiz provável do brick original

- Soft brick após **OTA**. Na plataforma H713 de referência, a GPT tem partições `_a`/`_b`, mas **só o Slot A tem dados**; o Slot B é zerado. Uma OTA que grava no Slot B e troca o slot ativo deixa o U-Boot tentando iniciar um sistema vazio.
- Isso está documentado para a placa de referência (`references/HY300-H713-Research/Firmware/PARTITION_LAYOUT.md`). **Para esta placa é hipótese**: não temos log serial que confirme.
- Hipótese alternativa a não descartar: a OTA gravou firmware de **outro painel/placa** (a "tela vazia com luz" é típica de painel sem sinal).

---

## 3. Hardware real deste aparelho (fotos em `fotos placa/`)

Esta placa **não é** a `HY200_QZ713DF_A1` da pesquisa YuujiLab. Diferenças confirmadas por foto:

| Item | Placa de referência (YuujiLab) | **Esta placa** |
| :--- | :--- | :--- |
| SoC | Allwinner H713 (visível) | **Coberto por dissipador, não verificado** |
| RAM (face superior) | 2x Elpida `J2108BCSE` | 2x **SK Hynix `H5TQ2G83CFR PBC 213V`** (DDR3 2Gb cada) |
| Wi-Fi/BT | AIC8800D40 (chip na face inferior) | Módulo blindado **`AW869A WiFi6`** na face superior, antena U.FL |
| Slot MicroSD | não tem | **Tem** (soldado ao lado da RAM, sem abertura na carcaça) |
| Pads UART | `TX`/`RX` serigrafados ao lado do SoC | **Sem serigrafia**, não localizados |
| Botão FEL/`UBOOT` | presente sob o HDMI | **Não montado**; só existe o botão Power |
| Etiqueta | `DW1G+8G+20800D4` | Etiqueta `…0115 PASS` perto do slot SD |

Demais itens desta placa:
- Cristal `24.000 MHz`; jack P2 3,5 mm; HDMI; 1x USB-A; FFC de 40 vias do LCD.
- Conectores (serigrafia chinesa): `5V电源接口` (5V), `风扇接口` (cooler), `遥控头接口` (receptor IR, 3 fios), `SPK` (alto-falante).
- `按键接口`: pads `GND` / `ON/OFF` / `LEDCTL`. `ON/OFF` é a linha do botão Power (em paralelo com o microswitch). **Não aciona FEL.**
- `马达接口`: motor de foco, não populado.

**Fonte (PCB verde):** `GKY40W-TYY27A REV:A01` (2023-11-25). Saídas **27 V / 1,1 A** (LED da lâmpada) e **5 V / 2 A** (placa lógica).
> ⚠️ O capacitor primário (`KSJ VENT`) guarda 170–340 V DC mesmo desligado. Não toque na placa verde ligada à tomada.

Infográficos anotados: `fotos_anotadas/01…04`. Eles foram gerados a partir da pesquisa de referência; **a posição de UART marcada neles não foi confirmada nesta placa.**

---

## 4. Histórico de tentativas

| Data | Tentativa | Resultado |
| :--- | :--- | :--- |
| antes de 28/09 | PhoenixSuit + botão/controle | Nunca reconheceu. Mas o Windows do **desktop** já registrou `USB\VID_1F3A&PID_EFE8` uma vez, então o SoC é Allwinner e **entra em FEL**. |
| 30/09 | Procurar pads TX/RX para o CP2102 | Não encontrados (placa sem serigrafia). |
| 30/09 | Curto `ON/OFF`–`GND` (sugestão do modo IA do Google) | Equivale a apertar Power; não leva a FEL. |
| 01/10 | Cartão `update/auto_update.txt` (pendrive/SD) | Preparado, **nunca testado** no projetor (foi substituído pelo PhoenixCard). Método **não confirmado** para este U-Boot. |
| 01–03/10 | PhoenixCard v4.2.7 modo **Product** no slot da placa | Fica em standby, sem barra, sem resposta. Sem cartão, nada mudou. |

---

## 5. Ferramentas e arquivos

| Arquivo | Função |
| :--- | :--- |
| `CRIAR_CARTAO_FEL.bat` → `tools/criar_cartao_fel.ps1` | **Novo.** Grava `tools/fel/fel-sdboot.sunxi` no setor 16 do cartão: força **modo FEL** pelo slot SD. |
| `ABRIR_PHOENIXSUIT.bat` | PhoenixSuit v1.10 (flash por FEL). Drivers: `tools/instalar_drivers_fel.ps1`. |
| `ABRIR_PHOENIXCARD.bat` | PhoenixCard v4.2.7 (cartão Product/Startup). Para voltar o cartão ao normal: botão **Format to Normal**. |
| `PREPARAR_CARTAO_MICROSD.bat` | Cartão/pendrive `update/auto_update.txt` (não confirmado). |
| `ABRIR_SERIAL_CP2102.bat` | PuTTY 115200 8-N-1 no CP2102 (COM9 no desktop). |
| `firmware/HY300 Pro+ - H713.img` | Imagem `IMAGEWTY` 1,91 GB (Git LFS). **Feita para a placa de referência.** |
| `tools/platform-tools/` | adb/fastboot. |

**Duas máquinas:** o agente roda no **desktop**; o projetor e o cartão ficam no **notebook**. Comandos de disco/USB executados pelo agente veem só as portas do desktop. Sincronize com `git pull` (ou pelo Google Drive em `G:\Meu Drive` para arquivos grandes).

---

## 6. Próximos passos (ordem recomendada)

1. **Identificar a placa e o SoC (antes de gravar qualquer coisa):**
   - Foto do **código serigrafado da placa** (geralmente na borda, ex.: `HY…_…_A1`, com data).
   - Foto da **face inferior** inteira (eMMC, PMIC).
   - Se o dissipador sair com segurança (clipe ou fita térmica, girar levemente, sem alavancar), foto da **marcação do chip**.
2. **Cartão FEL** (`CRIAR_CARTAO_FEL.bat`) + cabo USB-A×USB-A → confirmar `VID_1F3A&PID_EFE8` no notebook. Isso dá FEL garantido, sem botão nem UART.
3. Com FEL e o **SoC confirmado como H713**: flash pelo **PhoenixSuit** com a imagem. Se der erro de DRAM/inicialização, a imagem não é desta placa (ver passo 4).
4. **Conseguir a imagem certa para esta revisão** (placa com AW869A + slot SD + SK Hynix): procurar pelo código da placa no 4PDA / r/Magcubic / XDA.
5. **Antes de qualquer gravação bem-sucedida, fazer backup** da eMMC atual (via FEL + `sunxi-fel` da YuujiLab, ou via ADB se o Android chegar a subir).

Passo a passo detalhado: [docs/GUIA_RECUPERACAO.md](docs/GUIA_RECUPERACAO.md).
