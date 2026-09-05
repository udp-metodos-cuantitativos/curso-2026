/**
 * clase-viewer.js
 * Manejo de pantalla completa y acciones del visor de presentaciones.
 */
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("[data-action='fullscreen'], .btn-presentation-fullscreen").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const targetSelector = btn.getAttribute("data-target");
      const fallbackUrl = btn.getAttribute("data-fallback-url");
      let viewer = null;

      if (targetSelector) {
        viewer = document.querySelector(targetSelector);
      }
      if (!viewer) {
        const card = btn.closest(".clase-card-presentation") || btn.closest(".clase-main") || document;
        viewer = card.querySelector(".class-presentation-viewer");
      }

      if (!viewer) {
        if (fallbackUrl) {
          window.open(fallbackUrl, "_blank");
        }
        return;
      }

      if (!document.fullscreenElement) {
        if (viewer.requestFullscreen) {
          viewer.requestFullscreen().catch(function () {
            if (fallbackUrl) window.open(fallbackUrl, "_blank");
          });
        } else if (viewer.webkitRequestFullscreen) {
          viewer.webkitRequestFullscreen();
        } else if (viewer.msRequestFullscreen) {
          viewer.msRequestFullscreen();
        } else if (fallbackUrl) {
          window.open(fallbackUrl, "_blank");
        }
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
          document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) {
          document.msExitFullscreen();
        }
      }
    });
  });
});
