import re
import sys
from pathlib import Path


# ============================================================
# FIND FILES
# ============================================================
def find_files(th_file):
    th_file = Path(th_file).expanduser().resolve()

    if not th_file.is_file():
        print("\n========================================")
        print("ERREUR : FICHIER .th INTROUVABLE")
        print("========================================")
        print(f"\nFichier introuvable :\n  {th_file}\n")
        sys.exit(1)

    if th_file.suffix.lower() != ".th":
        print("\nERREUR : le fichier indiqué n'est pas un fichier .th :")
        print(f"  {th_file}\n")
        sys.exit(1)

    data_dir = th_file.parent

    if data_dir.name == "datas":
        project_dir = data_dir.parent
    else:
        project_dir = data_dir

    cavename = project_dir.name

    xvi_P = data_dir / f"{cavename}_P.xvi"
    xvi_C = data_dir / f"{cavename}_C.xvi"
    th2_P = data_dir / f"{cavename}_P.th2"
    th2_C = data_dir / f"{cavename}_C.th2"
    maps_th = project_dir / f"{cavename}_M.th"

    return cavename, th_file, xvi_P, xvi_C, th2_P, th2_C, maps_th


# ============================================================
# CHECK REQUIRED FILES
# ============================================================
def check_required_files(files):
    missing_files = [
        Path(file)
        for file in files
        if not Path(file).is_file()
    ]

    if missing_files:
        print("\n========================================")
        print("ERREUR : FICHIER(S) MANQUANT(S)")
        print("========================================")

        for file in missing_files:
            print("\nFichier introuvable :")
            print(f"  {file}")

        print("\n========================================")
        print("Create_scrap ne peut pas continuer.")
        print("========================================\n")
        sys.exit(1)


# ============================================================
# PARSE SURVEY NAME
# ============================================================
def parse_survey_name(th_file):
    with Path(th_file).open("r", encoding="utf-8") as f:
        for line in f:
            match = re.match(
                r"\s*survey\s+([A-Za-z0-9_.-]+)",
                line
            )

            if match:
                return match.group(1)

    raise ValueError(
        "\nERREUR : aucune instruction 'survey' trouvée dans :\n"
        f"  {th_file}\n"
    )


# ============================================================
# PARSE XVI - ALPHANUMERIQUE
# ============================================================
def parse_xvi(xvi_path):
    stations = []
    seen = set()

    with Path(xvi_path).open("r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(
        r"set\s+XVIstations\s+\{(.*?)\}\s*set",
        content,
        re.S
    )

    if not match:
        match = re.search(
            r"set\s+XVIstations\s+\{(.*)\}",
            content,
            re.S
        )

    if not match:
        raise ValueError(
            "\nERREUR : impossible de trouver XVIstations dans :\n"
            f"  {xvi_path}\n"
        )

    block = match.group(1)

    pattern = re.compile(
        r"\{\s*"
        r"([-+]?(?:\d+(?:\.\d*)?|\.\d+))\s+"
        r"([-+]?(?:\d+(?:\.\d*)?|\.\d+))\s+"
        r"([^\s{}]+)"
        r"\s*\}"
    )

    for match in pattern.finditer(block):
        x = float(match.group(1))
        y = float(match.group(2))
        name = match.group(3)

        key = (x, y, name)

        if key in seen:
            continue

        seen.add(key)

        stations.append({
            "x": x,
            "y": y,
            "name": name,
        })

    if not stations:
        raise ValueError(
            "\nERREUR : aucune station trouvée dans XVIstations :\n"
            f"  {xvi_path}\n"
        )

    return stations


# ============================================================
# ASK RANGES
# ============================================================
def ask_ranges():
    print()
    print("========================================")
    print("DECOUPAGE DES SCRAPS")
    print("========================================")
    print()
    print("Exemple : 1;12 13;20 21;50")
    print("Exemple alphanumérique : A1;A12 A13;A20")
    print("Entrée vide = toutes les stations dans un seul scrap")
    print()

    plan_ranges = input("Plages pour le PLAN  : ")
    coupe_ranges = input("Plages pour la COUPE : ")

    return plan_ranges.strip(), coupe_ranges.strip()


