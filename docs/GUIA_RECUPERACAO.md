# Guia Completo de Recuperação (Unbrick) — HY300 / HY300 Pro (Allwinner H713)

Este documento detalha todos os métodos práticos e laboratoriais conhecidos para reviver o projetor **HY300 / HY300 Pro** (marcas Magcubic, Transpeed ou genéricas) baseado no chip **Allwinner H713** (`sun50iw12p1` / placa `HY200_QZ713DF_A1`) após soft brick por atualização OTA.

---

## 1. Entendendo o Brick

* **Sintoma:** O aparelho acende o LED de status, o cooler/ventilador gira, a lâmpada LED pode ou não acender, mas não há imagem ou o sistema trava indefinidamente na logo inicial.
* **Causa Raiz:** O fabricante Hotack configurou uma tabela GPT com Virtual A/B "falsa". O sistema ativo é o **Slot A**. As partições do **Slot B** são blocos vazios preenchidos com zeros (`0x00`). Quando a atualização OTA oficial é aplicada, o Android grava no Slot B e troca o slot de boot no U-Boot. Ao reiniciar, o processador tenta inicializar um sistema vazio, resultando em falha imediata.

---

## 2. Método 1: Unbrick Autônomo via Pendrive USB (Sem PC / Sem Cabos Especiais)

Este é o método mais rápido e não invasivo. Ele aproveita a rotina de recuperação embutida no U-Boot do Allwinner:

### Requisitos:
* 1 Pendrive USB comum (de 4GB a 32GB).
* Arquivo de firmware stock `.img` (localizado em `firmware/`).

### Procedimento Passo a Passo:
1. Formate o pendrive em **FAT32** (tamanho de alocação padrão).
2. Crie uma pasta na raiz chamada exatamente `update` (em letras minúsculas).
3. Dentro da pasta `update`, crie um arquivo de texto chamado `auto_update.txt` com a seguinte linha exata:
   ```text
   sunxi_flash write update/update.img firmware
   ```
4. Copie o arquivo da ROM `.img` para dentro da pasta `update` e renomeie-o para `update.img` (tudo em minúsculas).
   *(Alternativa automatizada: basta executar o script `tools/preparar_pendrive_update.ps1` no PowerShell).*
5. Desconecte o cabo de energia da tomada do projetor.
6. Insira o pendrive na porta USB do HY300.
7. Ligue o cabo de energia na tomada. **NÃO pressione o botão de ligar**.
8. O U-Boot detectará o arquivo de comando no pendrive e iniciará a projeção de uma tela de regravação com barra de progresso verde.
9. Aguarde o término completo (100%).
10. Desconecte da tomada, **remova o pendrive** (caso contrário ele regravará no próximo boot) e ligue o projetor normalmente.

---

## 3. Método 2: Regravação via PC (Modo FEL / USB-A x USB-A)

Utilizado quando o U-Boot estiver corrompido ou não ler o pendrive. O chip Allwinner possui um modo de baixo nível em ROM pura (**Modo FEL**, `USB\VID_1F3A&PID_EFE8`) que permite injetar código e regravar a eMMC diretamente do computador.

### Requisitos:
* Cabo **USB-A Macho para USB-A Macho** de boa qualidade.
* Computador com Windows.
* Software **PhoenixSuit** (já extraído em `tools/PhoenixSuit/`) ou **PhoenixUSBPro**.
* Drivers Allwinner USB FEL instalados (execute `tools/instalar_drivers_fel.ps1`).

### Procedimento Passo a Passo:
1. Abra o arquivo executável:
   `tools/PhoenixSuit/PhoenixSuit v1.10/PhoenixSuit.exe`
2. No PhoenixSuit, clique na aba **Firmware** e selecione o arquivo `.img` da ROM.
3. Desconecte a energia do projetor.
4. Conecte uma ponta do cabo USB-A na porta USB do PC e a outra na porta USB do projetor.
5. **Gatilho do Modo FEL:**
   * **Opção com Botão Físico (Mais confiável):** Localize o pequeno orifício sob a porta HDMI (ou dentro do conector de áudio P2). Com um palito de dente não metálico ou clipe de papel fino, sinta o clique do botão interno e **mantenha-o pressionado**.
   * Conecte o cabo de energia do projetor na tomada mantendo o botão pressionado por cerca de 3 a 5 segundos e solte.
   * **Opção com Controle Remoto IR:** Aponte o controle remoto para o receptor do projetor e fique apertando repetidamente a tecla **Volume + (Vol+)** ao conectar o cabo de energia na tomada.
6. O Windows emitirá o som de dispositivo USB conectado e o Gerenciador de Dispositivos exibirá `USB Device(VID_1f3a_PID_efe8)`.
7. O PhoenixSuit exibirá uma janela de confirmação perguntando se deseja formatar a partição (**Upgrade / Format**). Confirme com **Sim**.
8. A regravação será iniciada. Não desconecte o cabo USB nem a energia.
9. Ao concluir (100%), desconecte o cabo USB e reinicie o aparelho. O primeiro boot leva entre 3 e 5 minutos.

---

## 4. Método 3: Depuração e Controle via Console Serial (UART)

Caso o projetor continue não respondendo ou deseje inspecionar exatamente o ponto de falha do boot:

### Pinagem na Placa-Mãe (`HY200_QZ713DF_A1`):
* **Pads de Teste UART:** Localizados próximos ao processador H713 e dissipador térmico (veja fotos em `references/HY300-H713-Research/Hardware/`).
* **TX da Placa:** Conectar no pino **RX** de um conversor USB-Serial (FTDI, CP2102, CH340).
* **RX da Placa:** Conectar no pino **TX** do conversor USB-Serial.
* **GND:** Pode ser soldado ou aterrado na carcaça externa metálica da porta USB ou HDMI.
* **Nível Lógico:** 3.3V (Não use 5V!).
* **Configuração:** 115200 baud, 8 bits de dados, sem paridade, 1 stop bit (8-N-1).

### Comandos de Resgate no U-Boot:
Ao ligar a energia com o terminal aberto (PuTTY / TeraTerm), pressione qualquer tecla repetidamente para interromper a contagem do boot:
1. **Forçar Modo FEL via software:**
   ```text
   => efex
   ```
   *(O projetor entrará imediatamente no modo USB FEL para o PhoenixSuit).*
2. **Iniciar modo Fastboot:**
   ```text
   => fastboot
   ```
3. **Verificar variáveis de ambiente e slots:**
   ```text
   => printenv
   ```

---

## 5. Método 4: Forçamento de FEL via Curto de Barramento eMMC (Hard Unbrick)

Em casos raros em que o bootloader entra em loop antes de verificar os botões de recuperação, o processador possui uma lógica de inicialização de hardware:
1. O BootROM tenta ler sucessivamente: SD Card -> eMMC -> SPI -> **Modo FEL**.
2. Se a leitura do eMMC falhar, o chip Allwinner cai **obrigatoriamente** no modo USB FEL.
3. Para simular falha de leitura e forçar o Modo FEL:
   * Com o aparelho desligado, use uma pinça ou agulha fina para fechar um curto momentâneo entre a linha de clock (`CLK`) ou dados (`DAT0`) do chip eMMC Kioxia (`THGBMHG6C1LBAIL`) e o terra (`GND`).
   * Ligue a alimentação do aparelho com o cabo USB-A conectado ao PC.
   * Remova o curto após 1 segundo.
   * O computador reconhecerá o dispositivo em modo `VID_1F3A&PID_EFE8` de fábrica.
