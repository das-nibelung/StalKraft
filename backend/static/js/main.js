/**
 * Template Name: UpConstruction - v1.3.0
 * Template URL: https://bootstrapmade.com/upconstruction-bootstrap-construction-website-template/
 * Author: BootstrapMade.com
 * License: https://bootstrapmade.com/license/
 */
document.addEventListener("DOMContentLoaded", () => {
  "use strict";
  // === Spectral-style WORD preloader ===
  // StalKraft word-preloader (устойчивый)
  // StalKraft word-preloader — показываем только при первом заходе (в рамках вкладки)
  (() => {
    const KEY = "sk_preloader_shown";
    const FALLBACK_KILL_MS = 4000; // страховка: уберём прелоадер в любом случае

    function init() {
      const reduce = window.matchMedia(
        "(prefers-reduced-motion: reduce)",
      ).matches;
      const alreadyShown = (function () {
        try {
          return sessionStorage.getItem(KEY) === "1";
        } catch (e) {
          return false;
        }
      })();

      const preloader = document.getElementById("preloader");
      const word = preloader
        ? preloader.querySelector(".preloader-word")
        : null;

      // Если прелоадер уже показывали, или анимации отключены, или разметка неполная — просто показываем сайт
      if (reduce || alreadyShown || !preloader || !word) {
        document.body.classList.remove("is-preload");
        if (preloader) preloader.remove();
        return;
      }

      // Ставим флажок "прелоадер уже был" — все последующие страницы в этой вкладке его пропустят
      try {
        sessionStorage.setItem(KEY, "1");
      } catch (e) {}

      let cleaned = false;
      const cleanup = () => {
        if (cleaned) return;
        cleaned = true;

        document.body.classList.remove("is-preload");

        preloader.classList.add("preloader-hide");
        const cs = getComputedStyle(preloader);
        const hasTransition = cs.transitionDuration
          .split(",")
          .some((d) => parseFloat(d) > 0);
        if (hasTransition) {
          // на всякий случай «тычок» рефлоу
          void preloader.offsetHeight;
          preloader.addEventListener(
            "transitionend",
            () => preloader.remove(),
            { once: true },
          );
          setTimeout(() => preloader.remove(), 1200); // страховка
        } else {
          preloader.remove();
        }
      };

      // Запуск анимации слова
      requestAnimationFrame(() => {
        word.classList.add("play");
        // если CSS не подгрузился/анимации нет — убираем сразу
        const animName = getComputedStyle(word).animationName;
        if (!animName || animName === "none") setTimeout(cleanup, 50);
      });

      // Основной триггер завершения
      word.addEventListener("animationend", cleanup, { once: true });
      word.addEventListener("webkitAnimationEnd", cleanup, { once: true });

      // Жёсткий фолбэк
      setTimeout(cleanup, FALLBACK_KILL_MS);
    }

    window.addEventListener("load", init, { once: true });

    // Возврат из BFCache (назад/вперёд) — прелоадер не нужен
    window.addEventListener("pageshow", (e) => {
      if (e.persisted) {
        const p = document.getElementById("preloader");
        document.body.classList.remove("is-preload");
        if (p) p.remove();
      }
    });
  })();

  /**
   * Preloader
   */
  /*const preloader = document.querySelector("#preloader");
  if (preloader) {
    window.addEventListener("load", () => {
      preloader.remove();
    });
  }
  */
  /**
   * Mobile nav toggle
   */

  const mobileNavShow = document.querySelector(".mobile-nav-show");
  const mobileNavHide = document.querySelector(".mobile-nav-hide");

  document.querySelectorAll(".mobile-nav-toggle").forEach((el) => {
    el.addEventListener("click", function (event) {
      event.preventDefault();
      mobileNavToogle();
    });
  });

  function mobileNavToogle() {
    document.querySelector("body").classList.toggle("mobile-nav-active");
    mobileNavShow.classList.toggle("d-none");
    mobileNavHide.classList.toggle("d-none");
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll("#navbar a").forEach((navbarlink) => {
    if (!navbarlink.hash) return;

    let section = document.querySelector(navbarlink.hash);
    if (!section) return;

    navbarlink.addEventListener("click", () => {
      if (document.querySelector(".mobile-nav-active")) {
        mobileNavToogle();
      }
    });
  });

  /**
   * Toggle mobile nav dropdowns
   */
  const navDropdowns = document.querySelectorAll(".navbar .dropdown > a");

  navDropdowns.forEach((el) => {
    el.addEventListener("click", function (event) {
      if (document.querySelector(".mobile-nav-active")) {
        event.preventDefault();
        this.classList.toggle("active");
        this.nextElementSibling.classList.toggle("dropdown-active");

        let dropDownIndicator = this.querySelector(".dropdown-indicator");
        dropDownIndicator.classList.toggle("bi-chevron-up");
        dropDownIndicator.classList.toggle("bi-chevron-down");
      }
    });
  });

  /**
   * Scroll top button
   */
  const scrollTop = document.querySelector(".scroll-top");
  if (scrollTop) {
    const togglescrollTop = function () {
      window.scrollY > 100
        ? scrollTop.classList.add("active")
        : scrollTop.classList.remove("active");
    };
    window.addEventListener("load", togglescrollTop);
    document.addEventListener("scroll", togglescrollTop);
    scrollTop.addEventListener("click", (e) => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: ".glightbox",
  });

  /**
   * Porfolio isotope and filter
   */
  let portfolionIsotope = document.querySelector(".portfolio-isotope");

  if (portfolionIsotope) {
    let portfolioFilter = portfolionIsotope.getAttribute(
      "data-portfolio-filter",
    )
      ? portfolionIsotope.getAttribute("data-portfolio-filter")
      : "*";
    let portfolioLayout = portfolionIsotope.getAttribute(
      "data-portfolio-layout",
    )
      ? portfolionIsotope.getAttribute("data-portfolio-layout")
      : "masonry";
    let portfolioSort = portfolionIsotope.getAttribute("data-portfolio-sort")
      ? portfolionIsotope.getAttribute("data-portfolio-sort")
      : "original-order";

    window.addEventListener("load", () => {
      let portfolioIsotope = new Isotope(
        document.querySelector(".portfolio-container"),
        {
          itemSelector: ".portfolio-item",
          layoutMode: portfolioLayout,
          filter: portfolioFilter,
          sortBy: portfolioSort,
        },
      );

      let menuFilters = document.querySelectorAll(
        ".portfolio-isotope .portfolio-flters li",
      );
      menuFilters.forEach(function (el) {
        el.addEventListener(
          "click",
          function () {
            document
              .querySelector(
                ".portfolio-isotope .portfolio-flters .filter-active",
              )
              .classList.remove("filter-active");
            this.classList.add("filter-active");
            portfolioIsotope.arrange({
              filter: this.getAttribute("data-filter"),
            });
            if (typeof aos_init === "function") {
              aos_init();
            }
          },
          false,
        );
      });
    });
  }

  /**
   * Init swiper slider with 1 slide at once in desktop view
   */
  new Swiper(".slides-1", {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
    slidesPerView: "auto",
    pagination: {
      el: ".swiper-pagination",
      type: "bullets",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });

  /**
   * Init swiper slider with 2 slides at once in desktop view
   */
  new Swiper(".slides-2", {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
    slidesPerView: "auto",
    pagination: {
      el: ".swiper-pagination",
      type: "bullets",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    breakpoints: {
      320: {
        slidesPerView: 1,
        spaceBetween: 20,
      },

      1200: {
        slidesPerView: 2,
        spaceBetween: 20,
      },
    },
  });

  /**
   * Initiate pURE cOUNTER
   */
  new PureCounter();

  /**
   * Animation on scroll function and init
   */
  function aos_init() {
    AOS.init({
      duration: 800,
      easing: "slide",
      once: true,
      mirror: false,
    });
  }
  window.addEventListener("load", () => {
    aos_init();
  });
  // --- Sticky header on scroll (with animated reveal) ---
  const headerEl = document.querySelector("#header");
  const STICKY_OFFSET = 100; // пиксели, после которых прилипаем

  if (headerEl) {
    // начальное состояние
    const setAtTopState = () => {
      headerEl.classList.add("at-top");
      headerEl.classList.remove("sticking", "sticked");
    };

    const stickHeader = () => {
      if (headerEl.classList.contains("sticked")) return; // уже прилип
      headerEl.classList.remove("at-top");
      headerEl.classList.add("sticking");
      // force reflow, чтобы анимация translateY сработала корректно
      void headerEl.offsetHeight;
      headerEl.classList.add("sticked");
    };

    const unstickHeader = () => {
      headerEl.classList.remove("sticked", "sticking");
      headerEl.classList.add("at-top");
    };

    // оптимизировано через rAF, чтобы не дёргать layout каждый scroll
    let ticking = false;
    const onScroll = () => {
      const y = window.scrollY || document.documentElement.scrollTop;
      if (!ticking) {
        window.requestAnimationFrame(() => {
          if (y > STICKY_OFFSET) {
            stickHeader();
          } else {
            unstickHeader();
          }
          ticking = false;
        });
        ticking = true;
      }
    };

    // инициализация при загрузке
    setAtTopState();
    onScroll();

    // слушатели
    document.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("load", onScroll);
  }
});