# ============================================================
# PARSE RANGE TEXT
# ============================================================
def parse_ranges(text):
    text = text.strip()

    if not text:
        return []

    ranges = []

    for item in text.split():
        parts = item.split(";")

        if len(parts) != 2:
            raise ValueError(
                f"\nERREUR : plage invalide '{item}'.\n"
                "Format attendu : DEBUT;FIN\n"
            )

        start = parts[0].strip()
        end = parts[1].strip()

        if not start or not end:
            raise ValueError(
                f"\nERREUR : plage invalide '{item}'.\n"
            )

        ranges.append((start, end))

    return ranges


# ============================================================
# SPLIT STATIONS BY RANGES
# ============================================================
def split_stations_by_ranges(stations, ranges_text):
    if not ranges_text.strip():
        return [stations]

    ranges = parse_ranges(ranges_text)

    names = [station["name"] for station in stations]
    groups = []

    for start, end in ranges:
        if start not in names:
            raise ValueError(
                f"\nERREUR : station de début introuvable : '{start}'\n"
            )

        if end not in names:
            raise ValueError(
                f"\nERREUR : station de fin introuvable : '{end}'\n"
            )

        start_index = names.index(start)

        try:
            relative_end = names[start_index:].index(end)
        except ValueError:
            raise ValueError(
                f"\nERREUR : la station '{end}' ne se trouve pas après "
                f"la station '{start}'.\n"
            )

        end_index = start_index + relative_end
        groups.append(stations[start_index:end_index + 1])

    return groups


# ============================================================
# MAKE SCRAP
# ============================================================
def make_scrap(name, projection, survey, stations):
    lines = []
    seen = set()

    lines.append(
        f'scrap {name} -projection {projection} '
        f'-station-names "" "@{survey}" '
        f'-scale [0 0 78.7402 0 0 0 1 0 m]'
    )

    for station in stations:
        station_name = station["name"]

        if station_name in seen:
            continue

        seen.add(station_name)

        lines.append(
            f"  point {station['x']} {station['y']} "
            f"station -name {station_name}"
        )

    lines.append("endscrap\n")
    return "\n".join(lines)


# ============================================================
# PARSE XVI GRID
# ============================================================
def parse_xvi_grid(xvi_path):
    """
    Lit automatiquement la ligne :

        set XVIgrid {x0 y0 vx vy wx wy nx ny}

    x0, y0 : origine de la grille
    vx, vy : vecteur d'une maille suivant l'axe X
    wx, wy : vecteur d'une maille suivant l'axe Y
    nx, ny : nombre de mailles
    """
    xvi_path = Path(xvi_path)

    content = xvi_path.read_text(encoding="utf-8")

    match = re.search(
        r"set\s+XVIgrid\s+\{([^}]*)\}",
        content,
        re.S
    )

    if not match:
        raise ValueError(
            "\nERREUR : impossible de trouver 'set XVIgrid {...}' dans :\n"
            f"  {xvi_path}\n"
        )

    values = re.findall(
        r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?",
        match.group(1)
    )

    if len(values) < 8:
        raise ValueError(
            "\nERREUR : XVIgrid doit contenir au moins 8 valeurs dans :\n"
            f"  {xvi_path}\n"
        )

    return [float(value) for value in values[:8]]


# ============================================================
# CALCUL POSITION XVI
# ============================================================
def calculate_xvi_insert_position(xvi_path, stations):
    """
    Calage du XVI sur la première station.

    Le centre calculé depuis XVIgrid est un décalage interne au XVI.
    On l'applique à la première station du dessin au lieu de l'utiliser
    comme une coordonnée absolue.

    Pour l'axe Y, le repère XVI est inversé par rapport au canevas
    XTherion. Le décalage vertical est donc appliqué dans le sens opposé.
    """
    if not stations:
        raise ValueError(
            "\nERREUR : aucune station disponible pour positionner le XVI.\n"
        )

    x0, y0, vx, vy, wx, wy, nx, ny = parse_xvi_grid(xvi_path)

    offset_x = x0 + ((vx * nx) + (wx * ny)) / 2
    offset_y = y0 + ((vy * nx) + (wy * ny)) / 2

    reference = stations[0]

    image_x = reference["x"] + offset_x

    # Correction du repère vertical XVI / XTherion.
    # La demi-maille verticale permet de retrouver le calage utilisé
    # par XTherion lors de l'insertion du fond XVI.
    vertical_half_step = abs(wy) / 2 if wy != 0 else abs(vy) / 2
    image_y = reference["y"] - offset_y - vertical_half_step

    return image_x, image_y


