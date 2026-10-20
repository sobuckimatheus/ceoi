#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador do site CEOI Premium.
Lê site/cursos_data.json e gera index.html + uma página por curso em site/cursos/.
Uso:  python3 build.py
"""
import json, os, re, html, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
OUT_COURSES = os.path.join(SITE, "cursos")

WHATSAPP = "5548999157432"
TEL_FIXO = "+554830255999"
TEL_FIXO_FMT = "(48) 3025-5999"
TEL_CEL_FMT = "(48) 99915-7432"
EMAIL = "contato@ceoipremium.com.br"
ENDERECO = "Av. Mauro Ramos, 825, Centro<br>Florianópolis, SC, 88020-302"
MAPS = "https://www.google.com/maps/search/?api=1&query=Av.+Mauro+Ramos,+825,+Centro,+Florian%C3%B3polis+-+SC,+88020-302"
INSTA = "https://www.instagram.com/escolaceoipremium"
FACE = "https://www.facebook.com/escolaceoi"

TYPE_ORDER = ["Especialização", "Mini Residência", "Aperfeiçoamento", "Imersão"]
TYPE_BLURB = {
    "Especialização": "Pós-graduação lato sensu, com titulação reconhecida e formação clínica completa.",
    "Mini Residência": "Formação intensiva e prática, concentrada nos procedimentos de maior demanda.",
    "Aperfeiçoamento": "Atualização técnica focada, para incorporar um novo procedimento à rotina clínica.",
    "Imersão": "Curso curto e hands-on, dedicado a uma única técnica do início ao fim.",
}

def e(s):
    return html.escape(s or "", quote=True)

ICO = {
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18"/></svg>',
 "user": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-6.5 8-6.5s8 2.5 8 6.5"/></svg>',
 "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/></svg>',
 "wa": '<svg viewBox="0 0 24 24"><path d="M17.5 14.4c-.3-.2-1.8-.9-2-1-.3-.1-.5-.2-.7.1s-.8 1-.9 1.2c-.2.2-.3.2-.6.1a8 8 0 0 1-2.4-1.5 9 9 0 0 1-1.6-2c-.2-.3 0-.5.1-.6l.5-.6.3-.5v-.5l-1-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4a3.2 3.2 0 0 0-1 2.4A5.6 5.6 0 0 0 7.3 13a12.7 12.7 0 0 0 4.9 4.3c.7.3 1.2.5 1.6.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.3.2-1.4l-.3-.2zM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.3a8.3 8.3 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.3 8.3 0 1 1 12 20.3z"/></svg>',
 "ig": '<svg viewBox="0 0 24 24"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9a3.8 3.8 0 0 1-.9-1.4c-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 1.8c-3.1 0-3.5 0-4.7.1-1.1.1-1.7.2-2.1.4-.5.2-.9.4-1.2.8-.4.3-.6.7-.8 1.2-.2.4-.3 1-.4 2.1C2.7 8.8 2.7 9.2 2.7 12s0 3.2.1 4.4c.1 1.1.2 1.7.4 2.1.2.5.4.9.8 1.2.3.4.7.6 1.2.8.4.2 1 .3 2.1.4 1.2.1 1.6.1 4.7.1s3.5 0 4.7-.1c1.1-.1 1.7-.2 2.1-.4.5-.2.9-.4 1.2-.8.4-.3.6-.7.8-1.2.2-.4.3-1 .4-2.1.1-1.2.1-1.6.1-4.4s0-3.2-.1-4.4c-.1-1.1-.2-1.7-.4-2.1a3 3 0 0 0-.8-1.2 3 3 0 0 0-1.2-.8c-.4-.2-1-.3-2.1-.4-1.2-.1-1.6-.1-4.7-.1zm0 3.1a4.9 4.9 0 1 1 0 9.8 4.9 4.9 0 0 1 0-9.8zm0 8.1a3.2 3.2 0 1 0 0-6.4 3.2 3.2 0 0 0 0 6.4zm6.3-8.3a1.15 1.15 0 1 1-2.3 0 1.15 1.15 0 0 1 2.3 0z"/></svg>',
 "fb": '<svg viewBox="0 0 24 24"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.5 2.9h-2.3v7A10 10 0 0 0 22 12z"/></svg>',
}

ORBIT = """<svg class="orbit" viewBox="0 0 400 400" role="img" aria-label="Marca CEOI Premium: a Ilha de Santa Catarina em órbita">
<defs><linearGradient id="goldGrad" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="#E3C76A"/><stop offset="50%" stop-color="#C9A227"/><stop offset="100%" stop-color="#9C7B14"/>
</linearGradient></defs>
<g class="ring r1"><ellipse cx="200" cy="200" rx="168" ry="62"/></g>
<g class="ring r2"><ellipse cx="200" cy="200" rx="168" ry="62" transform="rotate(60 200 200)"/></g>
<g class="ring r3"><ellipse cx="200" cy="200" rx="168" ry="62" transform="rotate(120 200 200)"/></g>
<g class="dot d1"><circle class="dot" cx="368" cy="200" r="5.5"/></g>
<g class="dot d2"><circle class="dot" cx="32" cy="200" r="4.5"/></g>
<path class="isle" d="M201 96c4 0 7 3 8 7 2 7 0 14 2 21 2 6 7 10 9 16 3 9-1 18-1 27 0 8 3 16 3 24 0 7-2 14-1 21 1 9 5 17 4 26-1 11-6 21-13 29-4 5-10 10-17 9-6-1-10-7-11-13-2-10 2-20 3-30 1-12-2-24-4-36-2-9-4-18-3-27 1-11 7-21 9-32 2-9 1-19 3-28 1-6 3-12 9-14z"/>
<path class="isle" d="M186 150c3-1 5 2 5 5 0 6-2 12-4 18-2 5-5 10-8 9-3-1-3-6-2-11 2-8 5-19 9-21z" opacity=".55"/>
</svg>"""

def head(title, desc, depth=0, extra=""):
    p = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta name="theme-color" content="#0F2748">
<link rel="icon" href="{p}images/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/style.css">
{extra}
</head>
<body>"""

