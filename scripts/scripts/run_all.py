import subprocess
from pathlib import Path
import argparse
import sys


def find_thconfigs(root: Path):
    patterns = ["thconfig", "*.thconfig"]
    files = set()

    for p in patterns:
        for f in root.rglob(p):
            if f.is_file():
                files.add(f.resolve())

    return sorted(files)


def run_therion(thconfig: Path, verbose=False, dry_run=False) -> bool:
    folder = thconfig.parent

    cmd = f'cd "{folder}" && therion "{thconfig.name}"'

    if verbose:
        print(f"\n[DIR] {folder}")
        print(f"[CMD] {cmd}")

    if dry_run:
        return True

    try:
        subprocess.run(cmd, shell=True, check=True)
        return True

    except subprocess.CalledProcessError as e:
        print(f"[FAIL] {folder} (code {e.returncode})")
        return False

    except FileNotFoundError:
        print("[FATAL] therion introuvable")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-n", "--dry-run", action="store_true")
    parser.add_argument("--stop-on-error", action="store_true")

    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve() if args.path else Path(
        input("Chemin projet: ").strip()
    ).expanduser().resolve()

    if not root.exists():
        print("[FATAL] chemin invalide")
        sys.exit(1)

    thconfigs = find_thconfigs(root)

    print(f"[INFO] {len(thconfigs)} fichiers")

    ok = 0
    fail = 0

    for t in thconfigs:
        success = run_therion(t, args.verbose, args.dry_run)

        if success:
            ok += 1
        else:
            fail += 1
            if args.stop_on_error:
                break

    print(f"\nOK={ok} FAIL={fail}")


if __name__ == "__main__":
    main()