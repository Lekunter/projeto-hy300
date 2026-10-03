# Projeto HY300: contexto de recuperação

> **Repositório:** [projeto-hy300 (GitHub: Lekunter)](https://github.com/Lekunter/projeto-hy300)
> **Última atualização:** 03/10/2026
> **Status:** projetor ainda em brick. O PhoenixCard (modo Product) no slot MicroSD da placa **não recuperou**. SoC **confirmado H713** e placa identificada como **`M11-REV1.3`** (fotos de 03/10, ver §3). Próximo passo: entrar em FEL (USB+Power ou cartão FEL `CRIAR_CARTAO_FEL.bat`; controle `Vol+` já falhou) e procurar a UART nos pads ao lado da eMMC.

---

## 1. Sintoma atual (confirmado em 03/10/2026)

| Situação | Comportamento |
| :--- | :--- |
| **Sem cartão**, liga na tomada | Pula o standby, liga direto (LED/cooler), projeta **tela vazia** (luz sem imagem). Igual ao brick original. |
| **Com o cartão PhoenixCard (Product)** no slot da placa | Fica em **standby**, não liga, não responde ao botão Power nem a nada. |

**Leitura técnica:**
- O comportamento **muda** com o cartão → o BootROM **lê o slot MicroSD** antes da eMMC. Isso é ótimo: o slot é um caminho garantido para executar código nosso (cartão FEL).
- Com o cartão Product, o boot0 do cartão foi carregado, mas o processo **travou ou não tem saída de vídeo** (não houve barra de progresso). Possíveis causas, em ordem de probabilidade:
  1. **A imagem não é desta placa.** O `HY300 Pro+ - H713.img` foi feito para a placa de referência `HY200_QZ713DF_A1`. Esta é a **`M11-REV1.3`**: mesmo SoC, mas eMMC, Wi-Fi e provavelmente painel diferentes. A configuração de DRAM/boot do cartão pode não servir para esta placa.
  2. O cartão estava gravando "às cegas" (o gravador de cartão não liga o painel LCD) e foi retirado antes do fim. Menos provável: o comportamento sem cartão continua idêntico ao de antes.
  - ~~SoC diferente de H713~~: **descartado**. O chip foi fotografado: `Allwinner H713 PA251DA 9B70`.
- **A eMMC muito provavelmente não foi alterada**, porque sem cartão o aparelho se comporta exatamente como antes.

---

## 2. Causa raiz provável do brick original

- Soft brick após **OTA**. Na plataforma H713 de referência, a GPT tem partições `_a`/`_b`, mas **só o Slot A tem dados**; o Slot B é zerado. Uma OTA que grava no Slot B e troca o slot ativo deixa o U-Boot tentando iniciar um sistema vazio.
- Isso está documentado para a placa de referência (`references/HY300-H713-Research/Firmware/PARTITION_LAYOUT.md`). **Para esta placa é hipótese**: não temos log serial que confirme.
- Hipótese alternativa a não descartar: a OTA gravou firmware de **outro painel/placa** (a "tela vazia com luz" é típica de painel sem sinal).

---

## 3. Hardware real deste aparelho (fotos em `fotos placa/` e `fotos placa/fotos 0310/`)

Placa **`M11-REV1.3`** (serigrafia ao lado do SoC, com `C01`). **Não é** a `HY200_QZ713DF_A1` da pesquisa YuujiLab, embora use o mesmo SoC. Tudo abaixo foi confirmado por foto em 03/10/2026, com o dissipador removido:

| Item | Placa de referência (YuujiLab) | **Esta placa (`M11-REV1.3`)** |
| :--- | :--- | :--- |
| SoC | Allwinner H713 | **Allwinner H713 `PA251DA 9B70`** ✅ |
| RAM | 4x 2Gb DDR3 (2x Elpida + 2x Samsung) | 4x 2Gb DDR3 **SK Hynix `H5TQ2G83CFR`** (2 em cada face) = 1 GB |
| eMMC | Kioxia `THGBMHG6C1LBAIL` 8 GB | **Samsung `KLM8G1WEPD-B031`** 8 GB (face inferior) |
| Wi-Fi/BT | AIC8800D40 (chip na placa) | Módulo blindado **`AW869A WiFi6`**, antena U.FL |
| PMIC | A8038S | QFN com 3 indutores `2R2` (face inferior, marcação não lida) |
| Amplificador | XA8870C | SOIC-8 `NS4150`-like ao lado do slot SD (face inferior) |
| Slot MicroSD | não tem | **Tem** (face inferior, ao lado da RAM, sem abertura na carcaça) |
| UART | pads `TX`/`RX` serigrafados | **Não localizada.** Candidato: 4 pads redondos em fila ao lado da eMMC (face inferior), não testado. |
| Receptor IR | conector `IR` | Conector `遥控头接口` (sensor frontal) **e** receptor traseiro de 3 pinos no canto P2/cooler (os "3 furos"). **Não é UART.** |
| Botão FEL/`UBOOT` | presente sob o HDMI | **Não montado**; só existe o botão Power |
| Etiqueta | `DW1G+8G+20800D4` | `A024 QC-C 0115 PASS` |

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
| antes de 03/10 | Controle remoto `Vol+` ao ligar | Não entrou em FEL. |
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

1. ~~Identificar placa e SoC~~: **feito** (H713, `M11-REV1.3`).
2. **Teste sem solda:** placa alimentada só pela USB do PC + botão Power (GUIA, Método E). O controle remoto `Vol+` **já foi testado e não funcionou**.
3. **UART nos 4 pads ao lado da eMMC** (os 3 furos do canto P2 são do receptor IR, não da UART): identificar GND/TX/RX com o multímetro e ligar o CP2102. O log de boot diz **por que** a tela fica vazia (slot B? painel? kernel?) antes de gravar qualquer coisa. Passo a passo: [docs/ROTEIRO_PRATICO_BANCADA_CP2102.md](docs/ROTEIRO_PRATICO_BANCADA_CP2102.md).
4. **Cartão FEL** (`CRIAR_CARTAO_FEL.bat`) + cabo USB-A×USB-A → confirmar `VID_1F3A&PID_EFE8` no notebook. Dá FEL garantido, sem botão nem UART.
5. **Preservar a configuração original desta placa.** A eMMC atual guarda o bootloader/DTB com o painel e a DRAM certos da `M11-REV1.3`. Se a UART funcionar, tentar o conserto **sem regravar tudo**: no U-Boot, `printenv` e corrigir o slot (ex.: voltar para `_a`). Se precisar gravar a imagem inteira, antes faça backup (via ADB se o Android subir, ou pela UART/FEL).
6. **Gravar a imagem de referência pelo PhoenixSuit é aceitável como último recurso.** Com o cartão FEL, a placa sempre volta para FEL, então um flash errado não "mata" o aparelho. O risco real é **perder a config de painel desta placa** (tela continuaria vazia, agora por outro motivo).
7. Procurar imagem específica da `M11-REV1.3`: buscas por "M11-REV1.3" não retornaram nada em 03/10/2026.

Passo a passo detalhado: [docs/GUIA_RECUPERACAO.md](docs/GUIA_RECUPERACAO.md).