def header(depth=0):
    p = "../" * depth
    return f"""
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{p}index.html" aria-label="CEOI Premium, página inicial">
      <img src="{p}images/logo.webp" alt="" width="42" height="42">
      <span class="brand-txt"><b>CEOI Premium</b><span>Florianópolis · SC</span></span>
    </a>
    <button class="nav-toggle" aria-label="Abrir menu" aria-expanded="false" aria-controls="nav">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <nav class="nav" id="nav">
      <a href="{p}index.html#cursos">Cursos</a>
      <a href="{p}index.html#instituto">O Instituto</a>
      <a href="{p}index.html#contato">Contato</a>
      <a class="btn btn--navy header-cta" href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">Fale conosco</a>
    </nav>
  </div>
</header>"""

def footer(depth=0):
    p = "../" * depth
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="{p}images/logo.webp" alt="CEOI Premium" width="40" height="40">
        <span>Centro de Ensino Odontológico da Ilha<br>Florianópolis, Santa Catarina</span>
      </div>
      <div class="socials">
        <a href="{INSTA}" target="_blank" rel="noopener" aria-label="Instagram">{ICO['ig']}</a>
        <a href="{FACE}" target="_blank" rel="noopener" aria-label="Facebook">{ICO['fb']}</a>
        <a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener" aria-label="WhatsApp">{ICO['wa']}</a>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 CEOI Premium. Todos os direitos reservados.</span>
      <span>{TEL_FIXO_FMT} · {EMAIL}</span>
    </div>
  </div>
