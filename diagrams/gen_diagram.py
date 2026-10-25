"""Hybrid IAM lab topology, drawn as SVG (README) and .excalidraw (editable) from one model."""
import base64, json, random, sys, time
from html import escape

OUT = sys.argv[1]
W, H = 1600, 1000
FONT = "Arial, Helvetica, sans-serif"
BLUE, INK, GREY, ORANGE, PURPLE = "#1f5fa8", "#1a1a1a", "#7a7a7a", "#c05600", "#6b3fa0"

# ---------- Cisco-style icons (64x64 viewBox) ----------
ICONS = {
"switch": f'<rect x="4" y="18" width="56" height="28" rx="3" fill="{BLUE}"/><g stroke="#fff" stroke-width="2.5" fill="none" stroke-linecap="round"><path d="M14 27h18M28 23l4 4-4 4M50 37H32M36 33l-4 4 4 4"/></g>',
"server": f'<rect x="18" y="4" width="28" height="56" rx="2" fill="{BLUE}"/><g fill="#fff"><rect x="23" y="11" width="18" height="3"/><rect x="23" y="18" width="18" height="3"/><rect x="23" y="25" width="18" height="3"/><circle cx="32" cy="50" r="2.5"/></g>',
"laptop": f'<rect x="12" y="12" width="40" height="28" rx="2" fill="{BLUE}"/><rect x="16" y="16" width="32" height="20" fill="#fff"/><path d="M6 44h52l-4 7H10z" fill="{BLUE}"/>',
"ap": f'<circle cx="32" cy="32" r="26" fill="{BLUE}"/><g stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"><path d="M22 30a14 14 0 0 1 20 0M17 24a21 21 0 0 1 30 0"/></g><circle cx="32" cy="38" r="3.5" fill="#fff"/>',
"cloud": f'<path d="M16 48h34a11 11 0 0 0 1-22 15 15 0 0 0-29-3 12 12 0 0 0-6 25z" fill="#fff" stroke="{GREY}" stroke-width="2.5"/>',
"entra": f'<path d="M32 6 56 34 32 58 8 34z" fill="#fff" stroke="{BLUE}" stroke-width="3"/><path d="M32 6v52M8 34h48" stroke="{BLUE}" stroke-width="2"/>',
"azure": f'<path d="M16 48h34a11 11 0 0 0 1-22 15 15 0 0 0-29-3 12 12 0 0 0-6 25z" fill="#fff" stroke="{BLUE}" stroke-width="2.5"/><g fill="{BLUE}"><rect x="24" y="32" width="6" height="6"/><rect x="34" y="32" width="6" height="6"/></g>',
}
def icon_svg(name):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">{ICONS[name]}</svg>'

# ---------- primitives (rendered to both formats) ----------
P = []
def zone(x, y, w, h, title, color=INK, dashed=False, fill="#ffffff"):
    P.append(("rect", x, y, w, h, color, fill, dashed, 1.5))
    P.append(("rect", x, y, w, 26, color, color if not dashed else "#ffffff", dashed, 1.5))
    P.append(("text", x + 10, y + 18, title, 13, "#ffffff" if not dashed else color, True, "start"))
def text(x, y, s, size=12, color=INK, bold=False, anchor="start"):
    P.append(("text", x, y, s, size, color, bold, anchor))
def line(pts, color=INK, dashed=False, arrows=(None, None), width=1.6):
    P.append(("line", pts, color, dashed, arrows, width))
def icon(name, cx, cy, s):
    P.append(("icon", name, cx - s / 2, cy - s / 2, s))
def table(x, y, rows, colw, rowh=18, head=False):
    for r, row in enumerate(rows):
        cx = x
        for c, cell in enumerate(row):
            hdr = head and r == 0
            P.append(("rect", cx, y + r * rowh, colw[c], rowh, "#9a9a9a", "#e8eef6" if hdr or (c == 0 and not head) else "#ffffff", False, 1))
            text(cx + 5, y + r * rowh + 13, cell, 11, INK, hdr or (c == 0 and not head))
            cx += colw[c]
def device(name, cx, cy, s, rows, colw=(70, 150)):
    icon(name, cx, cy, s)
    table(cx - sum(colw) / 2, cy + s / 2 + 8, rows, colw)

# ---------- drawing ----------
# Building network
zone(40, 40, 820, 150, "BUILDING NETWORK  (UPSTREAM, NOT MANAGED)", GREY, fill="#fafafa")
icon("cloud", 450, 112, 70)
text(500, 106, "Internet access via wall drop", 12, INK, True)
text(500, 122, "Upstream DHCP for 10.17.29.0/24", 11, GREY)

