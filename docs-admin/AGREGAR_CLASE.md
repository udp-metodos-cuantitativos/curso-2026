# Guía de Administración · Cómo Agregar o Publicar una Clase

Esta guía explica cómo publicar una nueva clase en el sitio web del curso sin necesidad de saber HTML, CSS ni JavaScript.

---

## Flujo Rápido en 6 Pasos

```text
1. Copiar la carpeta 'clases/_plantilla' a 'clases/clase_XX'
2. Colocar los archivos 'clase_XX.pdf' y/o 'clase_XX.pptx' dentro de esa carpeta
3. Abrir 'clases/clase_XX/index.qmd' y completar los datos del encabezado YAML
4. Redactar los contenidos de la sesión en Markdown simple
5. Cambiar 'publicada: true' y 'draft: false'
6. Ejecutar: quarto render
```

---

## 1. Copiar la Plantilla

Toma la carpeta:
```text
clases/_plantilla/
```
y crea una copia nombrándola según el número de la sesión (dos dígitos):
```text
clases/clase_05/
```

Dentro encontrarás el archivo:
```text
clases/clase_05/index.qmd
```

---

## 2. Agregar los Archivos de la Presentación

Guarda los archivos directamente dentro de la carpeta `clases/clase_05/`:
* `clase_05.pdf` (para el visor y botón de descarga)
* `clase_05.pptx` (opcional, para el botón de descarga)

> **Nota:** El sistema detecta automáticamente si los archivos existen. Si no hay PPTX, el botón correspondiente no se mostrará.

---

## 3. Configurar el Encabezado (YAML)

Abre `index.qmd`. En la parte superior verás un bloque entre líneas `---`:

```yaml
---
title: "Frecuencias y tablas descriptivas"
clase: "05"
unidad: "Unidad III"
unidad-titulo: "Estadística Univariada"
orden: 5
date: 2026-09-29
description: "Construcción, lectura e interpretación de tablas de frecuencias absolutas en R."
pdf: "clase_05.pdf"
pptx: "clase_05.pptx"
publicada: true
draft: false
---
```

### Campos:
* **`title`**: Nombre completo de la clase.
* **`clase`**: Número de dos dígitos (`"00"`, `"01"`, `"05"`, etc.).
* **`unidad`**: Nombre de la unidad (ej. `"Unidad III"`).
* **`unidad-titulo`**: Subtítulo temático de la unidad (ej. `"Estadística Univariada"`).
* **`orden`**: Número entero para ordenar la secuencia del semestre (`0`, `1`, `5`, etc.).
* **`date`**: Fecha de la clase en formato `AAAA-MM-DD`.
* **`description`**: Breve resumen de 1 a 2 líneas que aparecerá en el hero y en el listado general.
* **`pdf`**: Nombre del archivo PDF en la misma carpeta.
* **`pptx`**: Nombre del archivo PowerPoint (si existe).
* **`publicada`**: `true` para hacerla visible; `false` para mantenerla oculta.
* **`draft`**: `false` cuando está publicada; `true` cuando está en borrador.

---

## 4. Escribir los Contenidos Académicos

Debajo del encabezado escribe normalmente en Markdown:

```markdown
::: {.clase-card .clase-intro}

## Contenidos de la sesión

En esta clase aprenderemos a construir tablas de frecuencias...

::: {.clase-objetivos}

::: {.objetivo-card}
**Frecuencias absolutas**

Contar el número de casos en cada categoría de respuesta.
:::

::: {.objetivo-card}
**Frecuencias relativas**

Calcular proporciones y porcentajes para comparar categorías.
:::

:::

:::
```

---

## 5. Publicar y Compilar el Sitio

Abre la terminal en la carpeta principal del curso y ejecuta:

```bash
quarto render
```

### ¿Qué hace el sistema automáticamente?
1. Detecta la nueva clase y sus materiales.
2. Agrega la clase a la lista de compilación (`_quarto.yml`).
3. Agrega la clase al menú lateral (`includes/menu-clases.generated.qmd`).
4. Agrega la clase a la página general de listado (`clases.html`).
5. Construye el visor grande de diapositivas, los botones de descarga y el botón de pantalla completa.
6. Conecta el espacio de comentarios al final de la página.

**No es necesario editar manualmente ningún archivo HTML, CSS, JavaScript ni el menú lateral.**