</footer>
<a class="wa-float" href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener" aria-label="Conversar no WhatsApp">{ICO['wa']}</a>
<script src="{p}assets/app.js" defer></script>
</body>
</html>"""

def card(c, depth=0):
    p = "../" * depth
    cls = "tag--esp" if c["tipo"] == "Especialização" else ""
    meta = []
    if c["duracao"]:
        meta.append(f'<span>{ICO["clock"]}{e(c["duracao"])}</span>')
    if c["dias"]:
        d = c["dias"]
        d = d[:30] + "…" if len(d) > 31 else d
        meta.append(f'<span>{ICO["cal"]}{e(d)}</span>')
    if not meta and c["publico"]:
        meta.append(f'<span>{ICO["user"]}{e(c["publico"])}</span>')
    desc = c["objetivo"] or f'Curso de {c["tipo"].lower()} em {c["titulo"]}, ministrado por professores de referência no mercado odontológico.'
    return f"""      <article class="card reveal" data-tipo="{e(c["tipo"])}">
        <div class="card-media">
          <span class="tag {cls}">{e(c["tipo"])}</span>
          <img src="{p}{c['img_local']}" alt="{e(c['titulo'])}" loading="lazy" width="800" height="1000">
        </div>
        <div class="card-body">
          <h3>{e(c["titulo"])}</h3>
          <div class="card-meta">{''.join(meta)}</div>
          <p class="card-desc">{e(desc)}</p>
          <a class="card-link" href="{p}cursos/{c['slug']}.html">Ver o curso {ICO['arrow']}</a>
        </div>
      </article>"""


# ------------------------------------------------------------------ HOME
def build_index(courses):
    n_esp = sum(1 for c in courses if c["tipo"] == "Especialização")
    n_prof = len({t["nome"] for c in courses for t in c["professores"]})

    counts = {t: sum(1 for c in courses if c["tipo"] == t) for t in TYPE_ORDER}
    chips = ['<button class="chip" data-filter="todos" aria-pressed="true">Todos <i>%d</i></button>' % len(courses)]
    for t in TYPE_ORDER:
        if counts.get(t):
            chips.append(f'<button class="chip" data-filter="{e(t)}" aria-pressed="false">{e(t)} <i>{counts[t]}</i></button>')

    cards = []
    for t in TYPE_ORDER:
        for c in courses:
            if c["tipo"] == t:
                cards.append(card(c, 0))

    opts = "".join(f'<option value="{e(c["titulo"])}">{e(c["titulo"])}</option>' for c in courses)

    ld = {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "name": "CEOI Premium | Centro de Ensino Odontológico da Ilha",
        "url": "https://ceoipremium.com.br/",
        "telephone": TEL_FIXO,
        "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": "Av. Mauro Ramos, 825",
                    "addressLocality": "Florianópolis", "addressRegion": "SC",
                    "postalCode": "88020-302", "addressCountry": "BR"},
        "sameAs": [INSTA, FACE],
    }
    extra = '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False)

    body = f"""
