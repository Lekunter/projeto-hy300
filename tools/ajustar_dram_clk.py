"""Copia um firmware IMAGEWTY trocando so o clock da DRAM no fes1 e nos boot0.

Uso: python tools/ajustar_dram_clk.py <entrada.img> <saida.img> <MHz>

O clock fica no 1o word de dram_para (offset 0x38). O checksum do cabecalho eGON
(soma dos words com o campo em 0x5F0A6C39) e recalculado. Nada mais muda.
"""
import os
import shutil
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "references", "magcubic-root"))
from awimg import read_image  # noqa: E402

OFF_DRAM = 0x38
ALVOS = ("fes1.fex", "boot0_nand.fex", "boot0_sdcard.fex")


def checksum_egon(d):
    tam = struct.unpack_from("<I", d, 0x10)[0]
    b = bytearray(d[:tam])
    struct.pack_into("<I", b, 0x0C, 0x5F0A6C39)
    return sum(struct.unpack("<%dI" % (tam // 4), b)) & 0xFFFFFFFF


def ajustar(d, mhz):
    assert d[4:12] == b"eGON.BT0", "nao e eGON.BT0"
    assert checksum_egon(d) == struct.unpack_from("<I", d, 0x0C)[0], "checksum original nao bate"
    b = bytearray(d)
    struct.pack_into("<I", b, OFF_DRAM, mhz)
    struct.pack_into("<I", b, 0x0C, checksum_egon(b))
    assert checksum_egon(b) == struct.unpack_from("<I", b, 0x0C)[0]
    return bytes(b)


def main(entrada, saida, mhz):
    _, arquivos = read_image(entrada)
    por_nome = {fh["filename"]: fh for fh in arquivos}
    shutil.copyfile(entrada, saida)
    with open(saida, "r+b") as f:
        for nome in ALVOS:
            fh = por_nome[nome]
            f.seek(fh["offset"])
            d = f.read(fh["original_length"])
            antes = struct.unpack_from("<I", d, OFF_DRAM)[0]
            f.seek(fh["offset"])
            f.write(ajustar(d, mhz))
            print("%-17s %d -> %d MHz" % (nome, antes, mhz))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
