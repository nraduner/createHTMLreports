# HTML Report Builder

A lightweight Python utility for generating self-contained HTML (quality control) reports from neuroimaging figures. The output is a single `.html` file with all images embedded as base64 — no external dependencies, easy to share.

## Features

- Fixed navigation pane with scroll-spy highlighting
- Three levels of hierarchy: sections → subsections → figures
- Optional notes per section
- Missing images are flagged with a warning but won't crash the script
- Single portable `.html` output file

## Usage

```python
from pathlib import Path
from build_qc_report import build_qc_report

sub      = "sub-12142a"
figDir   = Path(f"/path/to/{sub}/figures")

skullstrip = {
    "title": "Skull-stripping",
    "note":  "red = original mask, yellow = no-CSF mask, cyan = infant mask",
    "subsections": {
        "3m": [("T1w + mask", figDir / "skull_stripping" / "03m_t1mask.png")],
        "1y": [("T1w + mask", figDir / "skull_stripping" / "01y_t1mask.png"),
               ("T2w + mask", figDir / "skull_stripping" / "01y_t2mask.png"),
               ("T1w + T2w",  figDir / "skull_stripping" / "01y_t1t2.png")],
    },
}

coreg = {
    "title": "Longitudinal Co-Registration",
    "note":  "",
    "subsections": {
        "Coregistration of T1w": [("", figDir / "coregistration" / "T1w_combined_rows.png")],
        "Coregistration of T2w": [("", figDir / "coregistration" / "T2w_combined_rows.png")],
    },
}

build_qc_report(
    title    = f"QC report: {sub}",
    sections = [skullstrip, coreg],
    out_path = figDir / "qc_report.html",
)
```

## Input structure

`build_qc_report` takes three arguments:

| Argument | Type | Description |
|----------|------|-------------|
| `title` | `str` | Page heading and browser tab title |
| `sections` | `list[dict]` | List of section dictionaries (see below) |
| `out_path` | `Path` | Where to write the `.html` file |

Each section dictionary has the following keys:

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `title` | `str` | yes | Section heading |
| `note` | `str` | no | Short blurb shown below the heading |
| `subsections` | `dict` | yes | `{subsection_title: [(fig_title, fig_path), ...]}` |

For each `(fig_title, fig_path)` tuple, leave `fig_title` as an empty string `""` to skip the figure-level heading and show only the image.

## Requirements

Python 3.10+ (uses `str | None` union syntax). No third-party packages — only the standard library.

## License

MIT
