"""Vẽ sơ đồ SVG cho báo cáo khám phá theo ĐÚNG MẪU ĐÃ CHỐT (dùng chung cho mọi dự án).

Vì sao có script này: trước đây mỗi lần làm báo cáo, sơ đồ được vẽ tay từ đầu nên màu, cỡ chữ,
bố cục khác nhau giữa các máy/các phiên. Giờ chỉ cần viết nội dung (JSON), script lo hình dáng.
Mẫu gốc: ba loại sơ đồ (tổng quan, tuần tự, trạng thái) trong `assets/so-do-mau/` — đã người dùng chốt.

Ba loại ("loai" trong JSON):
  tong-quan  : vai trò bên trái → hệ thống ở giữa → hệ thống bên thứ ba bên phải, mũi tên đánh số.
  tuan-tu    : các làn (tài khoản, hệ thống, bên thứ ba), mỗi thông điệp một dòng, có hộp ghi chú.
  trang-thai : ô trạng thái đặt theo cột/hàng, mũi tên đánh số, nhánh quay lại vẽ đường cong.
Cách viết JSON và ví dụ: references/so-do.md, assets/so-do-mau/*.json.

Dùng:
  - Trong file nguồn báo cáo: <div class="diag" data-so-do="so-do/tong-quan.json"></div>
    (đường dẫn tính từ thư mục file nguồn) → build-embed.py tự vẽ và chèn SVG.
  - Xem thử riêng: python -X utf8 ve-so-do.py <file.json> [-o xem-thu.html]
    → ra trang HTML có sẵn font + CSS chuẩn để mở xem.
"""
import io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')

# ---------- bảng màu đã chốt (khớp assets/giao-dien-chuan.css) ----------
VAI_TRO = {   # màu đậm (viền/chữ/nhãn), màu nền nhạt
    'p1': ('#177a5c', '#e3f4ed'), 'p2': ('#b7791f', '#fbf0dc'), 'p3': ('#2b6cb0', '#e4eefa'),
    'p4': ('#b83280', '#fbe7f1'), 'p5': ('#2c7a7b', '#e0f2f1'),
    'ext': ('#6b46c1', '#efe9fb'), 'sys': ('#4a5568', '#eef1f4'),
}
BRAND = '#0b5d4e'
KIEU_TT = {   # kiểu ô trạng thái: nền, viền, chữ
    'xam': ('#eef1f4', '#6b7a86', '#33414d'), 'xanh': ('#e4eefa', '#2b6cb0', '#2b6cb0'),
    'ok': ('#dcf3e7', '#146c43', '#146c43'), 'loi': ('#ffe3e8', '#a3123a', '#a3123a'),
    'cho': ('#fff0cf', '#b7791f', '#8a5a00'), 'tim': ('#efe9fb', '#6b46c1', '#6b46c1'),
    'ngoai': ('#f4f4f4', '#999', '#555'),   # ngoài phạm vi feature: viền nét đứt
}
NOTE_FILL, NOTE_LINE, NOTE_INK = '#fff6e0', '#f0c36d', '#6b4a00'
ARROW, ARROW_RET, LIFELINE = '#334', '#777', '#b9c4c0'

# ---------- đo chữ bằng độ rộng thật của font Be Vietnam Pro (bảng tạo bằng tao-bang-do-rong.py) ----------
_W = json.load(io.open(os.path.join(ASSETS, 'fonts', 'do-rong-chu.json'), encoding='utf-8'))['rong']

def tw(s, size, weight=400):
    """độ rộng (px) của chuỗi s ở cỡ chữ size, độ đậm weight (400/600/700)."""
    s = re.sub(r'\*\*', '', s)
    tbl = _W['700' if weight >= 650 else '600' if weight >= 550 else '400']
    return sum(tbl.get(ch, 1000 if ord(ch) > 0x2600 else 600) for ch in s) * size / 1000.0

CANH_BAO = []

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def rich(s):
    """**chữ đậm** → <tspan font-weight="700">"""
    parts = re.split(r'\*\*(.+?)\*\*', s)
    return ''.join(esc(p) if i % 2 == 0 else '<tspan font-weight="700">%s</tspan>' % esc(p) for i, p in enumerate(parts))

