# Projeto HY300 — Contexto de Recuperação e Engenharia Reversa

> **Repositório Oficial:** [projeto-hy300 (GitHub: Lekunter)](https://github.com/Lekunter/projeto-hy300)  
> **Status Atual:** Hardware desmontado e inspecionado; Mapeamento UART concluído com guia visual; Módulo CP2102 detectado na **COM9**; Scripts de inicialização automática criados; Firmware pronto para regravação.

---

## 1. O Problema e Causa Raiz

### Sintoma
- Projetor smart modelo **HY300** (Allwinner H713).
- Sofreu **soft brick** após atualização de firmware via OTA (Over-The-Air).
- O aparelho liga (cooler gira, LED acende), mas não carrega o sistema Android (tela preta ou travado).

### Diagnóstico Técnico
- **Falha de Particionamento Virtual A/B:** O particionamento GPT original define partições duplas (`_a` e `_b`), mas de fábrica **apenas o Slot A contém dados**. O Slot B é vazio (preenchido com zeros `0x00`).
- O serviço de atualização OTA gravou os dados no slot inativo e mudou o ponteiro do bootloader para o Slot B. Ao reiniciar, o U-Boot tenta inicializar um sistema inexistente.
- **Solução:** Forçar entrada em **Modo Allwinner FEL** (`USB\VID_1F3A&PID_EFE8`) e regravar a Stock ROM completa através do PhoenixSuit.

---

## 2. Raio-X do Hardware Real (Inspecionado via Fotos do Usuário)

Diferenças e especificações identificadas na placa física deste aparelho:

### Placa Principal (PCB Preta):
- **SoC (Processador):** Allwinner H713 (`sun50iw12p1` / plataforma TV303), protegido por um **dissipador de alumínio extrudado preto com aletas**.
- **Cristal Oscilador:** `24.000 MHZ` (clock base do SoC Allwinner).
- **Memória RAM:** 2x chips **SK Hynix** `H5TQ2G83CFR PBC 213V` na face superior (256MB DDR3 cada = 512MB nesta face, 1GB total somando a face inferior).
- **Conectividade Sem Fio:** Módulo blindado metálico **`AW869A WIFI6`** (Wi-Fi 6 + Bluetooth 5.x) com antena conectada via conector U.FL / IPEX dourado.
- **Portas de E/S:**
  - 1x HDMI Fêmea
  - 1x USB 2.0 Tipo-A (Porta de gravação FEL e periféricos)
  - 1x Jack P2 3.5mm de Áudio Estéreo (blindagem metálica)
- **Conectores e Serigrafia Traduzida:**
  - `5V电源接口`: Conector branco de 4 pinos com chicote vermelho grosso (Alimentação 5V vinda da fonte).
  - `风扇接口`: Conector de 2 pinos com fios vermelho e preto (Cooler/ventoinha de exaustão).
  - `遥控头接口`: Conector de 3 pinos com fios preto, vermelho e amarelo (Sensor infravermelho frontal).
  - `按键接口`: Trilha não populada com pads de teste (`GND`, `ON/OFF`, `LEDCTL`).
  - `马达接口`: Trilha não populada para motor de foco automático.
  - `SPK`: Conector de 2 pinos com fios torcidos vermelho e preto ao lado do HDMI (Alto-falante interno).
  - **FFC 40 pinos:** Conector do cabo flat alaranjado do display LCD de projeção.

### Placa da Fonte (PCB Verde):
- **Modelo:** `GKY40W-TYY27A REV:A01 HR DATE:2023.11.25`
- **Saídas do Transformador:**
  - `27V / 1.1A` (~30W): Alimentação do LED da lâmpada de projeção.
  - `5V / 2A` (10W): Alimentação regulada para a placa lógica principal.
- ⚠️ **AVISO DE SEGURANÇA ELÉTRICA:** O capacitor primário grande (`KSJ VENT`) retifica alta tensão (170V a 340V DC) e armazena carga perigosa mesmo após desligado. **Nunca tocar na placa verde enquanto conectada à tomada.**

---

## 3. Guias Visuais Anotados e Mapeamento de Hardware (`fotos_anotadas/`)

Foi gerado um conjunto completo de 4 infográficos técnicos de alta definição na pasta [`fotos_anotadas/`](fotos_anotadas/) anotando diretamente as fotografias reais da placa e comparando cada subsistema com a base de engenharia reversa (`references/HY300-H713-Research/Hardware`):

| Imagem Anotada | Descrição & Destaques | Comparação com a Base de Referência |
| :--- | :--- | :--- |
| [**`01_placa_principal_geral.jpg`**](fotos_anotadas/01_placa_principal_geral.jpg) | Visão panorâmica dos 12 subsistemas: SoC Allwinner H713, 2x RAMs DDR3, Wi-Fi 6, USB 2.0 (FEL), HDMI, Áudio P2, Botão FEL, FAN, 5V DC, SPK, LCD FFC 40p e IR. | Identifica as 4 grandes diferenças da sua placa em relação ao teardown da comunidade (RAMs SK Hynix, Wi-Fi no topo, P2 populado e botão FEL soldado). |
| [**`02_detalhe_processador_ram_botoes.jpg`**](fotos_anotadas/02_detalhe_processador_ram_botoes.jpg) | Macro de altíssima resolução do núcleo lógico: chips SK Hynix (`H5TQ2G83CFR`), dissipador H713, botão microswitch FEL e portas. | Destaque crucial: tutorial ilustrado passo a passo de como forçar o modo FEL (`1f3a:efe8`) usando o microswitch físico sem solda. |
| [**`03_detalhe_wifi_uart_sensores.jpg`**](fotos_anotadas/03_detalhe_wifi_uart_sensores.jpg) | Macro das conexões e conectividade: módulo `AW869A WIFI6`, cristal `24.000 MHz`, conector da ventoinha (`风扇接口`), jack P2 e vias UART. | Demonstra a pinagem de comunicação serial 3.3V TTL (TX/RX/GND) para leitura no PuTTY (COM9). |
| [**`04_placa_fonte_alimentacao.jpg`**](fotos_anotadas/04_placa_fonte_alimentacao.jpg) | Visão completa da placa de alimentação `GKY40W-TYY27A REV:A01` dividida entre Zona de Alta Tensão (Primário) e Zona Segura (Secundário). | Destaque em vermelho do capacitor `KSJ VENT` (~340V DC) com regras de ouro de segurança e guia de teste de voltagens com multímetro. |

---

## 4. Dispositivos de Recuperação Identificados

### 1. Botão Físico SMD de Recuperação (FEL / U-Boot)
- **Localização:** Na borda superior esquerda da placa preta, logo ao lado da porta HDMI (`zoom_left_hdmi_button.jpg`).
- **Função:** Microswitch SMD com botão branco em relevo. Manter pressionado ao conectar o cabo de energia força o chip Allwinner H713 a desviar do bootloader corrompido e entrar em modo FEL USB sem necessidade de conexões adicionais.

### 2. Porta Serial UART (Console U-Boot)
- **Localização dos Pinos:** No canto inferior da placa, entre o conector branco da ventoinha (`风扇接口`) e a porta de áudio P2 (vias circulares de sinal e ilhas de solda ao lado do parafuso).
- **Mapeamento Visual:** Consulte [guia_conexoes_ttl_completo.jpg](fotos%20placa/guia_conexoes_ttl_completo.jpg).
- **Parâmetros de Comunicação:**
  - **Nível Lógico:** **3.3V TTL** (JUMPER DO MÓDULO OBRIGATORIAMENTE EM 3.3V).
  - **Baud Rate:** 115200 bps
  - **Data Bits:** 8 | **Stop Bits:** 1 | **Parity:** None (8-N-1)
  - **GND:** Carcaça metálica externa da porta USB ou HDMI.
  - **VCC:** **NÃO CONECTAR!**
  - **RXD do Módulo:** Conectar ao TX da placa.
  - **TXD do Módulo:** Conectar ao RX da placa.

---

## 5. Estado das Ferramentas e Scripts de Automação

No diretório do projeto, foram criados utilitários de um clique para Windows:

1. **[ABRIR_SERIAL_CP2102.bat](ABRIR_SERIAL_CP2102.bat):**
   - Executa com bypass de permissões do PowerShell.
   - Detecta automaticamente o adaptador **Silicon Labs CP210x na COM9** (ou porta equivalente).
   - Abre o PuTTY automaticamente a 115200 baud configurado.
2. **[ABRIR_PHOENIXSUIT.bat](ABRIR_PHOENIXSUIT.bat):**
   - Abre o utilitário oficial Allwinner PhoenixSuit v1.10.
   - Localização dos arquivos: `tools/PhoenixSuit/PhoenixSuit v1.10/PhoenixSuit.exe`.
   - Instalador de drivers FEL: `tools/PhoenixSuit/PhoenixSuit v1.10/PhoenixDrvInstall.exe`.
3. **Firmware Stock Validado:**
   - Imagem salva em: `firmware/HY300_Pro_Plus_H713.img` (1.91 GB).
   - Cabeçalho verificado: Allwinner `IMAGEWTY` autêntico para chip H713.

---

## 6. Roteiro de Retomada dos Trabalhos

Quando retomar a sessão (seja no PC atual ou no notebook):

### Opção 1: Via Console Serial (CP2102)
1. Conectar o cabo GND na carcaça de metal da porta USB.
2. Conectar os pinos RX/TX nas vias indicadas no [guia_conexoes_ttl_completo.jpg](fotos%20placa/guia_conexoes_ttl_completo.jpg).
3. Plugar o CP2102 no PC e dar dois cliques em `ABRIR_SERIAL_CP2102.bat`.
4. Com a janela do PuTTY aberta, teclar **ESPAÇO** repetidamente e ligar o projetor na tomada.
5. No prompt `=>`, digitar:
   ```text
   efex
   ```
6. O projetor entrará no modo FEL.
7. Conectar o cabo USB macho-macho e abrir o `ABRIR_PHOENIXSUIT.bat` para regravar o arquivo `firmware/HY300_Pro_Plus_H713.img`.

### Opção 2: Via Botão Físico SMD (Sem Solda)
1. Projetor fora da tomada.
2. Cabo USB macho-macho conectado entre PC e o projetor.
3. PhoenixSuit aberto com a ROM carregada na aba **Firmware**.
4. Pressionar e manter pressionado o microswitch branco ao lado da HDMI com um palito.
5. Ligar a energia na tomada (segurar por 5 segundos).
6. O PhoenixSuit detectará o aparelho e iniciará o flash.
