<img src="resources/imagenes/logo.svg" alt="Logo del sitio" width="42" height="42" align="left" style="margin-right: 12px;"/>

# Métodos Cuantitativos

Sitio web oficial del curso **Métodos Cuantitativos** (código **ANT01221**), correspondiente a la **Escuela de Antropología** de la **Universidad Diego Portales (UDP)**, 2026.

**Docente:** Daniela Olivares Collío (`daniela.olivares2@mail.udp.cl`)  
**Ayudante:** Katherine Aravena Herrera (`katherine.aravena@mail.udp.cl`)  

**Repositorio:** [https://github.com/udp-metodos-cuantitativos/curso-2026](https://github.com/udp-metodos-cuantitativos/curso-2026)

---

## Descripción de la asignatura

La asignatura de **Métodos Cuantitativos** tiene como objetivo que las y los estudiantes conozcan y apliquen herramientas conceptuales y estadísticas básicas, principalmente a nivel descriptivo, para analizar fenómenos de las ciencias sociales de manera cuantitativa. 

El curso articula:

* Fundamentos y etapas del diseño de investigación cuantitativa.
* Medición de la realidad social, problematización, preguntas, objetivos e hipótesis estadísticas.
* Conceptualización, operacionalización, variables, atributos y niveles de medición.
* Nociones de universo, población, muestra y técnicas de recolección de datos.
* Elaboración de matrices de datos y libros de códigos.
* Estadística descriptiva univariada: distribución, frecuencias, medidas de tendencia central, dispersión, posición y forma.
* Análisis estadístico de relaciones bivariadas: tablas de contingencia, indicadores, índices, correlación de Pearson y regresión.
* Uso básico del software estadístico **R** como herramienta para el procesamiento y análisis descriptivo de datos sociales.

---

## Estructura del sitio web

El sitio centraliza los componentes pedagógicos de la asignatura:

* **Inicio (`index.qmd`):** Portada institucional, presentación del curso, equipo docente y últimas noticias.
* **Curso (`curso.qmd`):** Calendarización interactiva semana a semana, esquema formal de evaluaciones y fórmulas de cálculo (NP y NF), metodología y normativa académica de la Escuela de Antropología.
* **Clases (`clases/`):** Páginas individuales por sesión organizadas en las 4 unidades oficiales del curso, con resumen de contenidos, objetivos y diapositivas.
* **Bibliografía (`bibliografia.qmd`):** Catálogo de lecturas obligatorias (Ritchey) y complementarias (Johnson & Kuby, Cea D'Ancona, Agresti & Finlay, De Miguel) con acceso a documentos disponibles.
* **Recursos (`Recursos.qmd`):** Centro de apoyo interactivo con guías para instalación de R y RStudio, paquetes esenciales (`tidyverse`, `haven`, `janitor`, `psych`, `sjPlot`, `ggplot2`), manuales de apoyo, fuentes de datos sociales y solución de errores comunes.
* **Última información (`ultima-informacion.qmd`):** Avisos oficiales y novedades del curso.

---

## Tecnologías utilizadas

* [Quarto](https://quarto.org/) — Generación del sitio web estático.
* [Bootstrap 5](https://getbootstrap.com/) — Componentes visuales y maquetación responsive.
* [GitHub](https://github.com/) — Control de versiones y alojamiento del repositorio.
* HTML, CSS y JavaScript — Componentes interactivos personalizados (calendario dinámico, buscador y filtros).

---

## Estructura del repositorio

```text
├── _quarto.yml                     # Configuración general y navegación del sitio
├── index.qmd                       # Portada del curso
├── curso.qmd                       # Calendario, evaluaciones, metodología y normativa
├── bibliografia.qmd                # Catálogo bibliográfico del curso
├── Recursos.qmd                    # Centro de recursos de R, paquetes y datos
├── ultima-informacion.qmd          # Índice de noticias y avisos
├── styles.css                      # Hoja de estilos personalizados
├── README.md                       # Documentación del repositorio
│
├── clases/                         # Sesiones de cátedra
│   ├── clase_00/                   # Presentación y fundamentos
│   ├── clase_01/                   # Variables y operacionalización (Unidad I)
│   ├── clase_02/                   # Problema y matriz de datos (Unidades I–II)
│   ├── clase_03/                   # Población, muestra y recolección (Unidad II)
│   ├── clase_04/                   # Distribución y análisis univariado (Unidad III)
│   ├── clase_05/                   # Frecuencias y tablas (Unidad III)
│   ├── clase_06/                   # Tendencia central y dispersión (Unidad III)
│   ├── clase_07/                   # Posición y forma (Unidad III)
│   ├── clase_08/                   # Tablas de contingencia (Unidad IV)
│   ├── clase_09/                   # Indicadores, índices y escalas (Unidad IV)
│   ├── clase_10/                   # Correlación y regresión (Unidad IV)
│   ├── clase_11/                   # Taller de elaboración de trabajo grupal
│   └── clase_12/                   # Sesión de resolución de dudas
│
├── includes/                       # Componentes modulares reutilizables
│   ├── menu-clases.qmd             # Menú lateral acordeón de clases
│   ├── comentarios-giscus.qmd      # Contenedor de comentarios
│   └── comentarios-netlify.qmd     # Formulario alternativo de contacto
│
├── ultima-informacion/             # Artículos y noticias
│   └── 2026-08-11-bienvenida-curso.qmd
│
├── resources/                      # Recursos estáticos
│   ├── imagenes/                   # Logos e iconos del sitio
│   ├── post/                       # Imágenes destacadas para noticias
│   ├── biblio/                     # Archivos PDF de la biblioteca
│   ├── Daniela.jpg                 # Fotografía docente
│   ├── Katherine.jpg               # Fotografía ayudante
│   └── ELSOC_W06_v1.0_SPSS.sav     # Base de datos de práctica
│
└── docs/                           # Sitio web generado y compilado
```

---

## Licencias

| Tipo | Licencia |
|---|---|
| **Contenido** (textos, programas y guías) | [Creative Commons Atribución-NoComercial 4.0 Internacional (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/) |
| **Código** (HTML, CSS, JavaScript, scripts R) | [Licencia MIT](https://opensource.org/licenses/MIT) |
