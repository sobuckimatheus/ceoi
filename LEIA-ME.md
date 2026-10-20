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

13 cursos, conforme a arte oficial de divulgação:

| Formato | Qtd |
|---|---|
| Especialização | 7 |
| Aperfeiçoamento | 4 |
| Mini Residência | 1 |
| Imersão | 1 |

Também: professores com suas credenciais, tópicos de conteúdo programático
e o texto institucional.

## Pontos de atenção

- **Dois cursos foram criados a partir da arte** e ainda não têm conteúdo próprio:
  *Dupla Certificação em Implantodontia e Periodontia* e *Dentística Restauradora*.
  Estão no ar com título, formato e um texto curto, usando a imagem de um curso
  irmão. Falta enviar descrição, módulos, professores e imagem própria.
- **Cursos sem lista de módulos** (Dentística, Endodontia aperfeiçoamento, entre
  outros) estão assim porque o site original também não trazia esse conteúdo.
- **As datas de início** não foram trazidas, porque estavam desatualizadas no site
  original. Vale definir as turmas antes de divulgar.
- **O formulário de contato** abre o WhatsApp com a mensagem pronta, sem precisar
  de servidor. Se preferir envio por e-mail, dá para trocar por Formspree ou similar.
