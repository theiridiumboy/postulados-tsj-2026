# Postulados al TSJ 2026 (La Patilla Data)

Buscador móvil de los 1.066 postulados a magistrados del TSJ, páginas de 25.
En vivo: https://theiridiumboy.github.io/postulados-tsj-2026/

## Actualizar

1. Impugnados: poner los números de lista (columna `n` del CSV) en `IMPUGNADOS` de `build.py`.
2. `python3 build.py` (regenera `index.html` y la vista previa del artifact).
3. `git commit -am "..." && git push`. Pages tarda ~1 min.

Datos: `~/Documents/postulados-magistrados-TSJ-2026-11-20-completa.csv`.

## Candado

Dentro de un iframe solo se muestra si la página madre es `lapatilla.com` (o subdominio) o el espejo `tyht.cgixix.com`.
En cualquier otro sitio muestra "Esta herramienta es de La Patilla Data" con enlace a lapatilla.com.
Abierta directo (sin iframe) funciona. Página marcada `noindex`.

## Código para insertar en La Patilla (bloque HTML personalizado)

```html
<iframe id="lpdata-tsj" src="https://theiridiumboy.github.io/postulados-tsj-2026/" title="Postulados a magistrados del TSJ, La Patilla Data" style="width:100%;height:2300px;border:0;display:block" loading="lazy"></iframe>
<script>
window.addEventListener('message', function (e) {
  if (e.origin === 'https://theiridiumboy.github.io' && e.data && e.data.lpdata === 'tsj-postulados') {
    document.getElementById('lpdata-tsj').style.height = e.data.h + 'px';
  }
});
</script>
```

El `<script>` ajusta la altura del iframe al contenido. Si WordPress lo quita, el iframe queda en 2300px fijos.