def fix_bold(lines):
    """khi tự xuống dòng cắt giữa cặp ** … **: đóng ở cuối dòng, mở lại ở dòng sau"""
    out, open_ = [], False
    for ln in lines:
        if open_: ln = '**' + ln
        if ln.count('**') % 2: ln += '**'; open_ = True
        else: open_ = False
        out.append(ln)
    return out

def n(v):
    v = round(v, 1)
    return str(int(v)) if v == int(v) else str(v)

def text(x, y, s, size=13, fill='#222', weight=None, anchor=None, noh=False, extra=''):
    a = ['x="%s"' % n(x), 'y="%s"' % n(y), 'font-size="%s"' % n(size)]
    if fill: a.append('fill="%s"' % fill)
    if weight: a.append('font-weight="%s"' % weight)
    if anchor: a.append('text-anchor="%s"' % anchor)
    if noh: a.append('stroke="none"')
    return '<text %s%s>%s</text>' % (' '.join(a), extra, rich(s))

def badge(cx, cy, num, color, size=13):
    return ('<g class="noh"><circle cx="%s" cy="%s" r="11" fill="%s"/>'
            '<text x="%s" y="%s" text-anchor="middle" font-size="%s" font-weight="700" fill="#fff" stroke="none">%s</text></g>'
            % (n(cx), n(cy), color, n(cx), n(cy + 4.5), n(size), esc(str(num))))

def markers(mid):
    return ('<defs><marker id="%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
            '<path d="M0 0L10 5L0 10z" fill="%s"/></marker>'
            '<marker id="%sd" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
            '<path d="M0 0L10 5L0 10z" fill="%s"/></marker></defs>' % (mid, ARROW, mid, ARROW_RET))

def line(x1, y1, x2, y2, mid, ret=False, width=2):
    if ret:
        return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" stroke-dasharray="6 4" fill="none" marker-end="url(#%sd)"/>'
                % (n(x1), n(y1), n(x2), n(y2), ARROW_RET, width, mid))
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" fill="none" marker-end="url(#%s)"/>'
            % (n(x1), n(y1), n(x2), n(y2), ARROW, width, mid))

def color_of(key):
    if key not in VAI_TRO:
        raise ValueError('màu "%s" không có trong bảng màu chuẩn (dùng: %s)' % (key, ', '.join(VAI_TRO)))
    return VAI_TRO[key]

def lines_of(v):
    if v is None: return []
    return v if isinstance(v, list) else str(v).split('\n')

def svg_wrap(W, H, label, body):
    return ('<svg viewBox="0 0 %s %s" role="img" aria-label="%s" data-ve-boi="ve-so-do.py">\n%s\n</svg>'
            % (n(W), n(H), esc(label), '\n'.join(body)))


