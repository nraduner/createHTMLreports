from pathlib import Path
from build_html_report import build_html_report

# ── subject & directory setup ─────────────────────────────────────────────────
sub      = "sub-1000"
basePath = Path(f"/Path/to/subDir/{sub}")
figDir   = basePath / "figures"
ssDir    = figDir / "skull_stripping"
coregDir = figDir / "coregistration"

# ── skull-stripping section ───────────────────────────────────────────────────
# subsections are keyed by session label; each entry is a list of
# (figure title, image path) tuples — only include sessions that exist
skullstrip = {"title": "Skull-stripping",
              "note":  "red = original mask, yellow = no-CSF mask, cyan = infant mask",
              "subsections": {"3m": [("T1w + mask", ssDir / "03m_t1mask.png")],
                              "1y": [("T1w + mask", ssDir / "01y_t1mask.png"),
                                     ("T2w + mask", ssDir / "01y_t2mask.png"),
                                     ("T1w + T2w",  ssDir / "01y_t1t2.png")],},
}

# ── co-registration section ───────────────────────────────────────────────────
# one subsection per modality; figure title left empty ("") when the
# subsection heading is already descriptive enough
coreg = {"title": "Longitudinal Co-Registration",
         "note":  "",
         "subsections": {"Coregistration of T1w": [("", coregDir / "T1w_combined_rows.png")],
                         "Coregistration of T2w": [("", coregDir / "T2w_combined_rows.png")],},
}

# ── build report ──────────────────────────────────────────────────────────────
# sections are rendered in the order they appear in the list;
# missing images are flagged with a warning but won't crash the script
build_html_report(title    = f"QC report: {sub}",
                sections = [skullstrip, coreg],
                out_path = figDir / "qc_report.html")