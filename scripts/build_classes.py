#!/usr/bin/env python3
"""
build_classes.py
================
Script de sincronización y automatización de clases para el curso.

Funciones:
1. Lee las páginas de clases en clases/clase_*/index.qmd y extrae su metadata YAML.
2. Valida la presencia de archivos PDF y PPTX declarados.
3. Genera includes/menu-clases.generated.qmd con la estructura del sidebar según las clases publicadas.
4. Mantiene sincronizada la lista 'render' en _quarto.yml entre marcas seguras.
"""

import os
import re
import sys
import yaml
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

UNIDADES_INFO = {
    "0": {"id": "unidad0", "label": "Inicio", "title": "Presentación"},
    "1": {"id": "unidad1", "label": "Unidad I", "title": "Investigación Cuantitativa"},
    "2": {"id": "unidad2", "label": "Unidad II", "title": "Estadística en Investigación"},
    "3": {"id": "unidad3", "label": "Unidad III", "title": "Estadística Univariada"},
    "4": {"id": "unidad4", "label": "Unidad IV", "title": "Relaciones Bivariadas"},
}

def parse_class_qmd(qmd_path: Path) -> dict:
    content = qmd_path.read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
    if not m:
        return {}
    
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except Exception as e:
        print(f"[WARN] Error parseando YAML en {qmd_path}: {e}", file=sys.stderr)
        return {}

    clase_num = str(data.get("clase", "")).zfill(2)
    if not clase_num or clase_num == "00" and "clase" not in data:
        # Extraer del nombre de carpeta si no está explícito
        folder_match = re.search(r"clase_(\d+)", str(qmd_path))
        if folder_match:
            clase_num = folder_match.group(1).zfill(2)

    title = data.get("title", f"Clase {clase_num}")
    # Limpiar título para el menú si tiene formato 'Clase XX | Título'
    short_title = title
    if " | " in short_title:
        short_title = short_title.split(" | ", 1)[1].strip()
    elif " – " in short_title:
        parts = short_title.split(" – ", 1)
        if parts[0].strip().lower().startswith("clase"):
            short_title = parts[1].strip()

    orden = data.get("orden", int(clase_num) if clase_num.isdigit() else 99)
    unidad = data.get("unidad", "")
    unidad_titulo = data.get("unidad-titulo", "")
    
    # Determinar unidad_id
    unidad_id = "unidad0"
    if "present" in unidad.lower():
        unidad_id = "unidad0"
    elif "i–ii" in unidad.lower() or "i-ii" in unidad.lower():
        unidad_id = "unidad1"
    elif "iv" in unidad.lower():
        unidad_id = "unidad4"
    elif "iii" in unidad.lower():
        unidad_id = "unidad3"
    elif "ii" in unidad.lower():
        unidad_id = "unidad2"
    elif "i" in unidad.lower():
        unidad_id = "unidad1"
    else:
        # inferir de orden
        if orden == 0: unidad_id = "unidad0"
        elif orden in [1, 2]: unidad_id = "unidad1"
        elif orden == 3: unidad_id = "unidad2"
        elif orden in [4, 5, 6, 7]: unidad_id = "unidad3"
        else: unidad_id = "unidad4"

    # Publicada: Si tiene 'publicada', respetarla; si tiene 'draft', invertirla; por defecto True si orden <= 4
    if "publicada" in data:
        publicada = bool(data["publicada"])
    elif "draft" in data:
        publicada = not bool(data["draft"])
    else:
        publicada = (int(clase_num) <= 4) if clase_num.isdigit() else False

    pdf = data.get("pdf", f"clase_{clase_num}.pdf" if (qmd_path.parent / f"clase_{clase_num}.pdf").exists() else None)
    pptx = data.get("pptx", f"clase_{clase_num}.pptx" if (qmd_path.parent / f"clase_{clase_num}.pptx").exists() else None)

    # Validar materiales si está publicada
    if publicada:
        has_pdf = (qmd_path.parent / (pdf or "")).is_file() if pdf else False
        has_pptx = (qmd_path.parent / (pptx or "")).is_file() if pptx else False
        if not has_pdf and not has_pptx:
            print(f"[WARN] Clase {clase_num} ({qmd_path.parent.name}) está marcada como publicada pero no contiene PDF ni PPTX.", file=sys.stderr)

    return {
        "path": qmd_path,
        "rel_path": qmd_path.relative_to(WORKSPACE_ROOT).as_posix(),
        "clase": clase_num,
        "title": title,
        "short_title": short_title,
        "orden": orden,
        "unidad": unidad,
        "unidad_titulo": unidad_titulo,
        "unidad_id": unidad_id,
        "date": str(data.get("date", "")),
        "description": data.get("description", ""),
        "pdf": pdf,
        "pptx": pptx,
        "publicada": publicada
    }

