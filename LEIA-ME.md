# CEOI Premium — site novo

Site estático, profissional e responsivo, construído a partir do conteúdo real de
`ceoipremium.com.br/cursos/` (textos, módulos, professores e imagens originais).

## Como visualizar

```bash
cd site
python3 -m http.server 8000
# abra http://localhost:8000
```

Como é 100% estático, pode ser publicado em qualquer lugar — Netlify, Vercel,
GitHub Pages, Hostinger, ou a própria hospedagem atual. Basta subir a pasta `site/`.

## Estrutura

```
site/
  index.html            página inicial (hero, 19 cursos com filtro, instituto, contato)
  cursos/*.html         19 páginas de curso, uma por curso
  assets/style.css      estilos
  assets/app.js         filtro, menu mobile, animações, formulário
  images/               20 imagens baixadas do site original
  cursos_data.json      todo o conteúdo extraído, em JSON
build.py                gera index.html + as páginas de curso a partir do JSON
```

## Para alterar conteúdo

Edite `site/cursos_data.json` e rode:

```bash
python3 build.py
```

Cada curso tem: `titulo`, `tipo`, `objetivo`, `duracao`, `dias`, `publico`,
`modulos[]`, `professores[]` (com `nome`, `cargo`, `creds[]`) e a imagem.

Dados de contato (WhatsApp, telefone, e-mail, endereço) ficam no topo de `build.py`.

## O que foi extraído

19 cursos, divididos em 4 formatos:

| Formato | Qtd |
|---|---|
| Especialização | 6 |
| Aperfeiçoamento | 5 |
| Imersão | 7 |
| Mini Residência | 1 |

Também: 45 professores com 260 credenciais, 134 tópicos de conteúdo programático,
e o texto institucional.

## Pontos de atenção

- **Três cursos estão sem conteúdo no site original** e por isso aparecem aqui
  apenas com título, formato e imagem: *Dentística com Ênfase em HOF*,
  *Endodontia (aperfeiçoamento)* e *Desenho do Sorriso — Facetas de Resina e Cerâmica*.
  As páginas originais estão vazias — é preciso enviar esses textos para completá-las.
- **As datas de início** ("Março de 2024" etc.) não foram trazidas, porque estão
  desatualizadas no site original. Vale definir as turmas de 2026 antes de publicar.
- **O formulário de contato** abre o WhatsApp com a mensagem pronta — não precisa de
  servidor. Se preferir envio por e-mail, dá para trocar por Formspree ou similar.
- Alguns cursos não têm lista de módulos porque o site original também não tem.