<main>
  <section class="hero">
    <div class="wrap">
      <div class="hero-grid">
        <div>
          <p class="eyebrow eyebrow--lt">Florianópolis · Santa Catarina · Desde 2015</p>
          <h1>Odontologia<br>que se aprende<br><em>na prática.</em></h1>
          <p class="hero-lead">Especializações, aperfeiçoamentos e imersões para cirurgiões-dentistas,
          conduzidos por professores que são referência no mercado, em uma estrutura
          pensada para a clínica real.</p>
          <div class="hero-cta">
            <a class="btn btn--gold" href="#cursos">Conhecer os cursos</a>
            <a class="btn btn--ghost" href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">Falar com a secretaria</a>
          </div>
        </div>
        <div class="orbit-wrap">{ORBIT}</div>
      </div>
      <div class="hero-stats">
        <div class="stat reveal"><b>{len(courses)}</b><span>Cursos<br>em cartaz</span></div>
        <div class="stat reveal"><b>{n_esp}</b><span>Especializações<br>lato sensu</span></div>
        <div class="stat reveal"><b>{n_prof}+</b><span>Professores<br>e coordenadores</span></div>
        <div class="stat reveal"><b>2015</b><span>Ano de<br>fundação</span></div>
      </div>
    </div>
  </section>

  <section class="courses" id="cursos">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">Programação</p>
        <h2>Encontre o curso certo para o seu momento</h2>
        <p>Da pós-graduação completa à imersão de um fim de semana. Filtre pelo formato
        que cabe na sua agenda.</p>
      </div>
      <div class="filters" role="group" aria-label="Filtrar cursos por formato">
        {''.join(chips)}
      </div>
      <div class="grid" id="grid">
{chr(10).join(cards)}
        <p class="empty" id="empty" hidden>Nenhum curso neste formato no momento.</p>
      </div>
    </div>
  </section>

  <section class="about" id="instituto">
    <div class="wrap">
      <div class="about-grid">
        <div class="about-copy">
          <p class="eyebrow">O Instituto</p>
          <h2 style="font-size:clamp(2.1rem,5vw,3.2rem);margin-bottom:1.4rem">De seis alunos a uma
          escola de referência na Ilha</h2>
          <p>Em fevereiro de <strong>2015</strong> o CEOI foi inaugurado com apenas seis alunos
          na Especialização em Implantodontia. Ao final daquele mesmo ano, o número já era
          dez vezes maior.</p>
          <p>O instituto construiu sua identidade na relação próxima com as universidades locais
          e na valorização do cirurgião-dentista. Assim se tornou <strong>a escola que mais cresceu</strong>
          entre as instituições do grupo Harmonique.</p>
          <p>Da necessidade de ampliar a estrutura nasceu o <strong>Premium</strong>: um espaço que
          reúne conforto, modernidade e tecnologia para sustentar a próxima etapa.</p>
        </div>
        <div class="timeline">
          <div class="tl-item reveal">
            <span class="tl-year">2015</span>
            <div><h4>A inauguração</h4><p>O CEOI abre as portas com seis alunos na Especialização
            em Implantodontia.</p></div>
          </div>
          <div class="tl-item reveal">
            <span class="tl-year">2016</span>
            <div><h4>Crescimento exponencial</h4><p>O número de alunos se multiplica por dez e novas
            áreas entram na grade.</p></div>
          </div>
          <div class="tl-item reveal">
            <span class="tl-year">2020</span>
            <div><h4>Referência regional</h4><p>A escola que mais cresce entre as instituições do
            grupo Harmonique.</p></div>
          </div>
          <div class="tl-item reveal">
            <span class="tl-year">Hoje</span>
            <div><h4>O Premium</h4><p>Nova estrutura, {len(courses)} cursos em cartaz e professores
            de referência nacional.</p></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="contact" id="contato">
    <div class="wrap">
      <div class="contact-grid">
        <div>
          <p class="eyebrow eyebrow--lt">Contato</p>
          <h2>Vamos conversar sobre a sua formação</h2>
          <p class="contact-lead">A secretaria responde de segunda a sexta e pode te orientar sobre
          turmas, módulos e condições de matrícula.</p>
          <ul class="c-list">
            <li><span class="c-ico">{ICO['pin']}</span><div><b>Endereço</b>
              <a href="{MAPS}" target="_blank" rel="noopener">{ENDERECO}</a></div></li>
            <li><span class="c-ico">{ICO['phone']}</span><div><b>Telefone</b>
              <a href="tel:{TEL_FIXO}">{TEL_FIXO_FMT}</a></div></li>
            <li><span class="c-ico">{ICO['wa']}</span><div><b>WhatsApp</b>
              <a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">{TEL_CEL_FMT}</a></div></li>
            <li><span class="c-ico">{ICO['mail']}</span><div><b>E-mail</b>
              <a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
          </ul>
        </div>
        <form class="form" id="lead-form" novalidate>
          <h3>Tenho interesse</h3>
          <p>Conte qual curso te interessa e a secretaria entra em contato.</p>
          <div class="field"><label for="f-nome">Nome completo</label>
            <input id="f-nome" name="nome" type="text" required placeholder="Seu nome"></div>
          <div class="field"><label for="f-email">E-mail</label>
            <input id="f-email" name="email" type="email" required placeholder="voce@email.com"></div>
          <div class="field"><label for="f-tel">Telefone / WhatsApp</label>
            <input id="f-tel" name="telefone" type="tel" required placeholder="(48) 99999-9999"></div>
          <div class="field"><label for="f-curso">Curso de interesse</label>
            <select id="f-curso" name="curso">
              <option value="">Selecione um curso</option>{opts}
              <option value="Outro">Outro / ainda não sei</option>
            </select></div>
          <div class="field"><label for="f-msg">Mensagem (opcional)</label>
            <textarea id="f-msg" name="mensagem" placeholder="Alguma dúvida específica?"></textarea></div>
          <button class="btn btn--gold" type="submit">Enviar pelo WhatsApp</button>
          <p class="form-note">Ao enviar, abrimos o WhatsApp com a sua mensagem pronta.</p>
        </form>
      </div>
    </div>
  </section>