# ============================================================
# CALCUL EMPRISE XTHERION
# ============================================================
def calculate_area_adjust(stations, margin=800.0):
    """
    Calcule l'emprise de travail XTherion à partir des stations,
    avec une marge de 800 unités autour.
    """
    if not stations:
        raise ValueError(
            "\nERREUR : impossible de calculer l'emprise sans stations.\n"
        )

    min_x = min(station["x"] for station in stations)
    max_x = max(station["x"] for station in stations)
    min_y = min(station["y"] for station in stations)
    max_y = max(station["y"] for station in stations)

    return (
        min_x - margin,
        min_y - margin,
        max_x + margin,
        max_y + margin,
    )


# ============================================================
# FORMAT NUMBER
# ============================================================
def format_number(value):
    """
    Formate les nombres sans ajouter de zéros inutiles.
    """
    if abs(value) < 1e-12:
        value = 0.0

    result = f"{value:.12f}".rstrip("0").rstrip(".")

    if "." not in result:
        result += ".0"

    return result


# ============================================================
# UPDATE TH2 HEADER
# ============================================================
def update_th2_header(th2_file, xvi_file, stations):
    """
    Génère automatiquement :

        encoding utf-8
        xth_me_area_adjust ...
        xth_me_area_zoom_to 100
        xth_me_image_insert ...

    La position de l'image est calculée à partir du centre
    de la grille XVI.
    """
    th2_file = Path(th2_file)
    xvi_file = Path(xvi_file)

    image_x, image_y = calculate_xvi_insert_position(xvi_file, stations)

    min_x, min_y, max_x, max_y = calculate_area_adjust(stations)

    header = (
        "encoding  utf-8\n"
        f"##XTHERION## xth_me_area_adjust "
        f"{format_number(min_x)} "
        f"{format_number(min_y)} "
        f"{format_number(max_x)} "
        f"{format_number(max_y)}\n"
        "##XTHERION## xth_me_area_zoom_to 50\n"
        f"##XTHERION## xth_me_image_insert "
        f"{{{format_number(image_x)} 1 1.0}} "
        f"{{{format_number(image_y)} 0}} "
        f"{xvi_file.name} 0 {{}}\n"
    )

    content = th2_file.read_text(encoding="utf-8")

    cleaned_lines = []

    for line in content.splitlines():
        stripped = line.strip()

        if re.match(r"^encoding\s+", stripped, re.I):
            continue

        if stripped.startswith("##XTHERION## xth_me_area_adjust"):
            continue

        if stripped.startswith("##XTHERION## xth_me_area_zoom_to"):
            continue

        if stripped.startswith("##XTHERION## xth_me_image_insert"):
            continue

        cleaned_lines.append(line)

    cleaned_content = "\n".join(cleaned_lines).lstrip("\n")

    if cleaned_content:
        final_content = header + "\n\n" + cleaned_content
    else:
        final_content = header + "\n"

    th2_file.write_text(
        final_content,
        encoding="utf-8"
    )


# ============================================================
# APPEND TH2
# ============================================================
def append(file, content):
    with Path(file).open("a", encoding="utf-8") as f:
        f.write("\n" + content + "\n")


