# Guia de Recuperação (Unbrick): HY300 com slot MicroSD na placa

Métodos em ordem de prioridade **para esta placa** (revisão com módulo `AW869A`, RAM SK Hynix e slot MicroSD; ver [CONTEXTO.md](../CONTEXTO.md)). Cada método diz o que já foi testado e o que é só teoria.

> [!WARNING]
> A imagem `firmware/HY300 Pro+ - H713.img` foi feita para a placa de referência `HY200_QZ713DF_A1`. **Confirme o SoC e o código da placa antes de gravar a eMMC.** Imagem de outra placa pode deixar painel, Wi-Fi ou até a RAM sem funcionar.

---

## 0. Identificar placa e SoC: feito em 03/10/2026

SoC **Allwinner H713 `PA251DA 9B70`**, placa **`M11-REV1.3`**, eMMC Samsung `KLM8G1WEPD-B031`. Detalhes em [CONTEXTO.md](../CONTEXTO.md) §3.
Ordem recomendada agora: **Método F (UART)** para diagnosticar → **Método A (cartão FEL)** → Método B (PhoenixSuit) só se o U-Boot não resolver.

> Ao recolocar o dissipador, use pasta ou pad térmico novo. O H713 sem dissipador superaquece em poucos minutos.

---

## Método A: Cartão FEL no slot MicroSD (recomendado)

**Por que funciona:** o BootROM do Allwinner lê o **cartão SD antes da eMMC**. Já confirmamos que esta placa lê o slot, porque o comportamento muda com o cartão inserido. O stub `fel-sdboot.sunxi` (do sunxi-tools) só faz uma coisa: salta para a rotina FEL do BootROM. Não depende de botão, controle remoto, UART nem do U-Boot corrompido, e **não grava nada na eMMC**.

> Status: **não testado ainda nesta placa.** O stub é usado em vários SoCs Allwinner (salta para o endereço `0x20` do BROM); para o H713 especificamente não há confirmação publicada.

### Preparar o cartão (no notebook)
1. `git pull`.
2. MicroSD no **adaptador USB** (ou no leitor do notebook).
3. Dois cliques em **`CRIAR_CARTAO_FEL.bat`** (pede administrador).
4. Escolha o disco do cartão e digite `SIM`. O script:
   - apaga o cartão e cria uma partição FAT32 começando em 1 MB;
   - grava `tools/fel/fel-sdboot.sunxi` no offset **8 KB (setor 16)**;
   - relê e confere a gravação.

### Usar
1. Instale os drivers FEL no notebook: `tools/instalar_drivers_fel.ps1`.
2. Projetor **fora da tomada**. Cartão FEL no **slot da placa**.
3. Cabo **USB-A macho × USB-A macho** entre o notebook e a porta USB do projetor.
4. Ligue na tomada. O projetor deve ficar "morto" (sem luz/imagem): isso é normal em FEL.
5. No Gerenciador de Dispositivos deve aparecer **`USB\VID_1F3A&PID_EFE8`**.

### Resultados possíveis
| O que acontece | Significado | Próximo passo |
| :--- | :--- | :--- |
| Aparece `VID_1F3A&PID_EFE8` | FEL funcionando | Método B (PhoenixSuit), **se o SoC estiver confirmado** |
| Nada aparece no USB | Cabo/porta (teste outra porta, cabo curto) ou o stub não serve neste SoC | Conferir cabo; voltar ao passo 0 |

---

## Método B: Gravação pelo PhoenixSuit (com o aparelho em FEL)

1. Aparelho em FEL (Método A, ou qualquer outro).
2. `ABRIR_PHOENIXSUIT.bat` → aba **Firmware** → **Image** → selecione a imagem.
3. O PhoenixSuit detecta o FEL e pergunta se quer formatar → **Sim** (*mandatory format*).
4. Não mexa no cabo nem na tomada até `Upgrade Firmware Successfully`.
5. Desligue, **retire o cartão FEL do slot** (senão ele volta para FEL a cada boot), e ligue de novo. O primeiro boot pode levar de 3 a 5 minutos.

Se o PhoenixSuit falhar logo no início (erro de DRAM/`fes`), a imagem não é para este SoC/placa. Pare e procure a imagem certa.

---

## Método C: PhoenixCard (cartão de produção)