def get_all_classes() -> list:
    clases_dir = WORKSPACE_ROOT / "clases"
    qmd_files = sorted(clases_dir.glob("clase_*/index.qmd"))
    classes = []
    for qmd in qmd_files:
        info = parse_class_qmd(qmd)
        if info:
            classes.append(info)
    classes.sort(key=lambda x: x["orden"])
    return classes

def generate_sidebar_qmd(classes: list) -> str:
    # Agrupar por unidad_id
    groups = {
        "unidad0": [],
        "unidad1": [],
        "unidad2": [],
        "unidad3": [],
        "unidad4": [],
    }
    for c in classes:
        uid = c["unidad_id"]
        if uid not in groups:
            groups[uid] = []
        groups[uid].append(c)

    lines = [
        "<!--",
        "  ====================================================================",
        "  ESTE ARCHIVO SE GENERA AUTOMÁTICAMENTE MEDIANTE scripts/build_classes.py",
        "  NO EDITAR MANUALMENTE.",
        "  Para agregar o publicar clases, edita el frontmatter de cada",
        "  archivo en clases/clase_XX/index.qmd y ejecuta quarto render.",
        "  ====================================================================",
        "-->",
        "```{=html}",
        '<div class="clases-sidebar-wrapper">',
        '  <button class="clases-sidebar-toggle" type="button" aria-label="Mostrar u ocultar menú de clases">',
        '    <i class="bi bi-chevron-right"></i>',
        '  </button>',
        '',
        '  <aside class="clases-sidebar">',
        '    <div class="nav flex-column nav-pills" id="clases-tabs" role="navigation" aria-label="Menú de clases">',
    ]

    for uid in ["unidad0", "unidad1", "unidad2", "unidad3", "unidad4"]:
        c_list = groups.get(uid, [])
        published_in_unit = [c for c in c_list if c["publicada"]]
        unit_meta = UNIDADES_INFO.get(uid.replace("unidad", ""), {"label": uid, "title": ""})
        label = unit_meta["label"]
        unit_title = unit_meta["title"]

        if not published_in_unit:
            # Unidad sin clases publicadas: se comenta en el menú para mantener limpieza visual
            lines.append("")
            lines.append(f"      <!-- {label} ({unit_title}) - Sin clases publicadas aún -->")
            continue

        lines.append("")
        lines.append(f"      <!-- {label} -->")
        lines.append('      <div class="sidebar-unit-header">')
        lines.append(f'        <button class="btn btn-link sidebar-unit-toggle" type="button" data-bs-toggle="collapse" data-bs-target="#{uid}" aria-expanded="false" aria-controls="{uid}">')
        lines.append('          <div class="unit-label-wrap">')
        lines.append(f'            <span class="unit-label">{label}</span>')
        lines.append(f'            <span class="unit-title">{unit_title}</span>')
        lines.append('          </div>')
        lines.append('          <i class="bi bi-chevron-down"></i>')
        lines.append('        </button>')
        lines.append('      </div>')
        lines.append("")
        lines.append(f'      <div class="collapse" id="{uid}">')
        for c in published_in_unit:
            c_num = c["clase"]
            c_title = c["short_title"]
            lines.append(f'        <a class="clase-link" href="../clase_{c_num}/index.html" data-clase-link="clase_{c_num}">Clase {c_num} – {c_title}</a>')
        lines.append('      </div>')

    lines.extend([
        "    </div>",
        "  </aside>",
        "</div>",
        "```",
        ""
    ])
    return "\n".join(lines)

