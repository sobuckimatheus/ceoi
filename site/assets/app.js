/* CEOI Premium — interações do site */
(function () {
  'use strict';

  /* ---------- Menu mobile ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.getAttribute('data-open') === 'true';
      nav.setAttribute('data-open', String(!open));
      toggle.setAttribute('aria-expanded', String(!open));
      toggle.setAttribute('aria-label', open ? 'Abrir menu' : 'Fechar menu');
    });

    nav.addEventListener('click', function (ev) {
      if (ev.target.closest('a')) {
        nav.setAttribute('data-open', 'false');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', 'Abrir menu');
      }
    });

    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && nav.getAttribute('data-open') === 'true') {
        nav.setAttribute('data-open', 'false');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  /* ---------- Filtro de cursos ---------- */
  var chips = document.querySelectorAll('.chip');
  var grid = document.getElementById('grid');
  var empty = document.getElementById('empty');

  if (chips.length && grid) {
    var cards = Array.prototype.slice.call(grid.querySelectorAll('.card'));

    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        var filter = chip.dataset.filter;

        chips.forEach(function (c) {
          c.setAttribute('aria-pressed', String(c === chip));
        });

        var shown = 0;
        cards.forEach(function (card) {
          var type = card.dataset.tipo || '';
          var match = filter === 'todos' || type === filter;
          card.hidden = !match;
          // Um card filtrado pode nunca ter entrado na viewport, e ficaria
          // invisível (opacity:0) ao ser mostrado. Revela na hora.
          if (match) { card.classList.add('in'); shown++; }
        });

        if (empty) empty.hidden = shown !== 0;
      });
    });
  }

  /* ---------- Revelar ao rolar ---------- */
  var targets = document.querySelectorAll('.reveal');

  if (!('IntersectionObserver' in window) ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    targets.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry, i) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        setTimeout(function () { el.classList.add('in'); }, Math.min(i * 70, 350));
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    targets.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Formulário → WhatsApp ---------- */
  var form = document.getElementById('lead-form');

  if (form) {
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();

      if (!form.reportValidity()) return;

      var data = new FormData(form);
      var val = function (k) { return (data.get(k) || '').toString().trim(); };

      var lines = [
        'Olá! Gostaria de mais informações.',
        '',
        'Nome: ' + val('nome'),
        'E-mail: ' + val('email'),
        'Telefone: ' + val('telefone')
      ];

      var curso = val('curso');
      if (curso) lines.push('Curso de interesse: ' + curso);

      var msg = val('mensagem');
      if (msg) lines.push('', 'Mensagem: ' + msg);

      var url = 'https://wa.me/5548999157432?text=' +
                encodeURIComponent(lines.join('\n'));
      window.open(url, '_blank', 'noopener');
    });
  }
})();