- `ABRIR_PHOENIXCARD.bat` → imagem → modo **Product** → **Burn**. Depois coloque o cartão no slot da placa e ligue.
- **Testado em 01–03/10/2026: não funcionou.** O aparelho ficou em standby, sem barra de progresso e sem resposta. Ver hipóteses no CONTEXTO §1.
- Se for tentar de novo: deixe ligado **pelo menos 15–20 min** sem mexer (o gravador de cartão pode não ligar o painel LCD), depois retire o cartão e ligue. Se o comportamento sem cartão mudar, a gravação aconteceu.
- Para devolver o cartão ao uso normal: PhoenixCard → **Format to Normal** (ou `CRIAR_CARTAO_FEL.bat`, que também apaga o cartão).

---

## Método D: Pendrive/SD com `update/auto_update.txt`

- `PREPARAR_CARTAO_MICROSD.bat` cria `update/auto_update.txt` (`sunxi_flash write update/update.img firmware`) + `update/update.img` num pendrive/cartão FAT32.
- **Não confirmado para este U-Boot** e **nunca testado no projetor**. Não está na pesquisa de referência; trate como tentativa de baixa chance.

---

## Método E: Controle remoto IR (`Vol+`)

- Segundo `references/HY300-H713-Research/Boot/BOOT_MODES.md`, o U-Boot **da placa de referência** entra em FEL se `Vol+` for segurado no controle durante a energização (`Home` = recovery com wipe).
- Depende do U-Boot da eMMC estar íntegro e ser igual ao da referência.
- **Testado nesta placa: não entrou em FEL** (receptor IR traseiro original sempre esteve soldado). Possíveis motivos: o U-Boot desta placa não tem o atalho, ou nem chega a rodar.
- Esta placa tem **dois pontos de receptor IR**: os 3 furos no canto P2/cooler (receptor traseiro) e o conector `遥控头接口` (cabo para o sensor frontal). Antes do teste, confirme que pelo menos um receptor está **soldado na orientação certa** (cúpula para fora da placa, como no original). Aponte o controle para ele.
- Para conferir se o controle emite: aponte para a câmera do celular e aperte um botão. O LED deve piscar na tela.
- Sequência: cabo USB-A×A no PC → segure `Vol+` apontado para o receptor → ligue na tomada → mantenha por ~5 s.

### Variante: alimentar a placa só pela USB do PC + botão Power
- Um relato de outra placa H713 ([gist probonopd/HY300_PRO.md](https://gist.github.com/probonopd/3ad6b7777caea1503f00d5fe7710ad06)) entra em FEL assim: projetor **fora da tomada**, cabo USB-A×A no PC, apertar o botão Power.
- Esta placa é alimentada em 5 V, então a USB do PC pode conseguir ligar a lógica (o LED da lâmpada não acende, porque usa os 27 V da fonte).
- **Não confirmado nesta placa.** Custo zero de testar: veja se aparece `VID_1F3A&PID_EFE8`.

---

## Método F: Console UART (CP2102)

- 3,3 V TTL, 115200 8-N-1. Ligações: GND na carcaça do USB/HDMI, RX do módulo no TX da placa, TX do módulo no RX da placa, **VCC desligado**.
- No prompt `=>` do U-Boot: `efex` (vai para FEL), `printenv` (mostra slot/variáveis).
- Os **3 furos do canto P2/cooler são do receptor IR traseiro** (confirmado em 03/10/2026), não da UART.
- Candidato que sobra: 4 pads redondos em fila ao lado da eMMC, na face inferior (`fotos placa/fotos 0310/pads_teste_verso.jpg`). Identificação no [roteiro de bancada](ROTEIRO_PRATICO_BANCADA_CP2102.md).
- As fotos `marked_uart_pads.jpg` da pesquisa são da placa de referência; não valem para esta.

---

## Método G: Curto na eMMC (último recurso)

Encostar CLK ou DAT0 da eMMC ao GND durante a energização faz o BootROM falhar na eMMC e cair em FEL.
**Nesta placa não é necessário:** o slot MicroSD (Método A) faz o mesmo sem risco de danificar trilhas. Só use se o Método A não der FEL e você souber exatamente os pinos da eMMC.

---

## Depois de recuperar

1. **Backup da eMMC inteira** antes de qualquer outra mudança (`references/HY300-H713-Research/Firmware/EMMC_DUMPING.md`: via ADB sem root).
2. Desative as atualizações OTA do fabricante para não repetir o brick.