</main>"""

    desc = ("CEOI Premium | Centro de Ensino Odontológico da Ilha. Especializações, "
            "aperfeiçoamentos e imersões para cirurgiões-dentistas em Florianópolis/SC.")
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(head("CEOI Premium | Cursos de Odontologia em Florianópolis", desc, 0, extra)
                + header(0) + body + footer(0))


# ------------------------------------------------------------ COURSE PAGE
def build_course(c, courses):
    facts = []
    if c["duracao"]:
        facts.append(("Duração", c["duracao"]))
    if c["dias"]:
        facts.append(("Dias de aula", c["dias"]))
    if c["publico"]:
        facts.append(("Público", c["publico"]))
    if c["tipo"] == "Especialização":
        facts.append(("Titulação", "Pós-graduação lato sensu"))
    facts_html = "".join(
        f'<div class="fact"><b>{e(k)}</b><p>{e(v)}</p></div>' for k, v in facts)

    lead = c["objetivo"] or TYPE_BLURB.get(c["tipo"], "")

    mods = ""
    if c["modulos"]:
        items = "".join(f"<li>{e(m)}</li>" for m in c["modulos"])
        mods = f"""
  <section class="panel panel--alt">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">Conteúdo programático</p>
        <h2>O que você vai estudar</h2>
        <p>{len(c['modulos'])} tópicos distribuídos ao longo do curso.</p>
      </div>
      <ul class="mod-list">{items}</ul>
    </div>
  </section>"""

    profs = ""
    if c["professores"]:
        blocks = []
        for t in c["professores"]:
            creds = "".join(f"<li>{e(x)}</li>" for x in t["creds"])
            role = f'<p class="role">{e(t["cargo"])}</p>' if t["cargo"] else ""
            blocks.append(f'<article class="prof reveal"><h3>{e(t["nome"])}</h3>{role}'
                          f'<ul>{creds}</ul></article>')
        profs = f"""
  <section class="panel">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">Corpo docente</p>
        <h2>Quem ensina</h2>
        <p>Professores atuantes, com titulação e prática clínica reconhecidas.</p>
      </div>
      <div class="prof-grid">{''.join(blocks)}</div>
    </div>
  </section>"""

    rel = [x for x in courses if x["tipo"] == c["tipo"] and x["slug"] != c["slug"]][:3]
    if len(rel) < 3:
        rel += [x for x in courses if x["slug"] != c["slug"]
                and x not in rel][:3 - len(rel)]
    related = f"""
  <section class="related">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">Veja também</p>
        <h2>Outros cursos</h2>
      </div>
      <div class="grid">{''.join(card(x, 1) for x in rel)}</div>
    </div>
  </section>"""

    ld = {"@context": "https://schema.org", "@type": "Course", "name": c["titulo"],
          "description": lead[:300],
          "provider": {"@type": "EducationalOrganization", "name": "CEOI Premium",
                       "url": "https://ceoipremium.com.br/"}}
    extra = '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False)

    msg = f"Olá! Tenho interesse no curso de {c['tipo']} em {c['titulo']}."
    import urllib.parse
    wa = f"https://wa.me/{WHATSAPP}?text={urllib.parse.quote(msg)}"

    body = f"""
<main>
  <section class="detail-hero">
    <div class="wrap">
      <nav class="crumb" aria-label="Você está aqui">
        <a href="../index.html">Início</a><span>/</span>
        <a href="../index.html#cursos">Cursos</a><span>/</span>
        <span style="opacity:1;color:var(--gold-lt)">{e(c['titulo'])}</span>
      </nav>
      <div class="detail-grid">
        <div>
          <p class="eyebrow eyebrow--lt">{e(c['tipo'])}</p>
          <h1>{e(c['titulo'])}</h1>
          <p class="detail-lead">{e(lead)}</p>
          <div class="detail-facts">{facts_html}</div>
          <div class="hero-cta">
            <a class="btn btn--gold" href="{wa}" target="_blank" rel="noopener">Tenho interesse</a>
            <a class="btn btn--ghost" href="../index.html#contato">Pedir mais informações</a>
          </div>
        </div>
        <div class="detail-poster">
          <img src="../{c['img_local']}" alt="{e(c['titulo'])} | CEOI Premium" width="800" height="1000">
        </div>
      </div>
    </div>
  </section>
{mods}{profs}
  <section class="cta-band">
    <div class="wrap">
      <h2>Quer garantir sua vaga?</h2>
      <p>Fale com a secretaria para conhecer as turmas abertas e as condições de matrícula.</p>
      <div class="hero-cta">
        <a class="btn btn--gold" href="{wa}" target="_blank" rel="noopener">Falar no WhatsApp</a>
        <a class="btn btn--ghost" href="tel:{TEL_FIXO}">{TEL_FIXO_FMT}</a>
      </div>
    </div>
  </section>
{related}
</main>"""

    title = f"{c['titulo']} | {c['tipo']} | CEOI Premium"
    desc = (lead or c["titulo"])[:160]
    with open(os.path.join(OUT_COURSES, c["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(head(title, desc, 1, extra) + header(1) + body + footer(1))


def main():
    os.makedirs(OUT_COURSES, exist_ok=True)
    with open(os.path.join(SITE, "cursos_data.json"), encoding="utf-8") as f:
        courses = json.load(f)
    build_index(courses)
    for c in courses:
        build_course(c, courses)
    print(f"✓ index.html + {len(courses)} páginas de curso geradas em site/")


if __name__ == "__main__":
    main()
