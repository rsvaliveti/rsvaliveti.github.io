"""Import a BibTeX file into Zola publication bundles.

For each BibTeX entry a content bundle is created:

    <output>/<slug>/index.md   # TOML front matter (title, date, [extra] ...)
    <output>/<slug>/cite.bib   # the single entry, for the "BibTeX" section

Only ``title`` and ``date`` are written as top-level front matter keys; every
other field lives under ``[extra]`` so Zola never has to deal with unknown keys.

Adapted from the Wowchemy/academic-cli importer, trimmed to remove the
``academic`` package dependency and the template-file requirement.

Usage:
    python scripts/import_bibtex.py data/papers.bib content/publications --overwrite
"""

import argparse
import calendar
import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import bibtexparser
import toml
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import convert_to_unicode

# Map BibTeX entry types to universal CSL types used by the templates.
PUB_TYPES_BIBTEX_TO_CSL = {
    "article": "article-journal",
    "book": "book",
    "conference": "paper-conference",
    "inbook": "chapter",
    "incollection": "chapter",
    "inproceedings": "paper-conference",
    "manual": "book",
    "mastersthesis": "thesis",
    "patent": "patent",
    "phdthesis": "thesis",
    "proceedings": "book",
    "report": "report",
    "thesis": "thesis",
    "techreport": "report",
    "unpublished": "manuscript",
    "misc": "manuscript",
}

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)
log = logging.getLogger("import_bibtex")


def import_bibtex(
    bibtex, pub_dir, featured=False, overwrite=False, normalize=False, dry_run=False
):
    """Import all publications from a BibTeX file."""
    if not Path(bibtex).is_file():
        log.error("BibTeX file not found: %s", bibtex)
        raise SystemExit(1)

    with open(bibtex, "r", encoding="utf-8") as bibtex_file:
        parser = BibTexParser(common_strings=True)
        parser.customization = convert_to_unicode
        parser.ignore_nonstandard_types = False
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

    count = 0
    for entry in bib_database.entries:
        if parse_bibtex_entry(
            entry,
            pub_dir=pub_dir,
            featured=featured,
            overwrite=overwrite,
            normalize=normalize,
            dry_run=dry_run,
        ):
            count += 1
    log.info(
        "Imported %d/%d entries into %s", count, len(bib_database.entries), pub_dir
    )


def parse_bibtex_entry(
    entry, pub_dir, featured=False, overwrite=False, normalize=False, dry_run=False
):
    """Create a single publication bundle from a BibTeX entry."""
    log.info("Parsing entry %s", entry.get("ID", "<no-id>"))

    bundle_path = os.path.join(pub_dir, slugify(entry["ID"]))
    markdown_path = os.path.join(bundle_path, "index.md")

    if not overwrite and os.path.isdir(bundle_path):
        log.warning("Skipping %s (already exists; use --overwrite)", bundle_path)
        return False

    if not dry_run:
        Path(bundle_path).mkdir(parents=True, exist_ok=True)

    # Render the single-entry citation and embed it directly in the front matter.
    # (No separate cite.bib asset: the embedded copy is the single source and
    # keeps the template free of any runtime file reads.)
    db = BibDatabase()
    db.entries = [entry]
    bibtex_str = BibTexWriter().write(db).strip()

    extra = {"featured": featured, "bibtex": bibtex_str}
    attr = {"title": clean_bibtex_str(entry["title"])}

    if "subtitle" in entry:
        extra["subtitle"] = clean_bibtex_str(entry["subtitle"])

    year, month, day = "", "01", "01"
    if "date" in entry:
        parts = entry["date"].split("-")
        year = parts[0] if len(parts) >= 1 else ""
        month = parts[1] if len(parts) >= 2 else month
        day = parts[2] if len(parts) >= 3 else day
    if "month" in entry and month == "01":
        month = month2number(entry["month"])
    if "year" in entry and not year:
        year = entry["year"]
    if not year:
        log.error(
            "Invalid/missing date for entry %s; defaulting year to 1900", entry["ID"]
        )
        year = "1900"

    attr["date"] = f"{year}-{month}-{day}"
    extra["year"] = year
    extra["month"] = month
    extra["day"] = day
    extra["publish_date"] = datetime.now(timezone.utc).isoformat()

    authors = entry.get("author") or entry.get("editor")
    if authors:
        extra["authors"] = clean_bibtex_authors(
            [a.strip() for a in authors.replace("\n", " ").split(" and ")]
        )

    extra["publication_types"] = PUB_TYPES_BIBTEX_TO_CSL.get(
        entry["ENTRYTYPE"], "manuscript"
    )
    extra["abstract"] = (
        clean_bibtex_str(entry["abstract"]) if "abstract" in entry else ""
    )

    if "booktitle" in entry:
        extra["publication"] = clean_bibtex_str(entry["booktitle"])
    elif "journal" in entry:
        extra["publication"] = clean_bibtex_str(entry["journal"])
    elif "journaltitle" in entry:
        extra["publication"] = clean_bibtex_str(entry["journaltitle"])
    elif "publisher" in entry:
        extra["publication"] = clean_bibtex_str(entry["publisher"])
    else:
        extra["publication"] = ""

    if "keywords" in entry:
        extra["tags"] = clean_bibtex_tags(entry["keywords"], normalize)

    if "doi" in entry:
        extra["doi"] = clean_bibtex_str(entry["doi"])

    links = []
    if (
        all(f in entry for f in ["archiveprefix", "eprint"])
        and entry["archiveprefix"].lower() == "arxiv"
    ):
        links.append(
            {
                "name": "arXiv",
                "url": "https://arxiv.org/abs/" + clean_bibtex_str(entry["eprint"]),
            }
        )
    if "url" in entry:
        url = clean_bibtex_str(entry["url"])
        if url[-4:].lower() == ".pdf":
            extra["url_pdf"] = url
        else:
            links.append({"name": "URL", "url": url})
    if links:
        extra["links"] = links

    attr["extra"] = extra

    if not dry_run:
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write("+++\n")
            toml.dump(attr, f)
            f.write("+++\n")
    return True


