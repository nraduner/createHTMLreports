import base64
from pathlib import Path

def build_html_report(title: str, sections: list[dict], out_path: Path) -> None:
    """
    Build a self-contained HTML report with a fixed navigation pane.

    The report embeds all images as base64, so the output is a single portable
    .html file with no external dependencies.

    Parameters
    ----------
    title : str
        Page heading shown in the browser tab and as the <h1> title.
    sections : list of dicts, each with keys:
        title       : str
            Section heading (<h2>).
        note        : str, optional
            Short italicised blurb shown below the section heading.
        subsections : dict of {str: list of (str, Path)}
            Keys are subsection headings (<h3>).
            Values are lists of (figure_title, image_path) tuples.
            Use an empty string for figure_title to skip the <h4> heading
            and nav entry (useful when the subsection heading is enough).
    out_path : Path
        Destination for the .html file; parent directories are created
        automatically if they don't exist.
    """
    nav:  list[str] = []   # navigation pane links
    body: list[str] = []   # main content blocks

    def slug(text: str) -> str:
        """Convert a heading string to a URL-safe id."""
        return text.lower().replace(" ", "-").replace("/", "-")

    def add_note(note: str | None):
        """Append an italicised note paragraph if note is non-empty."""
        if note:
            body.append(f"<p class='note'>{note}</p>")

    # ── build nav + body from the sections data structure ────────────────────
    for s_i, sec in enumerate(sections):
        sec_id = f"sec-{s_i}-{slug(sec['title'])}"
        nav.append(f"<a class='sect' href='#{sec_id}'>{sec['title']}</a>")
        body.append(f"<h2 id='{sec_id}'>{sec['title']}</h2>")
        add_note(sec.get("note"))

        for ss_title, figures in sec.get("subsections", {}).items():
            ss_id = f"ss-{s_i}-{slug(ss_title)}"
            nav.append(f"<a class='ses' href='#{ss_id}'>{ss_title}</a>")
            body.append(f"<h3 id='{ss_id}'>{ss_title}</h3>")

            for fig_title, fig_path in figures:
                p = Path(fig_path)

                # only add a figure-level heading and nav entry when a title is given
                fig_id = (f"fig-{s_i}-{slug(ss_title)}-{slug(fig_title)}"
                          if fig_title else f"fig-{s_i}-{slug(ss_title)}")
                if fig_title:
                    nav.append(f"<a class='sub' href='#{fig_id}'>{fig_title}</a>")
                    body.append(f"<h4 id='{fig_id}'>{fig_title}</h4>")

                # embed image as base64, or show a warning if the file is missing
                if p.exists():
                    b64 = base64.b64encode(p.read_bytes()).decode()
                    body.append(f"<img src='data:image/png;base64,{b64}' alt='{fig_title}'>")
                else:
                    body.append(f"<p class='missing'>⚠ Image not found: {p}</p>")
                    print(f"WARNING – missing: {p}")

    # ── styling ───────────────────────────────────────────────────────────────
    css = """
    body { font-family: sans-serif; margin: 0 }

    /* fixed left navigation pane */
    nav  { position: fixed; top: 0; left: 0; bottom: 0; width: 210px;
           overflow-y: auto; background: #f4f4f4; padding: 14px 10px;
           box-sizing: border-box; border-right: 1px solid #ddd }
    nav a { display: block; text-decoration: none; color: #222;
            padding: 3px 6px; border-radius: 4px }

    /* three indent levels: section → subsection → figure */
    nav a.sect   { font-weight: bold; margin-top: 12px;
                   border-bottom: 1px solid #ccc; border-radius: 0 }
    nav a.ses    { padding-left: 14px }
    nav a.sub    { padding-left: 28px; font-size: 0.9em; color: #555 }

    /* highlight the nav entry that matches the current scroll position */
    nav a.active { background: #dbe7ff }

    main { margin-left: 220px; padding: 16px 24px 75vh 24px; max-width: 1500px }
    img  { max-width: 100% }
    p.note    { color: #444; font-style: italic }
    p.missing { color: #c00; font-style: italic }
    h2, h3, h4 { scroll-margin-top: 12px }
    h2 { border-bottom: 2px solid #ccc; padding-bottom: 4px; margin-top: 40px }
    h3 { border-bottom: 1px solid #eee; padding-bottom: 2px; margin-top: 28px }
    """

    # ── scroll-spy: highlights the nav link matching the visible heading ──────
    js = """
    const links   = Array.from(document.querySelectorAll('nav a'));
    const targets = links.map(a => document.getElementById(a.getAttribute('href').slice(1)));
    const update  = () => {
      let cur = 0;
      // find the last heading that has scrolled past the top of the viewport
      targets.forEach((t, i) => { if (t && t.getBoundingClientRect().top <= 40) cur = i; });
      // snap to the last entry when the page is fully scrolled down
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2)
        cur = targets.length - 1;
      links.forEach((l, i) => l.classList.toggle('active', i === cur));
    };
    window.addEventListener('scroll', update);
    update();   // run once on load to highlight the correct entry
    """

    # ── assemble and write the HTML file ─────────────────────────────────────
    html = "\n".join([
        "<!DOCTYPE html>",
        "<html><head>",
        "  <meta charset='utf-8'>",
        f"  <title>{title}</title>",
        f"  <style>{css}</style>",
        "</head><body>",
        f"  <nav>{''.join(nav)}</nav>",
        f"  <main><h1>{title}</h1>{''.join(body)}</main>",
        f"  <script>{js}</script>",
        "</body></html>",
    ])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"Report written: {out_path}")