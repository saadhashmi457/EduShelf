document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("navbar-toggle");
    const menu = document.getElementById("navbar-menu");

    toggleBtn.addEventListener("click", () => {
       menu.classList.toggle("hidden");
      if (menu.classList.contains("hidden")) {
        menu.classList.remove("hidden");
        menu.classList.add("flex");
      } else {
        menu.classList.add("hidden");
        menu.classList.remove("flex");
      }
    });
  });





// Add shadow on scroll only on navbar
const navbar = document.getElementById('main-navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
  const currentScroll = window.scrollY;

  if (currentScroll > 60) {
    navbar.classList.add('sticky', 'shadow-lg');
  } else {
    navbar.classList.remove('sticky', 'shadow-lg');
  }

  lastScroll = currentScroll;
});

// Animate sections with classy effect
const sections = document.querySelectorAll('.animate-section');
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      // Delay each section slightly for stagger effect
      setTimeout(() => {
        entry.target.classList.add('visible');
      }, i * 150);
    } else {
      // Reset if you want replay effect
      entry.target.classList.remove('visible');
    }
  });
}, { threshold: 0.2 });

sections.forEach(section => observer.observe(section));

// Scroll to top button
const scrollBtn = document.getElementById("scrollToTopBtn");
if (scrollBtn) {
  window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
      scrollBtn.classList.remove("hidden");
    } else {
      scrollBtn.classList.add("hidden");
    }
  });

  function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
  window.scrollToTop = scrollToTop; // make accessible in HTML onclick
}

// Filtering books
const buttons = document.querySelectorAll(".filter-btn");
const books = document.querySelectorAll(".book-card");

buttons.forEach((btn) => {
  btn.addEventListener("click", () => {
    const filter = btn.getAttribute("data-filter");
    books.forEach((book) => {
      if (filter === "all" || book.classList.contains(filter)) {
        book.classList.remove("hidden");
      } else {
        book.classList.add("hidden");
      }
    });
  });
});

// Lucide icons
if (window.lucide) {
  lucide.createIcons();
}

// Submit effect
function submitEffect(e) {
  e.preventDefault();
  document.getElementById('success-msg').classList.remove("hidden");
  setTimeout(() => {
    document.getElementById('success-msg').classList.add("hidden");
  }, 5000);
  e.target.reset();
}
window.submitEffect = submitEffect;

// Expandable sections
document.querySelectorAll('section[role="button"]').forEach(section => {
  section.addEventListener('click', () => {
    const isCollapsed = section.getAttribute('data-collapsed') === 'true';
    document.querySelectorAll('section[role="button"]').forEach(s => {
      s.setAttribute('data-collapsed', 'true');
      s.setAttribute('aria-expanded', 'false');
      const icon = s.querySelector('svg');
      if (icon) icon.classList.remove('rotate-180');
    });
    if (isCollapsed) {
      section.setAttribute('data-collapsed', 'false');
      section.setAttribute('aria-expanded', 'true');
      const icon = section.querySelector('svg');
      if (icon) icon.classList.add('rotate-180');
    }
  });

  section.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      section.click();
    }
  });
});


