/**
 * clases-menu.js
 * Comportamiento de navegación, persistencia y estado del menú lateral de clases.
 */
document.addEventListener("DOMContentLoaded", function () {
  const path = window.location.pathname;
  const unitStateKey = "clases-menu-unidades-ant01221";

  function readUnitState() {
    try {
      return JSON.parse(window.localStorage.getItem(unitStateKey)) || {};
    } catch (error) {
      return {};
    }
  }

  function writeUnitState(state) {
    try {
      window.localStorage.setItem(unitStateKey, JSON.stringify(state));
    } catch (error) {
      // localStorage puede no estar disponible en algunos contextos privados.
    }
  }

  function setUnitOpen(button, panel, isOpen) {
    button.setAttribute("aria-expanded", isOpen ? "true" : "false");
    panel.classList.toggle("show", isOpen);
  }

  const unitState = readUnitState();

  document.querySelectorAll(".sidebar-unit-toggle[data-bs-target]").forEach(function (button) {
    const target = button.getAttribute("data-bs-target");
    const panel = target ? document.querySelector(target) : null;

    if (!panel || !panel.id) return;

    // Si no hay estado guardado, por defecto abre la unidad que contenga el enlace activo
    const hasActiveLink = panel.querySelector("[data-clase-link].active") !== null;
    const shouldOpen = unitState[panel.id] !== undefined ? unitState[panel.id] === true : hasActiveLink;

    setUnitOpen(button, panel, shouldOpen);

    panel.addEventListener("shown.bs.collapse", function () {
      const currentState = readUnitState();
      currentState[panel.id] = true;
      writeUnitState(currentState);
    });

    panel.addEventListener("hidden.bs.collapse", function () {
      const currentState = readUnitState();
      currentState[panel.id] = false;
      writeUnitState(currentState);
    });
  });

  document.querySelectorAll("[data-clase-link]").forEach(function (link) {
    const clase = link.dataset.claseLink;

    if (
      path.includes("/" + clase + "/") ||
      path.endsWith("/" + clase + "/index.html") ||
      path.endsWith("/" + clase + "/")
    ) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
      const parentCollapse = link.closest(".collapse");
      if (parentCollapse) {
        parentCollapse.classList.add("show");
        const trigger = document.querySelector(`[data-bs-target="#${parentCollapse.id}"]`);
        if (trigger) trigger.setAttribute("aria-expanded", "true");
      }
    }
  });

  const toggle = document.querySelector(".clases-sidebar-toggle");
  const icon = toggle ? toggle.querySelector("i") : null;

  if (!toggle || !icon) return;

  toggle.addEventListener("click", function () {
    document.body.classList.toggle("sidebar-clases-collapsed");

    if (document.body.classList.contains("sidebar-clases-collapsed")) {
      icon.classList.remove("bi-chevron-right");
      icon.classList.add("bi-chevron-left");
    } else {
      icon.classList.remove("bi-chevron-left");
      icon.classList.add("bi-chevron-right");
    }
  });
});
