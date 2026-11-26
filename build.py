"""Genera la vista previa del buscador de postulados TSJ (La Patilla Data)."""
import base64, csv, io, json
from pathlib import Path
from PIL import Image

HERE = Path(__file__).parent
CSV = Path.home() / "Documents/postulados-magistrados-TSJ-2026-11-20-completa.csv"
LOGO = Path.home() / "Downloads/LaPatilla-DATA.png"
LP_LIGHT = Path.home() / "proyectos/barra-patilla-2/img/lp-logo-light.png"
# Números de lista (columna n) de los postulados impugnados. Se llena solo cuando Rory lo indique.
IMPUGNADOS = [156, 350, 737, 706, 1, 221, 767, 116, 704, 731, 855, 83, 599, 643, 150, 555, 347, 80, 118, 205, 244, 254, 259, 264, 391, 423, 435, 439, 462, 641, 816, 867, 902, 971, 995, 1034]  # +19 magistrados vigentes, orden de Rory 25/11

rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
data = [[int(r["n"]), r["nombre"].strip(), r["cedula"].strip()] for r in rows]
assert len(data) == 1066, len(data)

im = Image.open(LOGO)
im = im.crop(im.getbbox())
im.thumbnail((360, 360))
buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
logo = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

lp = "data:image/png;base64," + base64.b64encode(LP_LIGHT.read_bytes()).decode()

# Candado: dentro de un iframe solo funciona si la página madre es de La Patilla (o su dominio espejo).
# ponytail: si el navegador no revela el origen (Firefox con no-referrer) se deja pasar para no romper La Patilla.
GUARD = r"""if (window.top !== window.self) {
  let host = '';
  try { const ao = location.ancestorOrigins; if (ao && ao.length) host = new URL(ao[0]).hostname; } catch (e) {}
  if (!host && document.referrer) try { host = new URL(document.referrer).hostname; } catch (e) {}
  if (host && !/(^|\.)lapatilla\.com$|^tyht\.cgixix\.com$/.test(host)) {
    document.body.innerHTML = '<p style="font:16px Georgia,serif;text-align:center;padding:40px 16px;color:#1E1E1C">Esta herramienta es de La Patilla Data. Consúltala en <a href="https://lapatilla.com" target="_top" style="color:#458A39">lapatilla.com</a>.</p>';
    throw new Error('lpdata: dominio no autorizado');
  }
}"""

tpl = (HERE / "template.html").read_text(encoding="utf-8")
body = tpl.replace("__LOGO__", logo).replace("__LP__", lp).replace("__IMP__", json.dumps(IMPUGNADOS)).replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":")))

# Vista previa del artifact (sin candado: el visor de Claude también usa un iframe)
(HERE / "postulados-tsj.html").write_text(body.replace("__GUARD__", ""), encoding="utf-8")

# Producción GitHub Pages: documento completo, sin indexar (el tráfico va a La Patilla), con candado
site = HERE
head = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="robots" content="noindex, nofollow">\n'
        '<style>body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style>\n')
prod = body.replace("__GUARD__", GUARD)
split = prod.index("</style>") + len("</style>")
(site / "index.html").write_text(head + prod[:split] + "\n</head>\n<body>\n" + prod[split:] + "\n</body>\n</html>\n", encoding="utf-8")
(site / ".nojekyll").write_text("")
print("ok", len(data), len(body) // 1024, "KB")