# Lab LAN
zone(40, 230, 820, 540, "LAB LAN  10.17.29.0/24")
device("switch", 450, 300, 70, [["Host", "SW01"], ["Model", "TP-Link TL-SG108E"], ["Ports", "8 x 1 GbE"]])
line([(450, 148), (450, 278)], INK)
text(458, 230 - 8, "Uplink (wall drop)", 11, GREY)
# access bus
line([(450, 397), (450, 420)]); line([(150, 420), (720, 420)])
for x in (150, 435, 720):
    line([(x, 420), (x, 470)])
device("ap", 150, 500, 54, [["Host", "AP01"], ["Role", "Wireless access"], ["Status", "Not yet configured"]], (60, 140))
device("laptop", 435, 500, 60, [["Host", "MacBook-Air-1027"], ["OS", "macOS (Apple M4)"], ["IP", "10.17.29.215 (DHCP)"], ["NIC", "AX88179B USB-C GbE"], ["Role", "Admin workstation"]], (60, 150))
device("server", 720, 500, 60, [["Host", "DC01"], ["HW", "Dell OptiPlex"], ["OS", "Windows Server"], ["IP", "10.17.29.219"], ["Roles", "AD DS, DNS"]], (60, 140))
line([(470, 492), (686, 492)], BLUE, True, ("arrow", "arrow"))
text(578, 484, "RDP 3389", 11, BLUE, True, "middle")
# tailnet overlay
P.append(("rect", 318, 455, 525, 290, PURPLE, None, True, 1.5))
text(328, 738, "TAILNET 100.64.0.0/10  (PLANNED)", 12, PURPLE, True)

# Active Directory
zone(900, 40, 320, 730, "ACTIVE DIRECTORY  lab.local", ORANGE, fill="#fffaf3")
ou = [("lab.local", 0, True), ("Domain Controllers", 1, False), ("Admin", 1, True), ("Tier 0", 2, False), ("Tier 1", 2, False),
      ("Tier 2", 2, False), ("Employees", 1, False), ("Contractors", 1, False), ("Service Accounts", 1, False), ("Groups", 1, False)]
text(915, 90, "OU structure", 12, ORANGE, True)
for i, (n, d, b) in enumerate(ou):
    y = 115 + i * 22
    if d: line([(917 + (d - 1) * 20, y - 5), (930 + (d - 1) * 20, y - 5)], GREY, width=1)
    text(935 + (d - 1) * 20 if d else 915, y, n, 12, INK, b)
line([(917, 120), (917, 312)], GREY, width=1); line([(937, 164), (937, 225)], GREY, width=1)
text(915, 360, "Identity", 12, ORANGE, True)
table(915, 370, [["Users", "50"], ["Group model", "AGDLP"], ["File shares", "8 departments (SMB)"]], (100, 190))
text(915, 460, "Group Policy and controls", 12, ORANGE, True)
table(915, 470, [["Tier-0 isolation", "Built"], ["Windows LAPS", "Built"], ["Audit logging", "Built"], ["PS transcription", "Planned"]], (190, 100))
line([(750, 492), (900, 492)], ORANGE, True, (None, "arrow"))
text(825, 484, "hosts", 11, ORANGE, True, "middle")

# Entra tenant
zone(1260, 40, 300, 290, "ENTRA ID TENANT  (PLANNED)", BLUE, dashed=True, fill="#f6f9fd")
icon("entra", 1410, 110, 56)
table(1275, 160, [["Component", "Phase"], ["Entra Connect Sync (PHS)", "1"], ["Break-glass accounts", "1"], ["Conditional Access, MFA", "2"],
                  ["PIM (just-in-time)", "3"], ["Identity Protection", "4"], ["Microsoft Sentinel", "4"], ["Graph PowerShell JML", "6"]], (215, 55), head=True)
line([(1220, 200), (1260, 200)], BLUE, True, (None, "arrow"))
text(1240, 192, "Sync", 11, BLUE, True, "middle")

# Azure
zone(1260, 370, 300, 400, "AZURE SUBSCRIPTION  (PLANNED)", BLUE, dashed=True, fill="#f6f9fd")
icon("azure", 1410, 440, 60)
table(1275, 485, [["VNet", "Lab VMs, no public IPs"], ["NSG", "Deny all inbound"], ["Access", "Tailscale only"], ["IaC", "Terraform"], ["Cost", "Auto-shutdown 23:00"]], (70, 200))

# Flows table
text(40, 805, "TRAFFIC FLOWS", 12, INK, True)
table(40, 815, [["Source", "Destination", "Service", "Port", "Status"],
                ["MacBook-Air-1027", "DC01", "RDP", "TCP 3389", "Active"],
                ["MacBook-Air-1027", "DC01", "SSH (OpenSSH)", "TCP 22", "Pending"],
                ["Domain clients", "DC01", "DNS, Kerberos, LDAP", "53, 88, 389", "Active"],
                ["DC01", "Entra ID", "Entra Connect Sync", "TCP 443", "Planned"]], (140, 90, 140, 90, 70), head=True)

