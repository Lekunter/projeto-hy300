# Firmwares e ROMs stock: HY300

## 1. Imagem disponível neste repositório

| Arquivo | Tamanho | Formato | Origem | Placa-alvo |
| :--- | :--- | :--- | :--- | :--- |
| `HY300 Pro+ - H713.img` | 1,91 GB | Allwinner `IMAGEWTY` (PhoenixSuit/PhoenixCard) | Google Drive da comunidade (link abaixo) | `HY200_QZ713DF_A1` (H713, AIC8800D40) |

- Versionada com **Git LFS** (`.gitattributes`: `*.img`). Numa máquina nova: `git lfs install` e depois `git lfs pull`.
- Se o GitHub recusar por cota de LFS, publique o `.img` como anexo de uma **Release** em vez do LFS. Ou copie pelo Google Drive Desktop (`G:\Meu Drive`).
- `gdrive_dumps/` guarda um download parcial antigo (`.part`), ignorado pelo Git e que pode ser apagado.

> [!WARNING]
> **Esta imagem não foi feita para a placa deste aparelho.** Ele tem módulo `AW869A`, RAM SK Hynix e slot MicroSD (ver [CONTEXTO.md](../CONTEXTO.md) §3). A imagem já foi gravada num cartão PhoenixCard (modo Product) e **não recuperou** o aparelho. Antes de gravar a eMMC, confirme o SoC e procure uma imagem para o código da sua placa.

> [!WARNING]
> Nunca grave imagens de variantes Rockchip (RK3326-S) ou H726 numa placa H713, nem o contrário.

---

## 2. Links catalogados

### A. Google Drive (r/Magcubic / XDA): fonte da imagem atual
- [HY300 Pro+ H713: firmwares e dumps](https://drive.google.com/drive/folders/11P8tCMqPl8iK4V_BhmMEbqv8EnB4je0i)
- O download pelo terminal (`gdown`) é limitado a ~50–70 KB/s; baixe pelo navegador.

### B. Mega (4PDA / Hotack OEM): pacote `HY300Pro+_en_MAGCUBIC_202507211739`
- [Link 1](https://mega.nz/file/ipmijk6wxPxjeXac0-gtFBc) · [Link 2](https://mega.nz/file/nxDmjhMG_IPMhE0Rikt78Z4) · [Link 3](https://mega.nz/file/C0qqFF8mILaCW9TGFWpItrI) · [Link 4](https://mega.nz/file/uaQqpDXhoH0pLqVvIJJDcaY)
- Os links foram catalogados pelo agente anterior e **não foram verificados** (os links do Mega sem a chave `#...` não abrem).

### C. O que procurar para esta placa
- Busque pelo **código serigrafado da PCB** + "firmware" no 4PDA (tópico HY300), r/Magcubic e XDA.
- Termos úteis: `HY300 AW869A firmware`, `HY300 H713 TF card slot`, o código da etiqueta da placa.

### D. Debloat / root
- `references/magcubic-root/awimg.py` desempacota e reempacota `IMAGEWTY`. Também serve para **inspecionar o `sys_config.fex`** da imagem (painel, DRAM, Wi-Fi) e comparar com a placa.