# =====================================================================================
# 1) SƠ ĐỒ TỔNG QUAN
# =====================================================================================
def ve_tong_quan(d, mid):
    he = d['he-thong']; roles = d['vai-tro']; exts = d.get('ben-ngoai', []); steps = d['buoc']
    rid = {r['id']: r for r in roles}; eid = {e['id']: e for e in exts}
    for s in steps:
        if ('tu' in s) == ('den' in s):
            raise ValueError('bước %s: ghi đúng một trong "tu" (vai trò → hệ thống) hoặc "den" (hệ thống → bên thứ ba)' % s.get('so'))
        if 'tu' in s and s['tu'] not in rid: raise ValueError('bước %s: không có vai trò "%s"' % (s.get('so'), s['tu']))
        if 'den' in s and s['den'] not in eid: raise ValueError('bước %s: không có bên thứ ba "%s"' % (s.get('so'), s['den']))
    act_steps = {r['id']: [s for s in steps if s.get('tu') == r['id']] for r in roles}
    ext_steps = {e['id']: [s for s in steps if s.get('den') == e['id']] for e in exts}

    # --- bề ngang: tự nới theo chữ dài nhất ---
    aw = 210
    for r in roles:
        for t, sz, wt in [(r['ten'], 20, 700)] + [(x, 14, 600) for x in lines_of(r.get('vai'))] + [(x, 13, 400) for x in lines_of(r.get('mo-ta'))]:
            aw = max(aw, tw(t, sz, wt) + 24)
    lab1 = max([tw(s['nhan'], 12.5) for s in steps if 'tu' in s] + [0])
    ax, ar = 10, 10 + aw
    sx = ar + max(230, lab1 + 42 + 18)
    sw = 220
    for t, sz, wt in [(he['ten'], 21, 700), (he.get('phu', ''), 14, 400), (he.get('tieu-de-muc', ''), 13, 600),
                      (he.get('tieu-de-trang-thai', ''), 13, 600)] + [(x, 13, 400) for x in lines_of(he.get('trang-thai'))]:
        sw = max(sw, tw(t, sz, wt) + 30)
    for x in he.get('muc', []):
        sw = max(sw, tw('▸ ' + x, 13.5) + 60)
    sr = sx + sw
    lab2 = max([tw(s['nhan'], 12.5) + 36 for s in steps if 'den' in s] +
               [tw('← ' + s['tra-ve'], 12.5) + 70 for s in steps if 'den' in s and s.get('tra-ve')] +
               [tw(s.get('ghi-chu-nho', ''), 12) + 36 for s in steps if 'den' in s] + [0])
    ex = sr + max(210, lab2 + 18)
    ew = 210
    for e in exts:
        for t, sz, wt in [(e['ten'], 19, 700)] + [(x, 13, 400) for x in lines_of(e.get('mo-ta'))]:
            ew = max(ew, tw(t, sz, wt) + 24)
    W = (ex + ew + 10) if exts else (sr + 10)

    body = [markers(mid)]
    # --- vai trò (cột trái) ---
    y = 60
    arrows, labels, badges = [], [], []
    for r in roles:
        dark, light = color_of(r.get('mau', 'p1'))
        top = y
        tx = [text(ax + aw / 2, top + 32, r['ten'], 20, dark, 700, 'middle')]
        ly = top + 56
        for i, v in enumerate(lines_of(r.get('vai'))):
            ly = top + 56 + 18 * i
            tx.append(text(ax + aw / 2, ly, v, 14, None, 600, 'middle'))
        last = ly
        for i, v in enumerate(lines_of(r.get('mo-ta'))):
            last = ly + 30 + 18 * i
            tx.append(text(ax + aw / 2, last, v, 13, '#444', None, 'middle'))
        ss = act_steps[r['id']]
        ay = [top + 26 + 30 * i for i in range(len(ss))]
        h = max(last + 28 - top, (ay[-1] + 24 - top) if ay else 0)
        body.append('<rect x="%s" y="%s" width="%s" height="%s" rx="14" fill="%s" stroke="%s" stroke-width="2.5"/>' % (n(ax), n(top), n(aw), n(h), light, dark))
        body += tx
        for s, yy in zip(ss, ay):
            ret = bool(s.get('tra-ve'))           # nét đứt = kết quả hệ thống trả về
            if s.get('chieu') == 've':            # hệ thống → vai trò
                arrows.append(line(sx, yy, ar + 2, yy, mid, ret=ret))
                badges.append(badge(sx - 16, yy, s['so'], color_of(s.get('mau', 'sys'))[0]))
            else:
                arrows.append(line(ar, yy, sx - 2, yy, mid, ret=ret))
                badges.append(badge(ar + 16, yy, s['so'], color_of(s['mau'])[0] if s.get('mau') else dark))
            labels.append(text(ar + 42, yy - 5, s['nhan'], 12.5, '#555' if ret else '#222'))
        y = top + h + 60
    actors_bottom = y - 60

    # --- hệ thống bên thứ ba (cột phải) ---
    ext_boxes = []
    for e in exts:
        slots = []
        hh = 40
        for s in ext_steps[e['id']]:
            slots.append(hh)
            hh += 64 if (s.get('tra-ve') or s.get('ghi-chu-nho')) else 30
        nd = len(lines_of(e.get('mo-ta')))
        eh = max(100, hh + 26, 60 + 18 * max(nd - 1, 0) + 40)
        ext_boxes.append([e, eh, slots])
    if ext_boxes:
        tot = sum(b[1] for b in ext_boxes)
        span = max(actors_bottom, 60 + tot + 60 * (len(ext_boxes) - 1))
        gap = (span - 60 - tot) / (len(ext_boxes) - 1) if len(ext_boxes) > 1 else 0
        yy = 60
        for b in ext_boxes:
            b.append(yy); yy += b[1] + gap
        exts_bottom = max(b[3] + b[1] for b in ext_boxes)
    else:
        exts_bottom = 0
    for e, eh, slots, top in ext_boxes:
        dark, light = VAI_TRO['ext']
        body.append('<rect x="%s" y="%s" width="%s" height="%s" rx="14" fill="%s" stroke="%s" stroke-width="2.5"/>' % (n(ex), n(top), n(ew), n(eh), light, dark))
        body.append(text(ex + ew / 2, top + 36, e['ten'], 19, dark, 700, 'middle'))
        for i, v in enumerate(lines_of(e.get('mo-ta'))):
            body.append(text(ex + ew / 2, top + 60 + 18 * i, v, 13, '#444', None, 'middle'))
        for s, off in zip(ext_steps[e['id']], slots):
            yy = top + off
            arrows.append(line(sr, yy, ex - 2, yy, mid))
            labels.append(text(sr + 36, yy - 5, s['nhan'], 12.5))
            badges.append(badge(sr + 18, yy, s['so'], dark))
            if s.get('tra-ve'):
                arrows.append(line(ex, yy + 34, sr + 2, yy + 34, mid, ret=True))
                labels.append(text(sr + 70, yy + 28, '← ' + s['tra-ve'], 12.5, '#555'))
                if s.get('so-tra-ve') is not None:      # mũi tên trả về cũng là một bước có số
                    badges.append(badge(ex - 16, yy + 34, s['so-tra-ve'], dark))
            elif s.get('ghi-chu-nho'):
                labels.append(text(sr + 36, yy + 24, s['ghi-chu-nho'], 12, '#555'))

    # --- hệ thống chính (giữa) ---
    st = []
    cx = sx + sw / 2
    st.append(text(cx, 66, he['ten'], 21, BRAND, 700, 'middle'))
    if he.get('phu'): st.append(text(cx, 88, he['phu'], 14, '#555', None, 'middle'))
    cy = 88
    if he.get('tieu-de-muc'):
        cy = 124; st.append(text(cx, cy, he['tieu-de-muc'], 13, None, 600, 'middle'))
    for i, m in enumerate(he.get('muc', [])):
        cy = 152 + 26 * i
        st.append(text(sx + 42, cy, '▸ ' + m, 13.5, '#333'))
    if he.get('tieu-de-trang-thai'):
        cy += 58; st.append(text(cx, cy, he['tieu-de-trang-thai'], 13, None, 600, 'middle'))
        for i, v in enumerate(lines_of(he.get('trang-thai'))):
            cy += 22 if i == 0 else 20
            st.append(text(cx, cy, v, 13, '#333', None, 'middle'))
    sys_bottom = max(cy + 30, actors_bottom + 10, exts_bottom + 10)
    body.insert(1, '<rect x="%s" y="30" width="%s" height="%s" rx="16" fill="#fff" stroke="%s" stroke-width="3"/>' % (n(sx), n(sw), n(sys_bottom - 30), BRAND))
    body.insert(2, '\n'.join(st))
    body += arrows + labels + badges

    # --- hộp ghi chú (nhánh phụ) ---
    H = sys_bottom + 20
    note = d.get('ghi-chu')
    if note:
        tx0 = 64 if note.get('so') is not None else 26
        nl = []
        for raw in lines_of(note['dong']):     # tự xuống dòng khi dài quá khung (giữ nguyên **đậm** trong từng dòng)
            cur = ''
            for word in raw.split(' '):
                cand = (cur + ' ' + word).strip()
                if cur and tx0 + tw(cand, 14) > W - 30:
                    nl.append(cur); cur = word
                else:
                    cur = cand
            nl.append(cur)
        nl = fix_bold(nl)
        ny, nh = sys_bottom + 25, 18 + 20 * len(nl)
        body.append('<rect x="10" y="%s" width="%s" height="%s" rx="12" fill="%s" stroke="%s" stroke-width="2"/>' % (n(ny), n(W - 20), n(nh), NOTE_FILL, NOTE_LINE))
        if note.get('so') is not None:
            body.append(badge(40, ny + 29, note['so'], color_of(note.get('mau', 'sys'))[0]))
        for i, v in enumerate(nl):
            body.append(text(tx0, ny + 25 + 20 * i, v, 14, '#222', noh=True))
        H = ny + nh + 17
    return svg_wrap(W, H, d.get('mo-ta', 'Sơ đồ tổng quan'), body)


