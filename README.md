# portfolio.andminin.biz

Portfolio estático de Andrea Minin y ANDMININ Engineering, orientado a oportunidades senior de backend, arquitectura de soluciones y plataformas.

## Objetivo

Presentar experiencia profesional y artefactos técnicos públicos sin mezclar información confidencial ni describir repositorios de referencia como sistemas productivos.

## Stack

- HTML semántico
- CSS responsive
- GitHub Pages
- Python para validaciones locales y CI

El contenido principal se entrega directamente en HTML. La página no depende de JavaScript para mostrar información o navegar.

## Estructura

```text
assets/images/       Metadata visual
css/styles.css       Estilos y layout responsive
docs/static-server.mjs  Servidor local opcional con Node.js
scripts/validate.py  Validaciones estáticas sin dependencias externas
index.html           Contenido y metadatos del portfolio
robots.txt           Política de rastreo
sitemap.xml          Sitemap público
```

## Desarrollo local

Con Node.js:

```powershell
node docs/static-server.mjs
```

Alternativa con Python:

```bash
python3 -m http.server 4173 --bind 127.0.0.1
```

## Validación

```bash
python3 scripts/validate.py
```

La validación comprueba HTML, identificadores y anchors, referencias a archivos locales, sitemap, URLs canónicas y ausencia de contenido provisional.

## Publicación

GitHub Pages publica la rama `main` desde la raíz del repositorio. La URL activa es:

https://andminin-engineering.github.io/portfolio.andminin.biz/

El dominio `portfolio.andminin.biz` requiere una configuración DNS/CNAME independiente antes de utilizarse.
