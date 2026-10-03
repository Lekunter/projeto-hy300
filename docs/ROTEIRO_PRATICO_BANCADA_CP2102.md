# Roteiro Prático de Bancada: Recuperação do HY300 com CP2102

Roteiro da bancada para usar o console serial (UART).

> [!IMPORTANT]
> **Status (03/10/2026):** nesta placa os pads TX/RX **não têm serigrafia e não foram encontrados**. A placa também não tem botão de reset/FEL. Para entrar em FEL, prefira o **cartão FEL no slot MicroSD** ([GUIA_RECUPERACAO.md](GUIA_RECUPERACAO.md), Método A). Este roteiro continua útil para ver o log de boot, se os pads forem achados.

---

## 📋 Checklist de Ferramentas na Bancada

- [ ] Projetor HY300 / HY300 Pro (desconectado da tomada).
- [ ] Cabo de energia original do projetor.
- [ ] Cabo USB-A Macho para USB-A Macho.
- [ ] Módulo conversor USB-Serial **CP2102**.
- [ ] 3 cabinhos / jumpers finos (ou fios esmaltados).
- [ ] Ferro de solda e estanho (ou fita para fixação temporária firme).
- [ ] Chave Philips pequena para abrir a carcaça.
- [ ] Multímetro digital.
- [ ] Computador com o projeto em `D:\hy300\projeto-hy300`.

---

## ⚠️ PASSO 0: Configuração de Segurança do CP2102 (CRÍTICO)

Antes de plugar qualquer fio no projetor:
1. Olhe para a placa do seu **CP2102**. A maioria dos módulos possui um jumper ou 3 pads com solda marcados com **`3.3V`** e **`5V`**.
2. **GARANTA que o módulo está configurado em `3.3V`**.
   > [!CAUTION]
   > O processador Allwinner H713 opera em 3.3V. Se o CP2102 enviar 5V nos pinos RX/TX, a porta serial do processador pode queimar permanentemente.
3. **Pino VCC (Alimentação):** **NÃO CONECTE O VCC DO CP2102 NO PROJETOR**. O projetor recebe energia de sua própria fonte. Você só vai conectar 3 fios: **TX, RX e GND**.

---

## 🪛 PASSO 1: Abertura da Carcaça e Localização dos Pads

1. Retire os parafusos na base e na carcaça plástica cilíndrica do projetor.
2. Separe as duas metades da carcaça com cuidado para não romper os fios do alto-falante nem o cabo flat do display LCD.
3. Localize a placa-mãe principal. Na placa de referência (`HY200_QZ713DF_A1`) os pads `TX`/`RX` são serigrafados ao lado do SoC (`references/HY300-H713-Research/Hardware/marked_uart_pads.jpg`). **Nesta placa não há serigrafia.**
4. Para achar o TX com o multímetro (escala DC 20 V, ponta preta na carcaça do USB):
   - Com a placa ligada, procure vias/pads de teste perto do SoC que fiquem em **~3,3 V** em repouso.
   - O **TX** cai e oscila por alguns segundos logo após ligar na tomada (o bootloader está imprimindo log). Num multímetro isso aparece como um valor tremendo entre 2,5 e 3,3 V.
   - Confirme ligando o **RX do CP2102** nesse ponto com o PuTTY aberto: devem aparecer textos legíveis (`HELLO! BOOT0`, `U-Boot …`).
   - O RX da placa costuma ficar ao lado do TX, também em ~3,3 V, mas sem oscilar.

---

## 🔌 PASSO 2: Ligação Elétrica (CP2102 <-> Placa do Projetor)

Faça a ligação cruzada dos sinais:

| Pino no Módulo CP2102 | Ponto de Conexão no Projetor HY300 | Observação |
| :--- | :--- | :--- |
| **GND** | **Carcaça metálica da porta USB ou HDMI** | Solde ou prenda firmemente na lata externa do conector |
| **RX** | Pad marcado como **`TX`** na placa | O que o projetor envia, o CP2102 recebe |
| **TX** | Pad marcado como **`RX`** na placa | O que o CP2102 envia, o projetor recebe |
| **3V3 / 5V (VCC)** | **NÃO LIGAR NADA** | O projetor usará sua fonte própria |

