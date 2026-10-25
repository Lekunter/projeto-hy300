"""Mostra o tipo e o clock de DRAM que um firmware IMAGEWTY (PhoenixSuit/PhoenixCard) vai usar.

Uso: python tools/verificar_dram.py <imagem.img> [outra.img ...]

Esta placa (M11-REV1.3) tem DDR3: so serve imagem com tipo 3.
"""
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "references", "magcubic-root"))
from awimg import read_image  # noqa: E402

TIPOS = {2: "DDR2", 3: "DDR3", 4: "DDR4", 6: "LPDDR2", 7: "LPDDR3", 8: "LPDDR4"}
# Os 24 words de dram_para ficam em 0x38 no boot0/fes1 do H713 (dram_clk, dram_type, zq, ...).
OFF_DRAM = 0x38


def ler(f, fh):
    f.seek(fh["offset"])
    return f.read(fh["original_length"])


def verificar(caminho):
    _, arquivos = read_image(caminho)
    por_nome = {fh["filename"]: fh for fh in arquivos}
    print("==", caminho)
    with open(caminho, "rb") as f:
        if "sunxi_version.fex" in por_nome:
            print("   build:", ler(f, por_nome["sunxi_version.fex"]).rstrip(b"\0\n").decode(errors="replace"))
        for nome in ("boot0_sdcard.fex", "boot0_nand.fex", "fes1.fex"):
            if nome not in por_nome:
                continue
            d = ler(f, por_nome[nome])
            clk, tipo = struct.unpack_from("<II", d, OFF_DRAM)
            if tipo not in TIPOS or not 100 <= clk <= 1600:
                print("   %-17s nao reconhecido (layout diferente?)" % nome)
                continue
            aviso = "OK para esta placa" if tipo == 3 else "NAO serve (placa e DDR3)"
            print("   %-17s %-6s %4d MHz  -> %s" % (nome, TIPOS[tipo], clk, aviso))
            print("   %-17s dram_para: %s" % ("", " ".join("%x" % w for w in struct.unpack_from("<24I", d, OFF_DRAM))))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for c in sys.argv[1:]:
        verificar(c)
