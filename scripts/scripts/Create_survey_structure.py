from pathlib import Path
import shutil
import argparse
import re

# =====================================
# CONFIG
# =====================================

# BASE_DIR = Path(__file__).resolve().parent
# TEMPLATE_DIR = (BASE_DIR / "Templates").resolve()
# PROJECT_ROOT = (BASE_DIR  ).resolve()

# Dossier racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = (BASE_DIR / "scripts" / "Templates").resolve()
# Les projets créés sont dans le dossier parent
PROJECT_ROOT = BASE_DIR.resolve()

TH2_TEMPLATES = [
    "CAVENAME_P.th2",
    "CAVENAME_C.th2"
]

# =====================================
# ARGUMENTS
# =====================================

parser = argparse.ArgumentParser(
    description="Création d'un projet Therion structuré depuis templates.",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Exemples :

python Create_survey_structure.py essai --empty-th2
"""
)

parser.add_argument("survey")

parser.add_argument("--th", help="Export TopoDroid .th")
parser.add_argument("--th2", help="Export TopoDroid .th2")

args = parser.parse_args()

# =====================================
# NOMS / VARIABLES
# =====================================

SURVEY_ID = args.survey

if not re.fullmatch(r"[A-Za-z0-9_-]+", SURVEY_ID):
    raise ValueError("Nom invalide (A-Z a-z 0-9 _ - uniquement)")

SURVEY_LABEL = SURVEY_ID.replace("_", " ")
SURVEY_BIS = SURVEY_ID.replace("_", "")

# =====================================
# DOSSIERS
# =====================================

project_dir = (PROJECT_ROOT / SURVEY_ID).resolve()
data_dir = project_dir / "datas"
outputs_dir = project_dir / "exports"

data_dir.mkdir(parents=True, exist_ok=True)
outputs_dir.mkdir(parents=True, exist_ok=True)

# =====================================
# TEMPLATES PROJET (hors TH2 dessin)
# =====================================

for file in TEMPLATE_DIR.iterdir():

    if not file.is_file():
        continue

    if file.name in TH2_TEMPLATES:
        continue

    content = file.read_text(encoding="utf-8")

    content = content.replace("<CAVENAME>", SURVEY_ID)
    content = content.replace("<CAVENAME-BIS>", SURVEY_BIS)
    content = content.replace("<CAVENAME-LABEL>", SURVEY_LABEL)

    new_name = file.name.replace("CAVENAME", SURVEY_ID)

    (project_dir / new_name).write_text(content, encoding="utf-8")

# =====================================
# IMPORT TOPODROID
# =====================================

if args.th:
    src = Path(args.th)
    if not src.exists():
        raise FileNotFoundError(src)

    shutil.copy2(src, data_dir / f"{SURVEY_ID}.th")

if args.th2:
    src = Path(args.th2)
    if not src.exists():
        raise FileNotFoundError(src)

    shutil.copy2(src, data_dir / f"{SURVEY_ID}.th2")

# =====================================
# TH2 DEPUIS TEMPLATE
# =====================================

else:

    for template_name in TH2_TEMPLATES:

        template_path = TEMPLATE_DIR / template_name

        content = template_path.read_text(encoding="utf-8")

        content = content.replace("<CAVENAME>", SURVEY_ID)
        content = content.replace("<CAVENAME-BIS>", SURVEY_BIS)
        content = content.replace("<CAVENAME-LABEL>", SURVEY_LABEL)

        output_name = template_name.replace("CAVENAME", SURVEY_ID)

        (data_dir / output_name).write_text(content, encoding="utf-8")

# =====================================
# OUTPUT
# =====================================

print(f"Projet créé : {project_dir}")