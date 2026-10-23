from pathlib import Path


def clean_empty_therion_objects(file_path):
    """
    Supprime les blocs vides :
        line ... endline
        area ... endarea

    lorsqu'ils se suivent directement.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned = []

    i = 0
    removed_lines = 0
    removed_areas = 0

    while i < len(lines):

        current = lines[i].strip()
        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""

        # line vide
        if current.startswith("line") and next_line == "endline":
            removed_lines += 1
            i += 2
            continue

        # area vide
        if current.startswith("area") and next_line == "endarea":
            removed_areas += 1
            i += 2
            continue

        cleaned.append(lines[i])
        i += 1

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(cleaned)

    return removed_lines, removed_areas


def process_directory(root_folder):

    root = Path(root_folder)

    total_lines = 0
    total_areas = 0
    total_files = 0

    for th2_file in root.rglob("*.th2"):

        try:
            removed_lines, removed_areas = clean_empty_therion_objects(th2_file)

            if removed_lines > 0 or removed_areas > 0:
                print(
                    f"{th2_file} -> "
                    f"{removed_lines} line(s) supprimée(s), "
                    f"{removed_areas} area(s) supprimée(s)"
                )

            total_lines += removed_lines
            total_areas += removed_areas
            total_files += 1

        except Exception as e:
            print(f"Erreur sur {th2_file} : {e}")

    print("\n===== RÉSUMÉ =====")
    print(f"Fichiers traités : {total_files}")
    print(f"Lines supprimées : {total_lines}")
    print(f"Areas supprimées : {total_areas}")


if __name__ == "__main__":

    dossier = r"C:\Users\burru\Documents\Spéléo\Topographie"  # Modifier ici
    

    process_directory(dossier)