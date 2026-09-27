# Projeto HY300 — Recuperação e Firmware (Allwinner H713)

Repositório dedicado à recuperação de soft brick, documentação técnica, ferramentas de regravação e referências de firmware para o projetor smart **HY300 / HY300 Pro** baseado no processador **Allwinner H713** (`sun50iw12p1`).

## 📁 Estrutura do Repositório

- `CONTEXTO.md`: Relatório técnico detalhado contendo a arquitetura de boot, causa raiz do soft brick pós-OTA (particionamento Virtual A/B fake), gatilhos para modo FEL e procedimentos de unbrick.
- `/firmware`: *(Local reservado para arquivos de imagem .img e dumps)*
- `/tools`: *(Local reservado para instaladores do PhoenixSuit, LiveSuit e drivers USB)*

## ⚙️ Especificações Rápidas

- **SoC:** Allwinner H713 Quad-Core Cortex-A53
- **GPU:** Mali-G31 MP2
- **RAM:** 1GB DDR3
- **Armazenamento:** 8GB eMMC
- **Wi-Fi / BT:** AIC8800D40 (Wi-Fi 6 + Bluetooth 5.4)
- **ID USB FEL:** `VID_1F3A&PID_EFE8`

## 🛠️ Guia Rápido de Recuperação

Consulte o documento [CONTEXTO.md](CONTEXTO.md) para o passo a passo completo de conexão e regravação via **PhoenixSuit**.
