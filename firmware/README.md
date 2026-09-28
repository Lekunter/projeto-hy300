# Repositório de Firmwares e ROMs Stock — HY300 (Allwinner H713)

Este diretório é o destino para os arquivos de imagem de firmware (`.img`) necessários para a regravação via PhoenixSuit, PhoenixUSBPro ou pelo método de atualização automática por pendrive USB.

---

## 1. Identificação Crítica de Hardware

Antes de gravar qualquer imagem, confirme a identificação da sua placa e componentes:
- **SoC:** Allwinner H713 (`sun50iw12p1` / plataforma TV303)
- **Código da Placa-Mãe:** `HY200_QZ713DF_A1`
- **Etiqueta de Fábrica Típica:** `DW1G+8G+20800D4` (1GB RAM + 8GB eMMC + Wi-Fi AIC8800D40)
- **Chip Wi-Fi/BT:** AicSemi AIC8800D40 (Wi-Fi 6 + Bluetooth 5.4)

> [!WARNING]
> Nunca grave firmwares de variantes Rockchip (RK3326-S) ou de chips H726 nesta placa, sob risco de hard brick irreversível ou perda de vídeo e controle remoto.

---

## 2. Links de Download Catalogados

### A. Firmwares Oficiais da Placa `HY200_QZ713DF_A1` (Fonte: Comunidade 4PDA / Hotack OEM)
Compatíveis com os lotes padrão do Magcubic HY300 / HY300 Pro com placa `HY200_QZ713DF_A1`:

* **Pasta Mega (Lote Magcubic HY300 Pro+ / HY300 H713):**
  - Pacote completo: `HY300Pro+_en_MAGCUBIC_202507211739`
  - Link 1: [Mega.nz - Pacote Firmware 1](https://mega.nz/file/ipmijk6wxPxjeXac0-gtFBc)
  - Link 2: [Mega.nz - Pacote Firmware 2](https://mega.nz/file/nxDmjhMG_IPMhE0Rikt78Z4)
  - Link 3: [Mega.nz - Pacote Firmware 3](https://mega.nz/file/C0qqFF8mILaCW9TGFWpItrI)
  - Link 4: [Mega.nz - Pacote Firmware 4](https://mega.nz/file/uaQqpDXhoH0pLqVvIJJDcaY)

### B. Dumps Completos de eMMC e Imagens Stock H713 (Google Drive)
* **Repositório Google Drive (Comunidade Reddit r/Magcubic / XDA Developers):**
  - Contém dumps íntegros de eMMC, partições individuais e imagens prontas para flash:
  - Link: [Google Drive - HY300 Pro+ H713 Firmwares & Dumps](https://drive.google.com/drive/folders/11P8tCMqPl8iK4V_BhmMEbqv8EnB4je0i)

### C. Firmwares Debloated e com Root Pré-instalado
* **Firmware com Magisk + Bloatwares Removidos:**
  - Caso queira gerar uma ROM limpa sem os cavalos de troia / malwares de fábrica (`com.hotack.silentsdk` e `com.htc.eventuploadservice`), use o utilitário incluído no projeto:
  - Local da ferramenta: `references/magcubic-root/awimg.py`

---

## 3. Instruções de Armazenamento Local

Ao baixar a imagem (`.img`), salve o arquivo neste diretório com um nome claro, por exemplo:
- `firmware/HY300_H713_STOCK.img`

Caso vá utilizar o **Método do Pendrive Automático**, renomeie uma cópia do arquivo para:
- `firmware/update.img`