# =====================================================================================
# 2) SƠ ĐỒ TUẦN TỰ
# =====================================================================================
def ve_tuan_tu(d, mid):
    lanes = d['lan']; steps = d['buoc']
    idx = {l['id']: i for i, l in enumerate(lanes)}
    for s in steps:
        for k in ('tu', 'den'):
            if s.get(k) not in idx: raise ValueError('bước "%s": không có làn "%s"' % (s.get('nhan') or s.get('ghi-chu'), s.get(k)))
        if 'ghi-chu' not in s and s['tu'] == s['den']:
            raise ValueError('bước "%s": thông điệp phải đi giữa hai làn khác nhau (việc trong một làn ghi bằng "ghi-chu")' % s.get('nhan'))
    bw = []
    for l in lanes:
        w = max(110, tw(l['ten'], 14, 700) + 30)
        if l.get('phu'): w = max(w, tw(l['phu'], 11.5) + 24, 140)
        bw.append(w)
    # khoảng cách giữa hai làn kề nhau: đủ chỗ cho hộp tên và nhãn dài nhất
    gaps = []
    for i in range(len(lanes) - 1):
        g = bw[i] / 2 + bw[i + 1] / 2 + 20
        for s in steps:
            if 'ghi-chu' in s: continue
            a, b = sorted((idx[s['tu']], idx[s['den']]))
            if (a, b) == (i, i + 1):
                g = max(g, max(tw(x, 13) for x in lines_of(s["nhan"])) + 70)
        gaps.append(g)
    def centers():
        c = [bw[0] / 2 + 40]
        for g in gaps: c.append(c[-1] + g)
        return c
    for s in steps:   # thông điệp/ghi chú trải qua nhiều làn: nới đều nếu thiếu chỗ
        a, b = sorted((idx[s['tu']], idx[s['den']]))
        if a == b: continue
        need = (tw(s['ghi-chu'], 13) + 40) if 'ghi-chu' in s else (max(tw(x, 13) for x in lines_of(s["nhan"])) + 70)
        c = centers(); have = c[b] - c[a]
        if have < need:
            for k in range(a, b): gaps[k] += (need - have) / (b - a)
    c = centers()
    W = max(c[-1] + bw[-1] / 2 + 55, 900)

    body = [markers(mid)]
    heads = []
    for l, x, w in zip(lanes, c, bw):
        dark = color_of(l.get('mau', 'sys'))[0]
        heads.append('<rect x="%s" y="14" width="%s" height="48" rx="10" fill="%s"/>' % (n(x - w / 2), n(w), dark))
        if l.get('phu'):
            heads.append(text(x, 34, l['ten'], 14, '#fff', 700, 'middle', True))
            heads.append(text(x, 52, l['phu'], 11.5, '#fff', 500, 'middle', True))
        else:
            heads.append(text(x, 43, l['ten'], 14, '#fff', 700, 'middle', True))
    items, badges = [], []
    y = None; num = 0
    for s in steps:
        if 'ghi-chu' in s:
            a, b = sorted((idx[s['tu']], idx[s['den']]))
            ry = (y if y is not None else 64) + 30
            rx0, rx1 = c[a] + 40, c[b] + 40
            rx1 = max(rx1, rx0 + tw(s['ghi-chu'], 13) + 40)
            items.append('<rect x="%s" y="%s" width="%s" height="34" rx="8" fill="%s" stroke="%s" stroke-width="1.5"/>' % (n(rx0), n(ry), n(rx1 - rx0), NOTE_FILL, NOTE_LINE))
            items.append(text((rx0 + rx1) / 2, ry + 22, s['ghi-chu'], 13, NOTE_INK, None, 'middle', True))
            y = ry + 34 - 10   # thông điệp kế tiếp cách hộp ≥ 34px
            continue
        lab = lines_of(s['nhan'])
        y = (112 if y is None else y + 44) + 14 * (len(lab) - 1)
        num += 1
        a, b = idx[s['tu']], idx[s['den']]
        sg = 1 if b > a else -1
        ret = bool(s.get('tra-ve'))
        items.append(line(c[a], y, c[b] - 2 * sg, y, mid, ret=ret))
        mx = (c[a] + 30 * sg + c[b]) / 2      # chừa chỗ cho vòng số ở đầu mũi tên
        for k, t in enumerate(lab):
            items.append(text(mx, y - 7 - 14 * (len(lab) - 1 - k), t, 13, '#555' if ret else '#222', None, 'middle'))
        badges.append(badge(c[a] + 17 * sg, y, s.get('so', num), color_of(lanes[a].get('mau', 'sys'))[0], 12.5))
    end = (y if y is not None else 112) + 88
    life = ['<g stroke="%s" stroke-width="1.5" stroke-dasharray="5 5">' % LIFELINE] + \
           ['<line x1="%s" y1="64" x2="%s" y2="%s"/>' % (n(x), n(x), n(end)) for x in c] + ['</g>']
    body += life + ['<g class="noh">'] + heads + ['</g>'] + items + badges
    return svg_wrap(W, end + 20, d.get('mo-ta', 'Sơ đồ tuần tự'), body)