def slugify(s, lower=True):
    for r in (".", "_", ":"):
        s = s.replace(r, "-")
    s = re.sub(r"(\D+)(\d+)", r"\1\-\2", s)
    s = re.sub(r"(\d+)(\D+)", r"\1\-\2", s)
    s = re.sub(r"((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))", r"\-\1", s)
    s = "".join(c for c in s if c.isalnum() or c == "-").strip()
    s = re.sub("-{2,}", "-", s)
    return s.lower() if lower else s


def clean_bibtex_authors(author_str):
    """Convert author names to `firstname(s) lastname` format."""
    authors = []
    for s in author_str:
        s = s.strip()
        if not s:
            continue
        if "," in s:
            split_names = s.split(",", 1)
            last_name = split_names[0].strip()
            first_names = [i.strip() for i in split_names[1].split()]
        else:
            split_names = s.split()
            last_name = split_names.pop()
            first_names = [i.replace(".", ". ").strip() for i in split_names]
        if last_name.lower() in ("jnr", "jr", "junior"):
            last_name = first_names.pop()
        for item in list(first_names):
            if item in ("ben", "van", "der", "de", "la", "le"):
                last_name = first_names.pop() + " " + last_name
        authors.append((" ".join(first_names) + " " + last_name).strip())
    return authors


def clean_bibtex_str(s):
    """Clean a BibTeX string and escape TOML-hostile characters."""
    s = s.replace("\\", "")
    s = s.replace('"', '\\"')
    s = s.replace("{", "").replace("}", "")
    s = s.replace("\t", " ").replace("\n", " ").replace("\r", "")
    return s.strip()


def clean_bibtex_tags(s, normalize=False):
    tags = [tag.strip() for tag in clean_bibtex_str(s).split(",") if tag.strip()]
    if normalize:
        tags = [tag.lower().capitalize() for tag in tags]
    return tags


def month2number(month):
    """Convert a BibTeX/BibLaTeX month (numeric or textual) to a 2-digit string."""
    if len(month) <= 2:
        return month.zfill(2)
    month_abbr = month.strip()[:3].title()
    try:
        return str(list(calendar.month_abbr).index(month_abbr)).zfill(2)
    except ValueError:
        log.error("Unrecognized month '%s'; defaulting to 01", month)
        return "01"


def main():
    parser = argparse.ArgumentParser(
        prog="import_bibtex", description="Import a BibTeX file into Zola bundles"
    )
    parser.add_argument("input", help="Path to the BibTeX file")
    parser.add_argument(
        "output", help="Output content directory (e.g. content/publications)"
    )
    parser.add_argument(
        "--featured", action="store_true", help="Flag publications as featured"
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing bundles"
    )
    parser.add_argument(
        "--normalize", action="store_true", help="Normalize keyword casing"
    )
    parser.add_argument(
        "-dr", "--dry-run", action="store_true", help="Do not write any files"
    )
    args = parser.parse_args()
    import_bibtex(
        args.input,
        pub_dir=args.output,
        featured=args.featured,
        overwrite=args.overwrite,
        normalize=args.normalize,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