*(Dica de solda: Dê apenas um pingo minúsculo de solda na ponta de cada fio sobre o pad. Não aplique calor por mais de 2 segundos no pad para não soltá-lo da placa).*

---

## 💻 PASSO 3: Conexão no Computador e Abertura do Terminal

1. Conecte o cabo **USB-A Macho x Macho** entre o PC e a porta USB do projetor.
2. Conecte o módulo **CP2102** em outra porta USB do computador.
3. No computador, abra o PowerShell na pasta do projeto e execute nosso script automático:
   ```powershell
   cd D:\hy300\projeto-hy300\tools
   .\abrir_serial_cp2102.ps1
   ```
   *(O script detectará a porta COM do CP2102 e abrirá o PuTTY já configurado em 115200 bps, 8-N-1).*

---

## ⚡ PASSO 4: Interrompendo o Bootloader (U-Boot)

1. Com a janela preta do PuTTY aberta na tela do PC:
2. **Ligue o cabo de energia do projetor na tomada.**
3. No mesmo segundo em que ligar a energia, **comece a apertar a barra de espaço ou Enter repetidamente** no teclado do computador.
4. O U-Boot imprimirá mensagens de inicialização do sistema na tela e interromperá a contagem regressiva (`Hit any key to stop autoboot`).
5. Você verá o terminal parar exatamente neste prompt de comando interativo:
   ```text
   =>
   ```

*(Se o terminal exibir caracteres estranhos ou ilegíveis, verifique se a velocidade está em 115200 e se o GND está bem fixado).*

---

## 🚀 PASSO 5: Forçando o Modo FEL e Gravando a ROM

Agora o processador está sob o seu controle total:

1. No prompt `=>` do PuTTY, digite o comando e aperte Enter:
   ```text
   efex
   ```
2. **O que vai acontecer imediatamente:**
   - O processador H713 reiniciará instantaneamente em **Modo USB FEL**.
   - O Windows emitirá o som característico de dispositivo USB plugado (`USB\VID_1F3A&PID_EFE8`).
3. Abra a ferramenta que deixamos pronta:
   `D:\hy300\projeto-hy300\tools\PhoenixSuit\PhoenixSuit v1.10\PhoenixSuit.exe`
4. No PhoenixSuit:
   - Clique na aba **Firmware**.
   - Clique em **Image** e selecione a imagem **correta para a placa** (a atual é `firmware/HY300 Pro+ - H713.img`, feita para a placa de referência; ver `firmware/README.md`).
   - O PhoenixSuit detectará o projetor em modo FEL e exibirá uma caixa de diálogo perguntando se deseja formatar:
     `Tips: Does mandatory format?` -> Clique em **Sim (Yes)**.
5. A barra de progresso verde começará a avançar no PhoenixSuit:
   - Ela regrava a GPT, restaura o Slot A íntegro e zera o erro do Slot B.
   - **NÃO desconecte o cabo USB nem a tomada durante o processo.**
6. Ao chegar em 100%, o PhoenixSuit exibirá `Upgrade Firmware Successfully!`.

---

## 🏁 PASSO 6: Primeiro Boot e Teste

1. Desconecte o cabo USB-A do computador.
2. Desconecte o cabo de energia do projetor por 10 segundos.
3. Reconecte a energia do projetor na tomada.
4. Ligue o projetor pelo botão power ou controle.
5. **Paciência no primeiro boot:** Como a memória eMMC foi formatada limpa, o primeiro boot do Android 11 demora entre **3 a 5 minutos** (o cooler vai girar e a lâmpada acenderá).
6. O sistema iniciará na tela inicial de configuração de fábrica!
7. Desolde os fios do CP2102 e feche a carcaça plástica.
