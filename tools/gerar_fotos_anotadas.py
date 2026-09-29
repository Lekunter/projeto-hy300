#!/usr/bin/env python3
"""
Script de Geracao de Fotos Anotadas da Placa do Projetor HY300 (Allwinner H713)
Compara a placa fisica do usuario com a base de engenharia reversa e Teardown (HY200_QZ713DF_A1)
e gera 4 guias visuais de alta resolucao em fotos_anotadas/.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Diretorios
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOTOS_PLACA_DIR = os.path.join(BASE_DIR, "fotos placa")
OUTPUT_DIR = os.path.join(BASE_DIR, "fotos_anotadas")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_font(size, bold=False):
    font_names = (
        ["arialbd.ttf", "segoeuib.ttf", "calibrib.ttf"]
        if bold
        else ["arial.ttf", "segoeui.ttf", "calibri.ttf"]
    )
    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            pass
    try:
        font_path = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def draw_badge(draw, cx, cy, radius, text, bg_color, text_color=(255, 255, 255), font=None):
    """Desenha um circulo com borda e texto centralizado (numero ou sigla do componente)."""
    draw.ellipse([cx - radius + 3, cy - radius + 3, cx + radius + 3, cy + radius + 3], fill=(0, 0, 0, 140))
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=bg_color, outline=(255, 255, 255, 220), width=3)
    if font:
        bbox = font.getbbox(text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((cx - tw // 2, cy - th // 2 - 2), text, fill=text_color, font=font)

def draw_rounded_card(draw, x1, y1, x2, y2, r, fill, outline=None, width=1):
    """Desenha retangulo arredondado."""
    draw.rounded_rectangle([x1, y1, x2, y2], radius=r, fill=fill, outline=outline, width=width)

# ==============================================================================
# FOTO 1: VISAO GERAL DA PLACA PRINCIPAL
# ==============================================================================
def gerar_foto_1():
    print("Gerando Foto 1: Visao Geral da Placa Principal...")
    raw_path = os.path.join(FOTOS_PLACA_DIR, "IMG_0355_rot90cw.jpg")
    im_raw = Image.open(raw_path)
    
    board_crop = im_raw.crop((750, 1600, 2800, 3750)) # 2050 x 2150
    bw, bh = board_crop.size

    overlay = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)

    components = [
        (1, "SoC Allwinner H713", (660, 690, 1440, 1530), (239, 68, 68),
         "Processador Central e Grafico", "Allwinner H713 (sun50iw12p1)",
         "Quad-Core ARM Cortex-A53 a 1.5GHz + GPU Mali-G31 MP2. Sob dissipador de aluminio preto.",
         "Identico a referencia; porem na referencia o dissipador foi retirado para inspecao."),
        
        (2, "Memoria RAM DDR3 (512MB Top)", (700, 290, 1330, 650), (59, 130, 246),
         "2x CIs de Memoria RAM DDR3", "SK Hynix H5TQ2G83CFR PBC 213V",
         "2x 256MB = 512MB na face superior (total 1GB combinando com face inferior).",
         "DIFERENCA: Sua placa usa SK Hynix; a placa de referencia usava chips Elpida."),
        
        (3, "Modulo Wi-Fi 6 + Bluetooth 5.x", (1130, 1600, 1450, 1950), (16, 185, 129),
         "Conectividade Sem Fio de Alta Velocidade", "Allwinner / Fn-Link AW869A",
         "Wi-Fi 6 802.11ax dual-band + Bluetooth 5.2/5.4 com conector coaxial IPEX/U.FL acoplado.",
         "DIFERENCA: Na sua placa fica na FACE SUPERIOR (AW869A); na referencia usava AIC8800D40 no VERSO!"),
         
        (4, "Porta USB 2.0 / OTG (Modo FEL)", (200, 1050, 560, 1470), (245, 158, 11),
         "Porta de Flash e Perifericos", "USB 2.0 Tipo-A Receptacle",
         "Conecta pen-drives e aceita cabo Macho-Macho para gravacao de firmware via PhoenixSuit.",
         "Porta identica a referencia; fundamental para o resgate do projetor."),
         
        (5, "Porta HDMI Entrada", (170, 500, 490, 950), (217, 119, 6),
         "Entrada de Video Digital Externo", "HDMI Type-A 19 pinos",
         "Receptor digital conectado diretamente aos pinos de entrada de video do SoC H713.",
         "Identica a referencia de engenharia."),
         
        (6, "Saida de Audio P2 (3.5mm)", (270, 1500, 610, 1800), (168, 85, 247),
         "Jack de Fone de Ouvido / Auxiliar", "Conector P2 Femea 3.5mm",
         "Saida estereo analogica para fones de ouvido ou caixa de som externa.",
         "DIFERENCA: Populada na sua placa! Na placa de referencia, esse jack estava vazio."),
         
        (7, "Botao Microswitch FEL / U-BOOT", (250, 220, 430, 360), (234, 179, 8),
         "Botao Fisico de Recuperacao de Fabrica", "SMD Tactile Microswitch",
         "Forca o BootROM do SoC para o modo FEL (1f3a:efe8) quando mantido pressionado ao plugar na energia/USB.",
         "DIFERENCA CRUCIAL: Sua placa TEM BOTAO FISICO SOLDADO! Permite entrar em FEL sem solda nem curto!"),
         
        (8, "Conector da Ventoinha (FAN)", (680, 1670, 890, 1980), (6, 182, 212),
         "Cooler de Exaustao e Refrigeracao", "Silkscreen: Fan / Refrigeração",
         "Alimentacao 5V e controle de rotacao PWM para a turbina de refrigeracao da lampada LED.",
         "Identico a referencia de engenharia."),
         
        (9, "Conector de Alimentacao 5V / 2A", (1480, 360, 1750, 720), (225, 29, 72),
         "Entrada de Energia da Placa Logica", "Silkscreen: 5V Alimentação DC",
         "Recebe tensao continua DC de 5V da placa de fonte (fios vermelho e preto).",
         "Identico a referencia de engenharia."),
         
        (10, "Conector Alto-Falante (SPK)", (400, 230, 620, 420), (236, 72, 153),
         "Audio Interno Amplificado", "Header 2 pinos JST",
         "Conecta o alto-falante acustico embutido acionado pelo amplificador XA8870C.",
         "Identico a referencia de engenharia."),
         
        (11, "Conector Display LCD (FFC 40p)", (1560, 780, 1750, 1310), (249, 115, 22),
         "Barramento Digital do Painel LCD", "Conector FFC 40 vias com trava",
         "Transmite sinais digitais MIPI/LVDS de imagem para o display transmissivo de projecao.",
         "Identico a referencia de engenharia."),
         
        (12, "Receptor Infravermelho (IR)", (1560, 1370, 1820, 1650), (132, 204, 22),
         "Sensor do Controle Remoto", "Silkscreen: Receptor IR Remoto",
         "Chicote de 3 fios para o fotoreceptor IR frontal responsavel pelos comandos do controle.",
         "Identico a referencia de engenharia.")
    ]

    for num, name, box, col, _, _, _, _ in components:
        ov_draw.rectangle(box, fill=(col[0], col[1], col[2], 65))
        ov_draw.rectangle(box, outline=(col[0], col[1], col[2], 255), width=6)
        cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2
        if box[3] - box[1] < 200 or box[2] - box[0] < 200:
            bx, by = box[0] + 30, box[1] + 30
        else:
            bx, by = cx, cy
        draw_badge(ov_draw, bx, by, 32, str(num), (col[0], col[1], col[2], 240), font=get_font(28, bold=True))

    board_annotated = Image.alpha_composite(board_crop.convert("RGBA"), overlay).convert("RGB")

    sidebar_w = 1400
    canvas_w = bw + sidebar_w
    canvas_h = bh
    canvas = Image.new("RGB", (canvas_w, canvas_h), color=(15, 23, 42))
    canvas.paste(board_annotated, (0, 0))

    draw = ImageDraw.Draw(canvas)
    draw.line([(bw, 0), (bw, canvas_h)], fill=(51, 65, 85), width=3)

    # Header
    draw.rectangle([bw, 0, canvas_w, 140], fill=(30, 41, 59))
    draw.line([(bw, 140), (canvas_w, 140)], fill=(59, 130, 246), width=4)
    
    font_main_title = get_font(38, bold=True)
    font_sub_title = get_font(22, bold=False)
    font_card_title = get_font(23, bold=True)
    font_card_sub = get_font(18, bold=True)
    font_card_body = get_font(18, bold=False)
    font_card_diff = get_font(17, bold=True)

    draw.text((bw + 40, 25), "GUIA DE IDENTIFICAÇÃO DE HARDWARE", fill=(255, 255, 255), font=font_main_title)
    draw.text((bw + 40, 80), "Placa Principal HY300 (Allwinner H713) vs Teardown Base de Dados", fill=(148, 163, 184), font=font_sub_title)

    col_w = (sidebar_w - 60) // 2
    card_h = 310
    start_y = 160
    
    for i, (num, name, _, col, det_title, chip_ref, funcao, diff_ref) in enumerate(components):
        col_idx = i // 6
        row_idx = i % 6
        
        cx1 = bw + 20 + col_idx * (col_w + 15)
        cy1 = start_y + row_idx * (card_h + 15)
        cx2 = cx1 + col_w
        cy2 = cy1 + card_h
        
        draw_rounded_card(draw, cx1, cy1, cx2, cy2, 12, fill=(30, 41, 59), outline=(col[0], col[1], col[2]), width=2)
        
        draw.ellipse([cx1 + 14, cy1 + 14, cx1 + 54, cy1 + 54], fill=col)
        bbox_num = get_font(24, bold=True).getbbox(str(num))
        nw = bbox_num[2] - bbox_num[0]
        nh = bbox_num[3] - bbox_num[1]
        draw.text((cx1 + 34 - nw//2, cy1 + 34 - nh//2 - 2), str(num), fill=(255, 255, 255), font=get_font(24, bold=True))
        
        draw.text((cx1 + 65, cy1 + 18), name[:32], fill=(255, 255, 255), font=font_card_title)
        draw.text((cx1 + 65, cy1 + 48), chip_ref[:38], fill=(148, 163, 184), font=font_card_sub)
        
        draw.line([(cx1 + 15, cy1 + 78), (cx2 - 15, cy1 + 78)], fill=(51, 65, 85), width=1)
        
        words = funcao.split()
        line1 = ""
        line2 = ""
        for w in words:
            if len(line1 + " " + w) < 45:
                line1 = (line1 + " " + w).strip()
            elif len(line2 + " " + w) < 45:
                line2 = (line2 + " " + w).strip()
            else:
                break
        draw.text((cx1 + 15, cy1 + 90), line1, fill=(226, 232, 240), font=font_card_body)
        if line2:
            draw.text((cx1 + 15, cy1 + 115), line2, fill=(226, 232, 240), font=font_card_body)
            
        diff_box_y = cy1 + 155
        is_diff = "DIFERENCA" in diff_ref
        box_bg = (69, 26, 3) if is_diff else (15, 23, 42)
        box_border = (245, 158, 11) if is_diff else (71, 85, 105)
        draw_rounded_card(draw, cx1 + 12, diff_box_y, cx2 - 12, cy2 - 12, 8, fill=box_bg, outline=box_border, width=1)
        
        diff_words = diff_ref.split()
        dline1 = ""
        dline2 = ""
        dline3 = ""
        for dw in diff_words:
            if len(dline1 + " " + dw) < 42:
                dline1 = (dline1 + " " + dw).strip()
            elif len(dline2 + " " + dw) < 42:
                dline2 = (dline2 + " " + dw).strip()
            elif len(dline3 + " " + dw) < 42:
                dline3 = (dline3 + " " + dw).strip()
                
        tag_color = (251, 191, 36) if is_diff else (148, 163, 184)
        draw.text((cx1 + 22, diff_box_y + 10), dline1, fill=tag_color, font=font_card_diff)
        if dline2:
            draw.text((cx1 + 22, diff_box_y + 36), dline2, fill=tag_color, font=font_card_diff)
        if dline3:
            draw.text((cx1 + 22, diff_box_y + 62), dline3, fill=tag_color, font=font_card_diff)

    out_file = os.path.join(OUTPUT_DIR, "01_placa_principal_geral.jpg")
    canvas.save(out_file, quality=95)
    print(f"Foto 1 salva com sucesso em: {out_file}")

# ==============================================================================
# FOTO 2: DETALHE DO PROCESSADOR, RAM E BOTAO FEL
# ==============================================================================
def gerar_foto_2():
    print("Gerando Foto 2: Detalhe do Processador, RAM e Botao FEL...")
    raw_path = os.path.join(FOTOS_PLACA_DIR, "IMG_0357.jpg")
    im_raw = Image.open(raw_path)
    
    crop = im_raw.crop((200, 400, 2800, 3200)) # 2600 x 2800
    cw, ch = crop.size
    
    overlay = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    
    # 1. 2x SK Hynix RAM DDR3
    ram_box = (1000, 750, 2150, 1850)
    ov_draw.rectangle(ram_box, fill=(59, 130, 246, 60), outline=(59, 130, 246, 255), width=8)
    
    # 2. Dissipador Allwinner H713
    heatsink_box = (0, 700, 950, 2300)
    ov_draw.rectangle(heatsink_box, fill=(239, 68, 68, 50), outline=(239, 68, 68, 255), width=8)
    
    # 3. Botao Tactil Microswitch FEL
    fel_btn_box = (1500, 50, 1950, 350)
    ov_draw.rectangle(fel_btn_box, fill=(234, 179, 8, 80), outline=(255, 235, 59, 255), width=10)
    
    # 4. Conector SPK (Alto Falante)
    spk_box = (1750, 180, 2250, 680)
    ov_draw.rectangle(spk_box, fill=(236, 72, 153, 60), outline=(236, 72, 153, 255), width=7)
    
    # 5. Conector de Alimentacao 5V
    power_box = (1200, 2150, 2400, 2750)
    ov_draw.rectangle(power_box, fill=(225, 29, 72, 60), outline=(225, 29, 72, 255), width=7)
    
    # 6. Porta HDMI
    hdmi_box = (450, 0, 1500, 500)
    ov_draw.rectangle(hdmi_box, fill=(217, 119, 6, 60), outline=(217, 119, 6, 255), width=7)

    # Badges
    draw_badge(ov_draw, 1575, 1300, 55, "RAM", (59, 130, 246, 240), font=get_font(34, bold=True))
    draw_badge(ov_draw, 475, 1500, 55, "CPU", (239, 68, 68, 240), font=get_font(34, bold=True))
    draw_badge(ov_draw, 1725, 200, 55, "FEL", (234, 179, 8, 240), font=get_font(34, bold=True))
    draw_badge(ov_draw, 2000, 430, 50, "SPK", (236, 72, 153, 240), font=get_font(30, bold=True))
    draw_badge(ov_draw, 1800, 2450, 55, "5V", (225, 29, 72, 240), font=get_font(34, bold=True))

    crop_annotated = Image.alpha_composite(crop.convert("RGBA"), overlay).convert("RGB")

    panel_w = 1250
    canvas_w = cw + panel_w
    canvas_h = ch
    canvas = Image.new("RGB", (canvas_w, canvas_h), color=(15, 23, 42))
    canvas.paste(crop_annotated, (0, 0))

    draw = ImageDraw.Draw(canvas)
    draw.line([(cw, 0), (cw, canvas_h)], fill=(51, 65, 85), width=3)

    # Header
    draw.rectangle([cw, 0, canvas_w, 150], fill=(30, 41, 59))
    draw.line([(cw, 150), (canvas_w, 150)], fill=(234, 179, 8), width=4)
    draw.text((cw + 40, 28), "NÚCLEO DE PROCESSAMENTO & FEL", fill=(255, 255, 255), font=get_font(38, bold=True))
    draw.text((cw + 40, 92), "Macro Detalhado: Allwinner H713, SK Hynix e Botão Físico", fill=(148, 163, 184), font=get_font(22, bold=False))

    # Card 1: BOTAO FEL
    draw_rounded_card(draw, cw + 30, 170, canvas_w - 30, 680, 16, fill=(69, 26, 3), outline=(245, 158, 11), width=3)
    draw.text((cw + 55, 195), "★ DESCOBERTA CRUCIAL: BOTÃO FÍSICO FEL", fill=(251, 191, 36), font=get_font(28, bold=True))
    fel_text = [
        "Sua placa possui um microswitch SMD soldado de fabrica ao lado do HDMI!",
        "Na placa de teardown da comunidade, este botao NAO vinha soldado (exigia",
        "aterrar vias com pinca ou solda). Na sua placa, o processo e 100% seguro!",
        "",
        "COMO ACIONAR O MODO FEL (1f3a:efe8) PARA REGRAVAR A FIRMWARE:",
        "1. Desconecte o cabo de energia e o cabo USB do projetor.",
        "2. Abra o PhoenixSuit no computador com a imagem .img carregada.",
        "3. Mantenha este BOTAO FEL PRESSIONADO com o dedo ou espatula plastica.",
        "4. Conecte o cabo USB Macho-Macho entre o PC e a porta USB do projetor.",
        "5. Conecte o cabo de energia na tomada (mantendo o botao pressionado).",
        "6. O PhoenixSuit detectara instantaneamente o projetor em modo FEL!",
        "7. Solte o botao e confirme a gravacao de firmware na tela do PC."
    ]
    for idx, l in enumerate(fel_text):
        fcol = (255, 255, 255) if idx < 3 else ((254, 240, 138) if "COMO ACIONAR" in l else (226, 232, 240))
        fbld = True if (idx < 3 or "COMO ACIONAR" in l) else False
        draw.text((cw + 55, 250 + idx * 34), l, fill=fcol, font=get_font(20, bold=fbld))

    # Card 2: MEMORIAS SK HYNIX
    draw_rounded_card(draw, cw + 30, 705, canvas_w - 30, 1260, 16, fill=(30, 41, 59), outline=(59, 130, 246), width=2)
    draw.text((cw + 55, 730), "MEMÓRIAS RAM DDR3 (SK HYNIX)", fill=(96, 165, 250), font=get_font(28, bold=True))
    ram_info = [
        ("Part Number Gravado:", "SK Hynix H5TQ2G83CFR PBC 213V"),
        ("Numero de Lote:", "DTLGBD58H1 W"),
        ("Tipo & Frequencia:", "DDR3-1600 Mbps (PC3-12800), 1.5V"),
        ("Capacidade por CI:", "2 Gb (Giga-bits) = 256 MegaBytes cada"),
        ("Arranjo na Placa:", "2 chips na face superior (512MB) + 2 no verso (512MB) = 1GB Total"),
        ("Comparativo Teardown:", "DIFERENCA! A placa de engenharia usava CIs da Elpida (J2108BCSE)."),
        ("Impacto no Firmware:", "Total compatibilidade: o bootloader Allwinner auto-detecta a RAM.")
    ]
    for idx, (label, val) in enumerate(ram_info):
        draw.text((cw + 55, 785 + idx * 65), label, fill=(148, 163, 184), font=get_font(19, bold=False))
        val_col = (251, 191, 36) if "DIFERENCA" in val else (255, 255, 255)
        draw.text((cw + 55, 814 + idx * 65), val, fill=val_col, font=get_font(21, bold=True))

    # Card 3: PROCESSADOR ALLWINNER H713
    draw_rounded_card(draw, cw + 30, 1285, canvas_w - 30, 1840, 16, fill=(30, 41, 59), outline=(239, 68, 68), width=2)
    draw.text((cw + 55, 1310), "PROCESSADOR ALLWINNER H713", fill=(248, 113, 113), font=get_font(28, bold=True))
    soc_info = [
        ("SoC Part Number:", "Allwinner H713 (sun50iw12p1 architecture)"),
        ("Nucleos de CPU:", "Quad-Core ARM Cortex-A53 rodando a ate 1.512 GHz"),
        ("Processador Grafico:", "ARM Mali-G31 MP2 com suporte a OpenGL ES 3.2 e Vulkan 1.1"),
        ("Motor de Video VPU:", "Allwinner Phoenix Engine (Decodifica 4K a 60fps AV1/H.265)"),
        ("Dissipacao Termica:", "Dissipador passivo de aluminio extrudado com aletas verticais"),
        ("BootROM Integrada:", "Contem o protocolo Allwinner FEL nativo na porta USB.")
    ]
    for idx, (label, val) in enumerate(soc_info):
        draw.text((cw + 55, 1365 + idx * 65), label, fill=(148, 163, 184), font=get_font(19, bold=False))
        draw.text((cw + 55, 1394 + idx * 65), val, fill=(255, 255, 255), font=get_font(21, bold=True))

    # Card 4: INTERFACES ADJACENTES
    draw_rounded_card(draw, cw + 30, 1865, canvas_w - 30, 2380, 16, fill=(30, 41, 59), outline=(225, 29, 72), width=2)
    draw.text((cw + 55, 1890), "INTERFACES ADJACENTES", fill=(244, 63, 94), font=get_font(28, bold=True))
    conn_info = [
        ("5V Alimentacao DC:", "Header 2 pinos com chicote reforçado (5V / 2A direto da fonte)."),
        ("SPK (Alto-falante):", "Header JST 2 pinos conectado ao driver amplificador de audio."),
        ("Motor de Foco:", "Pad despopulado para motor de passo de foco eletrico."),
        ("Porta HDMI Type-A:", "Blindagem externa de chassi soldada ao plano de GND (Terra).")
    ]
    for idx, (label, val) in enumerate(conn_info):
        draw.text((cw + 55, 1945 + idx * 70), label, fill=(148, 163, 184), font=get_font(19, bold=False))
        draw.text((cw + 55, 1975 + idx * 70), val, fill=(255, 255, 255), font=get_font(21, bold=True))

    # Card 5: ATALHOS AUTOMATIZADOS CRIADOS NO PROJETO
    draw_rounded_card(draw, cw + 30, 2405, canvas_w - 30, 2740, 16, fill=(13, 71, 161), outline=(59, 130, 246), width=2)
    draw.text((cw + 55, 2430), "ATALHOS 1-CLIQUE CRIADOS NA PASTA DO PROJETO", fill=(255, 255, 255), font=get_font(26, bold=True))
    draw.text((cw + 55, 2480), "• ABRIR_PHOENIXSUIT.bat -> Abre o PhoenixSuit v1.10 com a firmware ja configurada.", fill=(224, 231, 255), font=get_font(20, bold=False))
    draw.text((cw + 55, 2525), "• ABRIR_SERIAL_CP2102.bat -> Conecta automaticamente no console PuTTY na COM9.", fill=(224, 231, 255), font=get_font(20, bold=False))
    draw.text((cw + 55, 2570), "• Imagem de Firmware: 'firmware/HY300_Pro_Plus_H713.img' pronta para ser gravada.", fill=(147, 197, 253), font=get_font(20, bold=True))
    draw.text((cw + 55, 2615), "DICA: O aterramento de qualquer sinal TTL ou cabo pode ser feito na carcaca do HDMI.", fill=(251, 191, 36), font=get_font(19, bold=False))

    out_file = os.path.join(OUTPUT_DIR, "02_detalhe_processador_ram_botoes.jpg")
    canvas.save(out_file, quality=95)
    print(f"Foto 2 salva com sucesso em: {out_file}")

# ==============================================================================
# FOTO 3: DETALHE DO WI-FI 6, UART E CRISTAL
# ==============================================================================
def gerar_foto_3():
    print("Gerando Foto 3: Detalhe do Wi-Fi 6, UART, Cristal e Fan...")
    raw_path = os.path.join(FOTOS_PLACA_DIR, "IMG_0356.jpg")
    im_raw = Image.open(raw_path)
    w_raw, h_raw = im_raw.size

    crop = im_raw.crop((int(w_raw * 0.28), int(h_raw * 0.05), int(w_raw * 0.98), int(h_raw * 0.72)))
    cw, ch = crop.size

    overlay = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)

    # 1. Modulo WiFi 6 AW869A
    wifi_box = (100, 220, 1050, 1450)
    ov_draw.rectangle(wifi_box, fill=(16, 185, 129, 60), outline=(16, 185, 129, 255), width=8)

    # 2. Conector Fan
    fan_box = (1450, 150, 2150, 1050)
    ov_draw.rectangle(fan_box, fill=(6, 182, 212, 60), outline=(6, 182, 212, 255), width=8)

    # 3. Cristal Oscilador 24MHz
    crystal_box = (1200, 1500, 1650, 1850)
    ov_draw.rectangle(crystal_box, fill=(245, 158, 11, 70), outline=(245, 158, 11, 255), width=7)

    # 4. Saida Audio P2
    jack_box = (2150, 1000, 2820, 1750)
    ov_draw.rectangle(jack_box, fill=(168, 85, 247, 60), outline=(168, 85, 247, 255), width=8)

    # 5. Carcaca USB (GND Reference)
    usb_box = (2250, 1750, 2820, 2026)
    ov_draw.rectangle(usb_box, fill=(59, 130, 246, 60), outline=(59, 130, 246, 255), width=8)

    # 6. Vias / Pads UART entre Fan e Jack P2
    uart_box = (2000, 500, 2250, 850)
    ov_draw.rectangle(uart_box, fill=(234, 179, 8, 90), outline=(255, 235, 59, 255), width=8)

    # Badges
    draw_badge(ov_draw, 575, 835, 50, "WIFI", (16, 185, 129, 240), font=get_font(30, bold=True))
    draw_badge(ov_draw, 1800, 600, 45, "FAN", (6, 182, 212, 240), font=get_font(28, bold=True))
    draw_badge(ov_draw, 1425, 1675, 45, "24M", (245, 158, 11, 240), font=get_font(28, bold=True))
    draw_badge(ov_draw, 2485, 1375, 45, "P2", (168, 85, 247, 240), font=get_font(28, bold=True))
    draw_badge(ov_draw, 2125, 675, 45, "UART", (234, 179, 8, 240), font=get_font(24, bold=True))
    draw_badge(ov_draw, 2535, 1888, 45, "GND", (59, 130, 246, 240), font=get_font(26, bold=True))

    crop_annotated = Image.alpha_composite(crop.convert("RGBA"), overlay).convert("RGB")

    panel_w = 1200
    canvas_w = cw + panel_w
    canvas_h = ch
    canvas = Image.new("RGB", (canvas_w, canvas_h), color=(15, 23, 42))
    canvas.paste(crop_annotated, (0, 0))

    draw = ImageDraw.Draw(canvas)
    draw.line([(cw, 0), (cw, canvas_h)], fill=(51, 65, 85), width=3)

    # Header
    draw.rectangle([cw, 0, canvas_w, 150], fill=(30, 41, 59))
    draw.line([(cw, 150), (canvas_w, 150)], fill=(16, 185, 129), width=4)
    draw.text((cw + 40, 28), "COMUNICAÇÃO, WI-FI 6 & UART", fill=(255, 255, 255), font=get_font(38, bold=True))
    draw.text((cw + 40, 90), "Macro Detalhado: AW869A, Test Points e Conexao Serial", fill=(148, 163, 184), font=get_font(22, bold=False))

    # Card 1: WIFI 6 ALLWINNER AW869A
    draw_rounded_card(draw, cw + 30, 180, canvas_w - 30, 680, 16, fill=(30, 41, 59), outline=(16, 185, 129), width=2)
    draw.text((cw + 60, 205), "MÓDULO WI-FI 6 & BLUETOOTH (AW869A)", fill=(52, 211, 153), font=get_font(28, bold=True))
    wifi_info = [
        ("Identificacao:", "Allwinner / Fn-Link AW869A WIFI6"),
        ("Padrao Sem Fio:", "IEEE 802.11ax / ac / a / b / g / n (Dual-Band 2.4GHz & 5GHz)"),
        ("Bluetooth:", "Bluetooth 5.2 / 5.4 Dual-Mode com suporte a LE Audio"),
        ("Antena:", "Conector coaxial micro-RF IPEX / U.FL com cabo conectado"),
        ("Diferenca Teardown:", "GRANDE DIFERENCA: Fica na face superior! Na placa de referencia"),
        ("", "o chip ficava no verso e era o AIC8800D40."),
        ("Compatibilidade:", "O firmware HY300_Pro_Plus_H713 ja inclui o modulo de kernel aw869a.ko.")
    ]
    for idx, (label, val) in enumerate(wifi_info):
        if label:
            draw.text((cw + 60, 265 + idx * 52), label, fill=(148, 163, 184), font=get_font(18, bold=False))
        vcol = (251, 191, 36) if "DIFERENCA" in val else (255, 255, 255)
        draw.text((cw + 60 if not label else cw + 240, 265 + idx * 52), val, fill=vcol, font=get_font(18, bold=True))

    # Card 2: PINAGEM UART SERIAL CONSOLE
    draw_rounded_card(draw, cw + 30, 710, canvas_w - 30, 1260, 16, fill=(30, 41, 59), outline=(234, 179, 8), width=2)
    draw.text((cw + 60, 735), "CONSOLE SERIAL UART (USB-TO-TTL)", fill=(251, 191, 36), font=get_font(28, bold=True))
    uart_info = [
        ("Nivel Logico:", "3.3V TTL (OBRIGATÓRIO: NUNCA LIGUE 5V NA CPU H713!)"),
        ("Velocidade (Baud):", "115,200 bps, 8 bits, Sem Paridade, 1 Stop Bit (8-N-1)"),
        ("Fio Preto (GND):", "Conectar a Carcaca Metalica da porta USB ou HDMI"),
        ("Fio Branco (TX Placa):", "Liga no pino RXD do adaptador USB-TTL (CP2102)"),
        ("Fio Verde (RX Placa):", "Liga no pino TXD do adaptador USB-TTL (CP2102)"),
        ("Pino VCC (Alimentacao):", "DEIXE DESCONECTADO (O projetor usa a propria fonte!)"),
        ("Status no Windows:", "Adaptador reconhecido e configurado na porta COM9.")
    ]
    for idx, (label, val) in enumerate(uart_info):
        draw.text((cw + 60, 795 + idx * 58), label, fill=(148, 163, 184), font=get_font(18, bold=False))
        vcol = (239, 68, 68) if "3.3V" in val or "NUNCA" in val else ((74, 222, 128) if "COM9" in val else (255, 255, 255))
        draw.text((cw + 60, 822 + idx * 58), val, fill=vcol, font=get_font(19, bold=True))

    # Card 3: CRISTAL OSCILADOR & CONECTOR FAN
    draw_rounded_card(draw, cw + 30, 1290, canvas_w - 30, 1780, 16, fill=(30, 41, 59), outline=(6, 182, 212), width=2)
    draw.text((cw + 60, 1315), "SISTEMA DE CLOCK & RESFRIAMENTO", fill=(34, 211, 238), font=get_font(28, bold=True))
    aux_info = [
        ("Cristal 24.000 MHz:", "Gera a frequencia mestre para o PLL do Allwinner H713."),
        ("Conector Fan (Cooler):", "Header polarizado com chicote de fios (Preto = GND, Vermelho = 5V)."),
        ("Controle de Rotacao:", "Sinal PWM gerenciado pelo kernel Android com base na temperatura."),
        ("Conector P2 (3.5mm):", "Conector estereo analogico blindado para caixa de som externa.")
    ]
    for idx, (label, val) in enumerate(aux_info):
        draw.text((cw + 60, 1375 + idx * 62), label, fill=(148, 163, 184), font=get_font(19, bold=False))
        draw.text((cw + 60, 1402 + idx * 62), val, fill=(255, 255, 255), font=get_font(20, bold=True))

    # Card 4: SCRIPT SERIAL
    draw_rounded_card(draw, cw + 30, 1810, canvas_w - 30, 1970, 14, fill=(13, 71, 161), outline=(59, 130, 246), width=2)
    draw.text((cw + 60, 1835), "SCRIPT PRONTO PARA LEITURA SERIAL:", fill=(255, 255, 255), font=get_font(24, bold=True))
    draw.text((cw + 60, 1875), "Execute o arquivo 'ABRIR_SERIAL_CP2102.bat' na pasta do projeto.", fill=(224, 231, 255), font=get_font(20, bold=False))
    draw.text((cw + 60, 1910), "Ele abrira o PuTTY diretamente em 115200 baud na porta COM9 detectada.", fill=(147, 197, 253), font=get_font(19, bold=True))

    out_file = os.path.join(OUTPUT_DIR, "03_detalhe_wifi_uart_sensores.jpg")
    canvas.save(out_file, quality=95)
    print(f"Foto 3 salva com sucesso em: {out_file}")

# ==============================================================================
# FOTO 4: PLACA DA FONTE DE ALIMENTACAO
# ==============================================================================
def gerar_foto_4():
    print("Gerando Foto 4: Placa da Fonte de Alimentacao...")
    raw_path = os.path.join(FOTOS_PLACA_DIR, "IMG_0359.jpg")
    im_raw = Image.open(raw_path)
    
    crop = im_raw.crop((200, 30, 2980, 3350)) # 2780 x 3320
    cw, ch = crop.size

    overlay = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)

    # 1. ZONA DE ALTA TENSAO (PERIGO LETAL - 110V/220V AC e ~340V DC)
    high_v_box = (50, 50, 1450, 3100)
    ov_draw.rectangle(high_v_box, fill=(220, 38, 38, 45), outline=(239, 68, 68, 255), width=10)

    # 2. Capacitor Primario KSJ VENT
    cap_box = (650, 680, 1400, 2300)
    ov_draw.rectangle(cap_box, fill=(234, 179, 8, 60), outline=(255, 235, 59, 255), width=8)

    # 3. Entrada AC e Fusivel
    ac_box = (650, 80, 1400, 680)
    ov_draw.rectangle(ac_box, fill=(249, 115, 22, 60), outline=(249, 115, 22, 255), width=7)

    # 4. Ponte Retificadora BD1
    bridge_box = (150, 680, 600, 1250)
    ov_draw.rectangle(bridge_box, fill=(239, 68, 68, 60), outline=(239, 68, 68, 255), width=7)

    # 5. Transformador Chopper
    trans_box = (1450, 750, 2600, 2150)
    ov_draw.rectangle(trans_box, fill=(59, 130, 246, 50), outline=(59, 130, 246, 255), width=8)

    # 6. ZONA DE BAIXA TENSAO (SECUNDARIO SEGURO - 27V e 5V)
    sec_box = (1450, 50, 2750, 3100)
    ov_draw.rectangle(sec_box, fill=(16, 185, 129, 35), outline=(16, 185, 129, 255), width=8)

    # 7. Capacitores e Saida Secundaria
    out_cap_box = (1950, 80, 2700, 750)
    ov_draw.rectangle(out_cap_box, fill=(16, 185, 129, 60), outline=(16, 185, 129, 255), width=7)

    # Badges e Avisos de Seguranca
    draw_badge(ov_draw, 1025, 1490, 60, "CAP", (220, 38, 38, 240), font=get_font(36, bold=True))
    draw_badge(ov_draw, 1025, 380, 55, "AC/F1", (249, 115, 22, 240), font=get_font(30, bold=True))
    draw_badge(ov_draw, 375, 965, 50, "BD1", (239, 68, 68, 240), font=get_font(30, bold=True))
    draw_badge(ov_draw, 2025, 1450, 60, "TRANS", (59, 130, 246, 240), font=get_font(32, bold=True))
    draw_badge(ov_draw, 2325, 415, 55, "27V/5V", (16, 185, 129, 240), font=get_font(28, bold=True))

    crop_annotated = Image.alpha_composite(crop.convert("RGBA"), overlay).convert("RGB")

    panel_w = 1250
    canvas_w = cw + panel_w
    canvas_h = ch
    canvas = Image.new("RGB", (canvas_w, canvas_h), color=(15, 23, 42))
    canvas.paste(crop_annotated, (0, 0))

    draw = ImageDraw.Draw(canvas)
    draw.line([(cw, 0), (cw, canvas_h)], fill=(51, 65, 85), width=3)

    # Header
    draw.rectangle([cw, 0, canvas_w, 160], fill=(30, 41, 59))
    draw.line([(cw, 160), (canvas_w, 160)], fill=(239, 68, 68), width=4)
    draw.text((cw + 40, 30), "FONTE DE ALIMENTAÇÃO (40W)", fill=(255, 255, 255), font=get_font(38, bold=True))
    draw.text((cw + 40, 95), "Modelo: GKY40W-TYY27A REV:A01 (27V LED + 5V Lógica)", fill=(148, 163, 184), font=get_font(22, bold=False))

    # CARD CRITICO: AVISO DE SEGURANCA
    draw_rounded_card(draw, cw + 30, 190, canvas_w - 30, 750, 16, fill=(69, 10, 10), outline=(239, 68, 68), width=4)
    draw.text((cw + 60, 220), "⚠ ALERTA MÁXIMO DE SEGURANÇA ELÉTRICA", fill=(254, 202, 202), font=get_font(30, bold=True))
    danger_text = [
        "O CAPACITOR PRIMÁRIO (KSJ VENT) RETÉM ATÉ 340V DC MESMO FORA DA TOMADA!",
        "",
        "Regras Fundamentais de Segurança:",
        "1. NUNCA toque com as maos nuas nas pernas ou na carcaca do capacitor preto.",
        "2. NUNCA repouse a placa da fonte sobre superficies metalicas condutivas.",
        "3. Apos desligar o projetor da tomada, aguarde pelo menos 5 A 10 MINUTOS",
        "   para que a resistencia de sangria descarregue a alta tensao.",
        "4. Ao manusear o projetor aberto durante o processo de recuperacao USB,",
        "   evite segurar pela lateral onde fica esta placa verde de fonte.",
        "5. O choque nesta regiao primaria e doloroso e pode ser fatal em pessoas sensiveis."
    ]
    for idx, l in enumerate(danger_text):
        fcol = (252, 165, 165) if idx == 0 else ((255, 255, 255) if "Regras" in l else (254, 226, 226))
        fbld = True if (idx == 0 or "Regras" in l) else False
        draw.text((cw + 60, 280 + idx * 38), l, fill=fcol, font=get_font(21, bold=fbld))

    # CARD 2: CIRCUITO PRIMARIO
    draw_rounded_card(draw, cw + 30, 780, canvas_w - 30, 1370, 16, fill=(30, 41, 59), outline=(249, 115, 22), width=2)
    draw.text((cw + 60, 805), "ESTÁGIO PRIMÁRIO (ALTA TENSÃO)", fill=(251, 146, 60), font=get_font(28, bold=True))
    prim_info = [
        ("Identificacao da Placa:", "GKY40W-TYY27A REV:A01 HR (Data: 2023.11.25)"),
        ("Entrada AC (CN1):", "100V ~ 240V AC bivolt automatico (50/60Hz)"),
        ("Fusivel de Entrada (F1):", "T3.15A 250V (ou T2AL/250V) protege contra curto-circuito"),
        ("Termistor NTC (Disco):", "Limita a corrente de partida instantanea ao plugar na tomada"),
        ("Ponte Retificadora (BD1):", "JBF310 (Converte AC senoidal para corrente pulsada)"),
        ("Capacitor de Filtro:", "KSJ VENT eletrolitico de alta tensao (filtra para ~170V a 340V DC)"),
        ("MOSFET de Chaveamento:", "CS10N65A (Transistor N-Channel 650V / 10A de alta frequencia)")
    ]
    for idx, (label, val) in enumerate(prim_info):
        draw.text((cw + 60, 860 + idx * 68), label, fill=(148, 163, 184), font=get_font(19, bold=False))
        vcol = (239, 68, 68) if "DC" in val else (255, 255, 255)
        draw.text((cw + 60, 890 + idx * 68), val, fill=vcol, font=get_font(21, bold=True))

    # CARD 3: CIRCUITO SECUNDARIO
    draw_rounded_card(draw, cw + 30, 1400, canvas_w - 30, 1990, 16, fill=(30, 41, 59), outline=(16, 185, 129), width=2)
    draw.text((cw + 60, 1425), "ESTÁGIO SECUNDÁRIO (BAIXA TENSÃO SEGURO)", fill=(52, 211, 153), font=get_font(28, bold=True))
    sec_info = [
        ("Transformador Chopper:", "GKY40W-TYY27A (Isolamento galvanico total primario-secundario)"),
        ("Linha de Saida 1 (LED):", "27V DC / 1.1A (~30W dedicados ao motor de luz LED do projetor)"),
        ("Linha de Saida 2 (Logica):", "5V DC / 2A (10W para alimentar o SoC H713, RAM, WiFi e portas)"),
        ("Optoacoplador:", "Realimenta o sinal de controle de tensao de volta ao primario isolado"),
        ("Filtragem de Saida:", "Bateria de capacitores eletroliticos de baixa ESR para reduzir ripple"),
        ("Conector de Saida (CN2):", "Chicote polarizado que distribui 27V para o LED e 5V para a placa-mae")
    ]
    for idx, (label, val) in enumerate(sec_info):
        draw.text((cw + 60, 1480 + idx * 68), label, fill=(148, 163, 184), font=get_font(19, bold=False))
        vcol = (74, 222, 128) if "DC" in val else (255, 255, 255)
        draw.text((cw + 60, 1510 + idx * 68), val, fill=vcol, font=get_font(21, bold=True))

    # Resumo
    draw_rounded_card(draw, cw + 30, 2020, canvas_w - 30, 2220, 14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
    draw.text((cw + 60, 2045), "COMO TESTAR SE A FONTE ESTÁ BOA COM MULTÍMETRO:", fill=(255, 255, 255), font=get_font(22, bold=True))
    draw.text((cw + 60, 2085), "• Meca no conector CN2 desconectado: o pino de 5V deve apresentar exatamente 5.0V a 5.2V DC.", fill=(226, 232, 240), font=get_font(19, bold=False))
    draw.text((cw + 60, 2125), "• O pino de LED deve apresentar entre 26V e 27.5V DC. Se ambas as tensoes estiverem presentes,", fill=(226, 232, 240), font=get_font(19, bold=False))
    draw.text((cw + 60, 2165), "  a fonte esta 100% integra e o problema do projetor e estritamente de firmware/boot!", fill=(74, 222, 128), font=get_font(20, bold=True))

    out_file = os.path.join(OUTPUT_DIR, "04_placa_fonte_alimentacao.jpg")
    canvas.save(out_file, quality=95)
    print(f"Foto 4 salva com sucesso em: {out_file}")

def main():
    print("=" * 60)
    print("GERANDO GUIAS VISUAIS ANOTADOS REFINADOS")
    print("=" * 60)
    gerar_foto_1()
    gerar_foto_2()
    gerar_foto_3()
    gerar_foto_4()
    print("=" * 60)
    print("TODAS AS 4 FOTOS FORAM ATUALIZADAS COM SUCESSO!")
    print("=" * 60)

if __name__ == "__main__":
    main()
