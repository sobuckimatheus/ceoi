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

  /* ---------- Clique em contato → dataLayer (GTM) ----------
     A conversa acontece fora do site (Datalitics/WhatsApp), então o que
     dá para medir aqui é o clique que leva até lá. O evento alimenta a
     conversão do Google Ads.                                          */
  // Um clique no widget do Datalitics chega duas vezes: na div do botão e
  // no <a> que o script dispara em seguida. Esta janela curta garante uma
  // conversão por clique — e também absorve duplo-clique do visitante.
  var ultimoEnvio = 0;

  function registrarContato(tipo, local) {
    var agora = Date.now();
    if (agora - ultimoEnvio < 1200) return;
    ultimoEnvio = agora;

    var h = document.querySelector('.detail-hero h1');
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: 'contato_clique',
      contato_tipo: tipo,
      contato_local: local,
      contato_curso: h ? h.textContent.trim() : '(home)'
    });
  }

  document.addEventListener('click', function (ev) {
    // O botão flutuante do Datalitics é uma <div> com onclick, não um link.
    if (ev.target.closest('.wp-datalitics')) {
      registrarContato('whatsapp', 'botao-flutuante');
      return;
    }

    var link = ev.target.closest('a[href]');
    if (!link) return;

    var href = link.getAttribute('href') || '';
    var tipo = href.indexOf('respondechat') > -1 || href.indexOf('wa.me') > -1 ? 'whatsapp'
             : href.indexOf('tel:') === 0 ? 'telefone'
             : href.indexOf('mailto:') === 0 ? 'email'
             : null;
    if (!tipo) return;

    // De onde partiu o clique, para separar as origens nos relatórios.
    var local = link.closest('.site-header') ? 'cabecalho'
              : link.closest('.hero') ? 'topo'
              : link.closest('.detail-hero') ? 'pagina-curso'
              : link.closest('.contact') ? 'contato'
              : link.closest('.cta-band') ? 'chamada-final'
              : link.closest('.site-footer') ? 'rodape'
              : 'outro';

    registrarContato(tipo, local);
  }, true);

})();