# ============================================================
# UPDATE MAPS
# ============================================================
def update_maps(maps_file, plan_scraps, coupe_scraps):
    maps_file = Path(maps_file)

    with maps_file.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    out = []
    inserted_plan = False
    inserted_coupe = False

    for line in lines:
        out.append(line)

        if "map MP" in line and not inserted_plan:
            for scrap in plan_scraps:
                out.append(f"  {scrap}\n")
            inserted_plan = True

        if "map MC" in line and not inserted_coupe:
            for scrap in coupe_scraps:
                out.append(f"  {scrap}\n")
            inserted_coupe = True

    if not inserted_plan:
        raise ValueError(
            f"\nERREUR : 'map MP' introuvable dans :\n  {maps_file}\n"
        )

    if not inserted_coupe:
        raise ValueError(
            f"\nERREUR : 'map MC' introuvable dans :\n  {maps_file}\n"
        )

    with maps_file.open("w", encoding="utf-8") as f:
        f.writelines(out)


# ============================================================
# MAIN
# ============================================================
def main():
    if len(sys.argv) != 2:
        print("\nUtilisation :")
        print(
            "  python scripts/Create_scrap.py "
            "banon-brieux/datas/banon-brieux.th"
        )
        print()
        sys.exit(1)

    # LES QUESTIONS SONT POSEES IMMEDIATEMENT
    plan_ranges, coupe_ranges = ask_ranges()

    (
        cavename,
        th_file,
        xvi_P,
        xvi_C,
        th2_P,
        th2_C,
        maps_th,
    ) = find_files(sys.argv[1])

    print()
    print(f"[INFO] Projet détecté : {cavename}")
    print(f"[INFO] Fichier .th : {th_file}")

    check_required_files([
        th_file,
        xvi_P,
        xvi_C,
        th2_P,
        th2_C,
        maps_th,
    ])

    survey = parse_survey_name(th_file)
    print(f"[INFO] Survey détecté : {survey}")

    print("[INFO] Lecture des fichiers XVI...")

    stations_plan = parse_xvi(xvi_P)
    stations_coupe = parse_xvi(xvi_C)

    print(f"[INFO] {len(stations_plan)} stations trouvées en plan")
    print(f"[INFO] {len(stations_coupe)} stations trouvées en coupe")

    plan_groups = split_stations_by_ranges(
        stations_plan,
        plan_ranges
    )

    coupe_groups = split_stations_by_ranges(
        stations_coupe,
        coupe_ranges
    )

    plan_scraps = []
    coupe_scraps = []
    plan_out = []
    coupe_out = []

    for i, group in enumerate(plan_groups, start=1):
        name = f"{cavename}_SP{i}"
        plan_scraps.append(name)
        plan_out.append(make_scrap(name, "plan", survey, group))

    for i, group in enumerate(coupe_groups, start=1):
        name = f"{cavename}_SC{i}"
        coupe_scraps.append(name)
        coupe_out.append(make_scrap(name, "extended", survey, group))

    print()
    print(f"[INFO] {len(plan_scraps)} scraps plan générés")
    print(f"[INFO] {len(coupe_scraps)} scraps coupe générés")

    update_th2_header(
        th2_P,
        xvi_P,
        stations_plan
    )

    update_th2_header(
        th2_C,
        xvi_C,
        stations_coupe
    )

    append(th2_P, "\n".join(plan_out))
    append(th2_C, "\n".join(coupe_out))

    update_maps(
        maps_th,
        plan_scraps,
        coupe_scraps
    )

    # ========================================================
    # RESUME
    # ========================================================
    print()
    print("========================================")
    print("RÉSUMÉ DES SCRAPS GÉNÉRÉS")
    print("========================================")
    print()

    print(f"PLAN : {len(plan_scraps)} scrap(s)")

    for i, group in enumerate(plan_groups, start=1):
        print(
            f"  {cavename}_SP{i} : "
            f"{len(group)} station(s)"
        )

    print()

    print(f"COUPE : {len(coupe_scraps)} scrap(s)")

    for i, group in enumerate(coupe_groups, start=1):
        print(
            f"  {cavename}_SC{i} : "
            f"{len(group)} station(s)"
        )

    print()

    print(
        f"Total PLAN  : "
        f"{sum(len(group) for group in plan_groups)} station(s)"
    )

    print(
        f"Total COUPE : "
        f"{sum(len(group) for group in coupe_groups)} station(s)"
    )

    print("========================================")
    print()


# ============================================================
# START
# ============================================================
if __name__ == "__main__":
    main()
