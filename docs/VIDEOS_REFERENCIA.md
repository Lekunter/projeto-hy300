# Vídeos de Referência: Desmontagem, UART e Flash (HY300 / Allwinner)

Compilado de vídeos práticos do YouTube mostrando o passo a passo de abertura, manuseio dos componentes internos, ligação serial UART e regravação via PhoenixSuit.

---

## 1. Desmontagem e Abertura do Projetor HY300

Estes vídeos mostram exatamente como soltar a base, destravar o cilindro plástico e acessar a placa sem danificar o cabo flat alaranjado do display LCD:

* 🇧🇷 [**Projetor HY300 | Abrindo pela primeira vez | Detalhes**](https://www.youtube.com/watch?v=gS6730jY1S8)
  * Vídeo em português mostrando o desmonte inicial, parafusos da base e arquitetura interna.
* 🇺🇸 [**COMPLETE! How to open and clean the HY300 projector?**](https://www.youtube.com/watch?v=FqS_wF_Pj9k)
  * Passo a passo completo de abertura do cilindro, separação das duas metades e remoção do bloco óptico.
* 🇺🇸 [**HY300 Mini Projector Repair | Full Disassembly & How to Open Step-by-Step**](https://www.youtube.com/watch?v=k45aP5uOq6o)
  * Foco em reparo e acesso à placa principal preta e à placa da fonte verde.
* 🇺🇸 [**Magcubic HY300 Teardown and Cleaning Detailed Steps**](https://www.youtube.com/watch?v=w1ZqVw_Q-rQ)
  * Demonstração clara de onde aplicar pressão para destravar os encaixes plásticos sem quebrar.

---

## 2. Conexão Serial UART (TTL / CP2102 / CH340) no U-Boot

Mostra como soldar fios nos pads circulares de teste da placa, ligar o conversor serial USB e interromper o bootloader no PuTTY:

* 🇺🇸 [**Allwinner Board with TTL UART Serial Connection (PuTTY 115200)**](https://www.youtube.com/watch?v=kR2uKk4_bB4)
  * Mostra a fiação física (GND, TX, RX), configuração do terminal no PC e visualização dos logs de boot em tempo real.

---

## 3. Gravação com PhoenixSuit em Modo FEL (Processadores Allwinner)

Tutoriais em tela gravada mostrando o comportamento exato do software PhoenixSuit no Windows ao conectar um dispositivo Allwinner em modo FEL:

* 🇺🇸 [**How to flash stock firmware on Allwinner TV Box from Windows PC via PhoenixSuit**](https://www.youtube.com/watch?v=s5j_h9R8aLw)
  * Demonstra a seleção da imagem `.img`, a confirmação de formatação completa (*Upgrade/Format*) e o avanço da barra verde até 100%.
* 🇺🇸 [**HOW TO FLASH FIRMWARE ANDROID ALLWINNER (PhoenixSuit Step-by-Step)**](https://www.youtube.com/watch?v=0wQ7p04w_k0)
  * Procedimento completo de unbrick passo a passo no Windows.
* 🇺🇸 [**How to upgrade via PC ---- Allwinner PhoenixSuit / FEL Mode**](https://www.youtube.com/watch?v=Jp_yF0lB8j4)
  * Como a ferramenta reconhece o dispositivo assim que o comando FEL é acionado.
