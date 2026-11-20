#!/usr/bin/env python3
"""Tạo lại `assets/fonts/do-rong-chu.json` (độ rộng từng ký tự ở độ đậm 400/600/700, đơn vị 1/1000 em) từ font Be Vietnam Pro của repo.

    python -X utf8 .claude/skills/feature-exploration-report/scripts/tao-bang-do-rong.py

`ve-so-do.py` dùng bảng này để đo chữ trong hộp sơ đồ: font đổi thì chạy lại, hộp sơ đồ luôn vừa chữ. Cần fonttools + brotli.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import giao_dien  # noqa: E402
from fontTools.ttLib import TTFont  # noqa: E402
from fontTools.varLib import instancer  # noqa: E402

OUT = os.path.join(giao_dien.ASSETS, 'fonts', 'do-rong-chu.json')


def main():
    entries = [m for m in giao_dien._manifest() if m['family'] == 'Be Vietnam Pro' and m['style'] == 'normal']
    if not entries:
        print('Chưa có font Be Vietnam Pro ở docs/thuong-hieu/fonts (chạy scripts/tai-font.py).')
        return 1
    table = {'400': {}, '600': {}, '700': {}}
    for m in entries:
        for weight in table:
            if m['weight'] != weight:   # font tĩnh: mỗi độ đậm một file
                continue
            font = TTFont(os.path.join(giao_dien.FONTS, m['file']))
            cmap, hmtx, upem = font.getBestCmap(), font['hmtx'], font['head'].unitsPerEm
            for cp, glyph in cmap.items():
                if cp <= 0x2BFF:
                    table[weight].setdefault(chr(cp), round(hmtx[glyph][0] * 1000 / upem))
    note = 'Độ rộng chữ (1/1000 em) của Be Vietnam Pro ở độ đậm 400, 600, 700, tạo bằng scripts/tao-bang-do-rong.py từ docs/thuong-hieu/fonts.'
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps({'ghi-chu': note, 'rong': table}, ensure_ascii=False, separators=(',', ':')))
    print('Đã ghi %s (%d ký tự mỗi độ đậm)' % (os.path.relpath(OUT, giao_dien.ROOT), len(table['400'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