# =====================================================================================
# 3) SƠ ĐỒ TRẠNG THÁI
# =====================================================================================
def ve_trang_thai(d, mid):
    sts = d['trang-thai']; trs = d['chuyen']
    by = {s['id']: s for s in sts}
    for t in trs:
        for k in ('tu', 'den'):
            if t.get(k) not in by: raise ValueError('mũi tên %s: không có trạng thái "%s"' % (t.get('so'), t.get(k)))
    for s in sts:
        if s.get('kieu', 'xam') not in KIEU_TT:
            raise ValueError('trạng thái "%s": kiểu "%s" không có (dùng: %s)' % (s['ten'], s.get('kieu'), ', '.join(KIEU_TT)))
        dong = lines_of(s.get('dong'))       # dòng phụ dưới tên (thường dùng cho ô 'ngoai')
        s['_w'] = max([130, tw(s['ten'], 17 if not dong else 14, 700) + 44] + [tw(x, 13) + 40 for x in dong])
        s['_h'] = 56 if not dong else 50 + 22 * len(dong)
    ncol = max(s['cot'] for s in sts) + 1
    colw = [max([s['_w'] for s in sts if s['cot'] == k] + [130]) for k in range(ncol)]
    colx = [20]
    for k in range(ncol - 1):
        between = [t for t in trs if sorted((by[t['tu']]['cot'], by[t['den']]['cot'])) == [k, k + 1]]
        straight = all(by[t['tu']]['hang'] == by[t['den']]['hang'] for t in between)
        g = 120 if straight else 230
        for t in between:
            if t.get('nhan'): g = max(g, tw(t['nhan'], 13) + (50 if straight else 110))
        colx.append(colx[-1] + colw[k] + g)
    for s in sts:
        s['_w'] = colw[s['cot']]          # ô cùng cột rộng bằng nhau
        s['_x'] = colx[s['cot']]
        s['_y'] = 20 + 125 * s['hang']
        s['_cx'], s['_cy'] = s['_x'] + s['_w'] / 2, s['_y'] + s['_h'] / 2
    body = [markers(mid)]
    boxes = ['<g class="noh" font-size="17" font-weight="700" text-anchor="middle">']
    notes = []
    right = 0
    for s in sts:
        fill, stroke, ink = KIEU_TT[s.get('kieu', 'xam')]
        dash = ' stroke-dasharray="6 4"' if s.get('kieu') == 'ngoai' else ''
        boxes.append('<rect x="%s" y="%s" width="%s" height="%s" rx="12" fill="%s" stroke="%s" stroke-width="2.5"%s/>' % (n(s['_x']), n(s['_y']), n(s['_w']), n(s['_h']), fill, stroke, dash))
        dong = lines_of(s.get('dong'))
        if dong:
            boxes.append('<text x="%s" y="%s" font-size="14" fill="%s" stroke="none">%s</text>' % (n(s['_cx']), n(s['_y'] + 30), ink, esc(s['ten'])))
            for i, x in enumerate(dong):
                boxes.append('<text x="%s" y="%s" font-size="13" font-weight="400" fill="%s" stroke="none">%s</text>' % (n(s['_cx']), n(s['_y'] + 30 + 22 * (i + 1)), ink, rich(x)))
        else:
            boxes.append('<text x="%s" y="%s" fill="%s" stroke="none">%s</text>' % (n(s['_cx']), n(s['_y'] + 35), ink, esc(s['ten'])))
        right = max(right, s['_x'] + s['_w'])
        if s.get('ghi-chu'):
            notes.append(text(s['_x'] + s['_w'] + 12, s['_cy'] + 4, s['ghi-chu'], 12.5, ink, noh=True))
            right = max(right, s['_x'] + s['_w'] + 12 + tw(s['ghi-chu'], 12.5))
    boxes.append('</g>')
    paths, dpaths, labels, badges = [], [], [], []
    back = False
    def add(t, el):          # nét đứt (net-dut) = chuyển ra ngoài phạm vi / chưa kiểm chứng
        (dpaths if t.get('net-dut') else paths).append(el)
    def num(cx, cy, t):      # mũi tên không có 'so' thì không vẽ vòng số
        if t.get('so') is not None:
            badges.append(badge(cx, cy, t['so'], ARROW, 12))
    # mũi tên đi tới (sang cột phải): toả đều từ cạnh phải của ô nguồn
    fwd = {}
    for t in trs:
        if by[t['den']]['cot'] > by[t['tu']]['cot']:
            fwd.setdefault(t['tu'], []).append(t)
    # nhiều mũi tên cùng đổ vào một ô (vd Nháp và Bị trả lại cùng → Đã gửi): toả đều đầu mũi tên trên cạnh trái ô đích
    inc = {}
    for lst in fwd.values():
        for t in lst:
            inc.setdefault(t['den'], []).append(t)
    for lst in inc.values():
        lst.sort(key=lambda t: by[t['tu']]['_cy'])
    for src, lst in fwd.items():
        lst.sort(key=lambda t: by[t['den']]['_y'])
        for i, t in enumerate(lst):
            a, b = by[t['tu']], by[t['den']]
            ins = inc[t['den']]; j = ins.index(t)
            fan_in = len(ins) > 1 and len(lst) == 1
            x1, y1 = a['_x'] + a['_w'], a['_cy'] + (i - (len(lst) - 1) / 2) * 16
            x2, y2 = b['_x'] - 2, b['_cy'] + ((j - (len(ins) - 1) / 2) * 16 if fan_in else 0)
            add(t, '<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (n(x1), n(y1), n(x2), n(y2)))
            yat = lambda xx: y1 + (y2 - y1) * (xx - x1) / (x2 - x1)
            bx = x1 + (x2 - x1) * (0.7 if fan_in else 0.5); byy = yat(bx)
            num(bx, byy, t)
            if t.get('nhan'):
                lw = tw(t['nhan'], 13)
                if abs(y2 - y1) < 20:
                    labels.append(text((x1 + x2) / 2, yat((x1 + x2) / 2) - (20 if t.get('so') is not None else 10), t['nhan'], 13,
                                       '#777' if t.get('net-dut') else '#222', anchor='middle'))
                elif fan_in:   # nhãn ở đoạn đầu (gần ô nguồn), phía ngoài chùm mũi tên
                    lx = x1 + (x2 - x1) * 0.12
                    ly = yat(lx) - 8 if y2 > y1 else yat(lx) + 18
                    labels.append(text(lx, ly, t['nhan'], 13))
                else:   # toả ra: nhãn phía ngoài, không cắt qua đường
                    lx = bx + 24
                    if y2 < y1:
                        ly = min(yat(lx), yat(lx + lw)) - 6
                    else:
                        ly = max(yat(lx), yat(lx + lw)) + 16
                    labels.append(text(lx, ly, t['nhan'], 13))
    for t in trs:
        a, b = by[t['tu']], by[t['den']]
        if b['cot'] > a['cot']:
            continue
        if b['cot'] == a['cot']:   # cùng cột: mũi tên thẳng đứng
            down = b['_y'] > a['_y']
            x = a['_cx']
            y1 = a['_y'] + a['_h'] if down else a['_y']
            y2 = b['_y'] - 2 if down else b['_y'] + b['_h'] + 2
            add(t, '<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (n(x), n(y1), n(x), n(y2)))
            num(x, (y1 + y2) / 2, t)
            if t.get('nhan'): labels.append(text(x + 20, (y1 + y2) / 2 + 4, t['nhan'], 13))
            continue
        # quay lại (sang cột trái): đường cong vòng phía dưới
        back = True
        p0 = (a['_x'], a['_y'] + a['_h'] - 14)
        p1 = (a['_x'] - 120, a['_y'] + a['_h'] + 46)
        p2 = (b['_cx'], max(a['_y'] + a['_h'] + 24, b['_y'] + b['_h'] + 60))
        p3 = (b['_cx'], b['_y'] + b['_h'] + 2)
        add(t, '<path d="M%s %s C %s %s, %s %s, %s %s"/>' % tuple(n(v) for v in (*p0, *p1, *p2, *p3)))
        def bez(tt):
            return tuple((1 - tt) ** 3 * p0[k] + 3 * (1 - tt) ** 2 * tt * p1[k] + 3 * (1 - tt) * tt ** 2 * p2[k] + tt ** 3 * p3[k] for k in (0, 1))
        bp = bez(0.62); lp = bez(0.4)
        num(bp[0], bp[1], t)
        if t.get('nhan'): labels.append(text(lp[0], lp[1] + 20, t['nhan'], 13, anchor='middle'))
    bottom = max(s['_y'] + s['_h'] for s in sts)
    W = max(right + 30, 760)
    H = bottom + (64 if back else 24)
    cthich = lines_of(d.get('chu-thich'))          # dòng chú thích dưới sơ đồ
    for i, x in enumerate(cthich):
        notes.append(text(20, H + 4 + 20 * i, x, 12.5, '#555', noh=True))
        W = max(W, 20 + tw(x, 12.5) + 20)
    H += 20 * len(cthich)
    body += boxes + ['<g stroke="%s" stroke-width="2.2" fill="none" marker-end="url(#%s)">' % (ARROW, mid)] + paths + ['</g>']
    if dpaths:
        body += ['<g stroke="#999" stroke-width="2" stroke-dasharray="6 4" fill="none" marker-end="url(#%sd)">' % mid] + dpaths + ['</g>']
    body += labels + badges + notes
    return svg_wrap(W, H, d.get('mo-ta', 'Sơ đồ trạng thái'), body)


VE = {'tong-quan': ve_tong_quan, 'tuan-tu': ve_tuan_tu, 'trang-thai': ve_trang_thai}

def ve(path, mid=None):
    """Đọc file JSON và trả về chuỗi <svg>. mid: tiền tố id mũi tên (phải khác nhau giữa các sơ đồ trong 1 trang)."""
    d = json.load(io.open(path, encoding='utf-8'))
    loai = d.get('loai')
    if loai not in VE:
        raise ValueError('%s: "loai" phải là một trong %s' % (path, ', '.join(VE)))
    mid = mid or 'm' + re.sub(r'\W', '', os.path.splitext(os.path.basename(path))[0])
    return VE[loai](d, mid)


def trang_xem_thu(svgs):
    """Trang HTML độc lập có font + CSS chuẩn, để xem thử sơ đồ."""
    import giao_dien
    divs = '\n'.join('<h3>%s</h3><div class="diag">%s</div>' % (esc(t), s) for t, s in svgs)
    page = '<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Xem thử sơ đồ</title>%s</head><body><div class="wrapper">%s</div></body></html>' % (giao_dien.std_block(), divs)
    return giao_dien.embed_fonts(page, CANH_BAO)


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Vẽ sơ đồ theo mẫu chuẩn từ file JSON')
    ap.add_argument('json', nargs='+')
    ap.add_argument('-o', '--out', default='xem-thu-so-do.html')
    a = ap.parse_args()
    out = []
    for i, p in enumerate(a.json):
        out.append((os.path.basename(p), ve(p, 'm%d' % i)))
    io.open(a.out, 'w', encoding='utf-8').write(trang_xem_thu(out))
    for w in CANH_BAO: print('Cảnh báo:', w)
    print('Đã vẽ %d sơ đồ → %s' % (len(out), a.out))
