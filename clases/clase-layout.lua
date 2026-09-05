--[[
  clase-layout.lua
  ================
  Filtro de Pandoc/Quarto para páginas de clases individuales.
  
  Automatiza la estructura completa de una clase a partir de su frontmatter:
  1. Genera el Hero (<section class="clase-hero">) con kicker, título y descripción.
  2. Genera el visor grande (<div class="class-presentation-viewer">) e iframe del PDF.
  3. Genera los botones de acción (.clase-presentacion-actions) alineados a la izquierda:
     - [Descargar PDF] (rojo vino)
     - [Descargar PowerPoint] (neutro, condicional si existe pptx)
     - [Pantalla completa] (neutro, con listener en assets/js/clase-viewer.js)
  4. Envuelve el contenido en el layout de dos columnas (#catedra, .clase-main).
  5. Agrega automáticamente la caja de comentarios Giscus.
  6. Agrega automáticamente el menú lateral (.column-margin) generado desde includes/.
  
  Permite que el archivo .qmd de la clase contenga ÚNICAMENTE YAML y Markdown docente.
]]

local function read_first_existing(paths)
  for _, p in ipairs(paths) do
    local f = io.open(p, "r")
    if f then
      local c = f:read("*a")
      f:close()
      return c
    end
  end
  return nil
end

local function clean_raw_html(content)
  if not content then return "" end
  -- Eliminar delimitadores ```{=html} y ```
  content = content:gsub("```%{=html%}\r?\n", "")
  content = content:gsub("\r?\n```%s*$", "")
  content = content:gsub("\r?\n```\r?\n", "\n")
  return content
end

function Pandoc(doc)
  local meta = doc.meta
  if not meta.clase then
    return doc
  end

  local clase_num = pandoc.utils.stringify(meta.clase)
  local title = pandoc.utils.stringify(meta.title or "")
  local unidad = meta.unidad and pandoc.utils.stringify(meta.unidad) or ""
  local kicker = meta.kicker and pandoc.utils.stringify(meta.kicker)
  if not kicker or kicker == "" then
    if unidad ~= "" then
      kicker = "Clase " .. clase_num .. " · " .. unidad
    else
      kicker = "Clase " .. clase_num
    end
  end
  local desc = meta.description and pandoc.utils.stringify(meta.description) or ""
  local pdf = meta.pdf and pandoc.utils.stringify(meta.pdf) or ""
  local pptx = meta.pptx and pandoc.utils.stringify(meta.pptx) or ""

  -- Verificar si el documento ya tiene la estructura manual (compatibilidad hacia atrás)
  local has_manual_catedra = false
  local has_manual_hero = false
  local has_manual_viewer = false

  for _, block in ipairs(doc.blocks) do
    if block.t == "Div" then
      if block.identifier == "catedra" or block.classes:includes("columns") then
        has_manual_catedra = true
      end
    elseif block.t == "RawBlock" and block.format == "html" then
      if block.text:find('class="clase-hero"') or block.text:find("clase%-hero") then
        has_manual_hero = true
      end
      if block.text:find("class%-presentation%-viewer") or block.text:find("clase%-presentacion%-actions") then
        has_manual_viewer = true
      end
    end
  end

  if has_manual_catedra then
    -- El documento ya incluye el envoltorio manual #catedra, no alterar
    return doc
  end

  local main_blocks = {}

  -- 1. Inyectar Hero si no existe manualmente
  if not has_manual_hero then
    local hero_html = '<section class="clase-hero">\n' ..
      '  <p class="clase-kicker">' .. kicker .. '</p>\n' ..
      '  <h1>' .. title .. '</h1>\n'
    if desc ~= "" then
      hero_html = hero_html .. '  <p>' .. desc .. '</p>\n'
    end
    hero_html = hero_html .. '</section>'
    table.insert(main_blocks, pandoc.RawBlock("html", hero_html))
  end

  -- 2. Inyectar Visor y Acciones si se definió PDF y no existe visor manual
  if not has_manual_viewer and pdf ~= "" then
    local viewer_html = '<div class="clase-card clase-card-presentation">\n' ..
      '  <div class="class-presentation-viewer" id="viewer-clase-' .. clase_num .. '">\n' ..
      '    <iframe src="' .. pdf .. '#view=FitH" title="Presentación Clase ' .. clase_num .. '" allowfullscreen=""></iframe>\n' ..
      '  </div>\n' ..
      '  <div class="clase-presentacion-actions">\n' ..
      '    <a href="' .. pdf .. '" class="btn btn-primary" download=""><i class="bi bi-file-earmark-pdf me-2"></i>Descargar PDF</a>\n'
    if pptx ~= "" then
      viewer_html = viewer_html .. '    <a href="' .. pptx .. '" class="btn btn-outline-secondary" download=""><i class="bi bi-file-earmark-ppt me-2"></i>Descargar PowerPoint</a>\n'
    end
    viewer_html = viewer_html .. '    <button type="button" class="btn btn-outline-secondary btn-presentation-fullscreen" id="btn-fullscreen-' .. clase_num .. '" data-action="fullscreen" data-target="#viewer-clase-' .. clase_num .. '" data-fallback-url="' .. pdf .. '"><i class="bi bi-arrows-fullscreen me-2"></i>Pantalla completa</button>\n' ..
      '  </div>\n' ..
      '</div>'
    table.insert(main_blocks, pandoc.RawBlock("html", viewer_html))
  end

  -- 3. Insertar los bloques de contenido del autor
  for _, block in ipairs(doc.blocks) do
    table.insert(main_blocks, block)
  end

  -- 4. Inyectar Comentarios Giscus al final de la columna principal
  local giscus_html = '<!-- Sistema de comentarios Giscus -->\n' ..
    '<section class="comments-box comments-giscus-box" aria-label="Espacio de comentarios">\n' ..
    '  <div class="comments-heading">\n' ..
    '    <h2 class="anchored">Preguntas, dudas y comentarios</h2>\n' ..
    '    <p class="text-muted small">\n' ..
    '      El canal de consultas y comentarios de la sesión estará habilitado durante el desarrollo del curso.\n' ..
    '    </p>\n' ..
    '  </div>\n' ..
    '  <div class="giscus"></div>\n' ..
    '</section>'
  table.insert(main_blocks, pandoc.RawBlock("html", giscus_html))

  -- 5. Crear columna principal
  local main_col = pandoc.Div(main_blocks, pandoc.Attr("", {"column", "clase-main"}))

  -- 6. Crear columna de margen con el menú lateral
  local sidebar_raw = read_first_existing({
    "../../includes/menu-clases.generated.qmd",
    "../includes/menu-clases.generated.qmd",
    "includes/menu-clases.generated.qmd",
    "../../includes/menu-clases.qmd",
    "includes/menu-clases.qmd"
  })

  local sidebar_html = clean_raw_html(sidebar_raw or '<aside class="clases-sidebar"><p>Menú no disponible</p></aside>')
  local margin_col = pandoc.Div({
    pandoc.RawBlock("html", sidebar_html)
  }, pandoc.Attr("", {"column-margin"}))

  -- 7. Envolver en contenedor #catedra
  local catedra_div = pandoc.Div({main_col, margin_col}, pandoc.Attr("catedra", {"columns"}))

  return pandoc.Pandoc({catedra_div}, meta)
end