# Legend
text(640, 805, "LEGEND", 12, INK, True)
for i, (lab, col, d) in enumerate([("Ethernet (physical)", INK, False), ("Management session", BLUE, True),
                                   ("Directory service / sync", ORANGE, True), ("Overlay network (planned)", PURPLE, True)]):
    y = 830 + i * 22
    line([(640, y), (690, y)], col, d)
    text(700, y + 4, lab, 11)

# Title block
tb = [["Project", "Hybrid Identity and Access Management Lab"], ["Drawing", "Physical and logical topology"],
      ["Author", "Emily Huynh"], ["Date", "2026-10-20"], ["Revision", "1.0"]]
table(1100, 815, tb, (90, 370), rowh=22)

# ---------- SVG ----------
DA, DB = ' stroke-dasharray="8 5"', ' stroke-dasharray="7 4"'
def build_svg():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
         '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" fill="context-stroke"/></marker></defs>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    for p in P:
        if p[0] == "rect":
            _, x, y, w, h, c, f, d, sw = p
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{f or "none"}" stroke="{c}" stroke-width="{sw}"{DA if d else ""}/>')
        elif p[0] == "text":
            _, x, y, s, sz, c, b, a = p
            o.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{sz}" font-weight="{700 if b else 400}" fill="{c}" text-anchor="{a}">{escape(s)}</text>')
        elif p[0] == "line":
            _, pts, c, d, (a0, a1), sw = p
            m = (' marker-start="url(#ah)"' if a0 else "") + (' marker-end="url(#ah)"' if a1 else "")
            o.append(f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{c}" stroke-width="{sw}"{DB if d else ""}{m}/>')
        elif p[0] == "icon":
            _, n, x, y, s = p
            o.append(f'<svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="0 0 64 64">{ICONS[n]}</svg>')
    o.append("</svg>")
    return "\n".join(o)

# ---------- Excalidraw ----------
def build_excalidraw():
    rng, now, els, files = random.Random(7), int(time.time() * 1000), [], {}
    def el(t, x, y, w, h, **kw):
        e = dict(id=f"{t}-{len(els)}", type=t, x=x, y=y, width=w, height=h, angle=0, strokeColor=INK,
                 backgroundColor="transparent", fillStyle="solid", strokeWidth=1, strokeStyle="solid", roughness=0,
                 opacity=100, groupIds=[], frameId=None, roundness=None, seed=rng.randint(1, 2**30), version=1,
                 versionNonce=rng.randint(1, 2**30), isDeleted=False, boundElements=None, updated=now, link=None, locked=False)
        e.update(kw); els.append(e)
    for p in P:
        if p[0] == "rect":
            _, x, y, w, h, c, f, d, sw = p
            el("rectangle", x, y, w, h, strokeColor=c, backgroundColor=f or "transparent", strokeStyle="dashed" if d else "solid", strokeWidth=sw)
        elif p[0] == "text":
            _, x, y, s, sz, c, b, a = p
            w = len(s) * sz * (0.6 if b else 0.55)
            x = x - w / 2 if a == "middle" else x
            el("text", x, y - sz, w, sz * 1.25, strokeColor=c, text=s, originalText=s, fontSize=sz, fontFamily=2,
               textAlign="left", verticalAlign="top", containerId=None, lineHeight=1.25, autoResize=True)
        elif p[0] == "line":
            _, pts, c, d, (a0, a1), sw = p
            x0, y0 = pts[0]
            rel = [[x - x0, y - y0] for x, y in pts]
            el("arrow" if a0 or a1 else "line", x0, y0, max(abs(r[0]) for r in rel) or 1, max(abs(r[1]) for r in rel) or 1,
               strokeColor=c, strokeStyle="dashed" if d else "solid", strokeWidth=sw, points=rel, lastCommittedPoint=None,
               startBinding=None, endBinding=None, startArrowhead=a0, endArrowhead=a1)
        elif p[0] == "icon":
            _, n, x, y, s = p
            fid = f"icon-{n}"
            files[fid] = dict(mimeType="image/svg+xml", id=fid, created=now,
                              dataURL="data:image/svg+xml;base64," + base64.b64encode(icon_svg(n).encode()).decode())
            el("image", x, y, s, s, fileId=fid, status="saved", scale=[1, 1], strokeColor="transparent")
    return dict(type="excalidraw", version=2, source="https://excalidraw.com", elements=els,
                appState=dict(viewBackgroundColor="#ffffff", gridSize=None), files=files)

open(f"{OUT}/hybrid-iam-lab.svg", "w").write(build_svg())
json.dump(build_excalidraw(), open(f"{OUT}/hybrid-iam-lab.excalidraw", "w"))
print("ok", len(P), "primitives")