def update_quarto_render_list(classes: list):
    quarto_yml = WORKSPACE_ROOT / "_quarto.yml"
    if not quarto_yml.exists():
        return

    content = quarto_yml.read_text(encoding="utf-8")

    start_marker = "    # AUTOGENERATED CLASES RENDER: START"
    end_marker = "    # AUTOGENERATED CLASES RENDER: END"

    published_lines = []
    hidden_lines = []

    for c in classes:
        if c["publicada"]:
            published_lines.append(f"    - {c['rel_path']}")
        else:
            hidden_lines.append(f"    # - {c['rel_path']} ({c['short_title']})")

    render_block = [start_marker]
    render_block.append("    # Clases publicadas activas:")
    render_block.extend(published_lines)
    if hidden_lines:
        render_block.append("    # Clases preparadas / ocultas (se publican con 'publicada: true'):")
        render_block.extend(hidden_lines)
    render_block.append(f"    {end_marker}")
    new_render_section = "\n".join(render_block)

    if start_marker in content and end_marker in content:
        pattern = re.compile(rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        new_content = pattern.sub(new_render_section, content)
    else:
        # Si aún no tiene marcadores, reemplazar la sección de clases bajo render:
        old_pattern = re.compile(
            r"([ \t]*# CLASES PUBLICADAS.*?(?:# - clases/clase_\d+/index\.qmd\r?\n)+)",
            re.DOTALL
        )
        if old_pattern.search(content):
            new_content = old_pattern.sub(new_render_section + "\n", content)
        else:
            # Reemplazar después de ultima-informacion/*.qmd
            target = "    - ultima-informacion/*.qmd"
            if target in content:
                new_content = content.replace(target, target + "\n\n" + new_render_section)
            else:
                new_content = content

    if new_content != content:
        quarto_yml.write_text(new_content, encoding="utf-8")
        print("[OK] _quarto.yml actualizado con clases publicadas.")

def update_clases_listing(classes: list):
    clases_qmd = WORKSPACE_ROOT / "clases.qmd"
    if not clases_qmd.exists():
        return

    content = clases_qmd.read_text(encoding="utf-8")
    start_marker = "    # AUTOGENERATED LISTING: START"
    end_marker = "    # AUTOGENERATED LISTING: END"

    published_items = [f'    - "{c["rel_path"]}"' for c in classes if c["publicada"]]
    block = [start_marker] + published_items + [end_marker]
    new_block = "\n".join(block)

    if start_marker in content and end_marker in content:
        pattern = re.compile(rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        new_content = pattern.sub(new_block, content)
        if new_content != content:
            clases_qmd.write_text(new_content, encoding="utf-8")
            print("[OK] clases.qmd listing actualizado.")

def main():
    classes = get_all_classes()
    published = [c for c in classes if c["publicada"]]
    hidden = [c for c in classes if not c["publicada"]]

    print(f"build_classes: {len(classes)} clases detectadas ({len(published)} publicadas, {len(hidden)} ocultas).")

    # 1. Generar includes/menu-clases.generated.qmd
    menu_qmd = WORKSPACE_ROOT / "includes" / "menu-clases.generated.qmd"
    menu_content = generate_sidebar_qmd(classes)
    menu_qmd.write_text(menu_content, encoding="utf-8")
    print(f"[OK] Generado {menu_qmd.relative_to(WORKSPACE_ROOT)}")

    # Mantener includes/menu-clases.qmd apuntando o sincronizado
    legacy_menu = WORKSPACE_ROOT / "includes" / "menu-clases.qmd"
    legacy_menu.write_text(menu_content, encoding="utf-8")

    # 2. Actualizar _quarto.yml
    update_quarto_render_list(classes)

    # 3. Actualizar clases.qmd
    update_clases_listing(classes)

    # 4. Limpiar directorios en docs/ para clases ocultas
    import shutil
    for c in hidden:
        hidden_doc = WORKSPACE_ROOT / "docs" / "clases" / f"clase_{c['clase']}"
        if hidden_doc.exists():
            shutil.rmtree(hidden_doc, ignore_errors=True)
            print(f"[OK] Limpiado directorio de clase oculta: {hidden_doc.relative_to(WORKSPACE_ROOT)}")

if __name__ == "__main__":
    main()
