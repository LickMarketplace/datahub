"""Commandes locales sans dépendance ni accès réseau."""
import argparse
import csv
import json
import sys
from collections import Counter


def inspect_csv(path, delimiter, encoding):
    with open(path, encoding=encoding, newline="") as stream:
        reader = csv.reader(stream, delimiter=delimiter, strict=True)
        headers = next(reader, None)
        if not headers:
            raise ValueError("Le CSV est vide ou ne contient pas d'en-têtes.")
        normalized = [name.strip() for name in headers]
        duplicates = [name for name, count in Counter(normalized).items() if count > 1]
        blank_headers = [index + 1 for index, name in enumerate(normalized) if not name]
        rows = 0
        malformed_rows = 0
        for row in reader:
            if not row:
                continue
            rows += 1
            if len(row) != len(headers):
                malformed_rows += 1
    result = {
        "columns": headers,
        "row_count": rows,
        "blank_header_positions": blank_headers,
        "duplicate_headers": duplicates,
        "rows_with_wrong_column_count": malformed_rows,
    }
    return result, bool(duplicates or blank_headers or malformed_rows)


def main():
    parser = argparse.ArgumentParser(description="Lick Datahub : contrôles locaux")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="Vérifier le démarrage local")
    inspect = commands.add_parser("inspect-csv", help="Contrôler la structure d'un CSV")
    inspect.add_argument("path")
    inspect.add_argument("--delimiter", default=";")
    inspect.add_argument("--encoding", default="utf-8-sig")
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        parser.exit(1, "Python 3.11 ou supérieur est requis.\n")
    if args.command == "check":
        print(json.dumps({"status": "ok", "storage_connected": False}))
        return 0
    if len(args.delimiter) != 1 or args.delimiter in "\r\n":
        parser.error("--delimiter doit contenir un seul caractère hors retour à la ligne.")
    try:
        result, has_errors = inspect_csv(args.path, args.delimiter, args.encoding)
    except (OSError, UnicodeError, csv.Error, ValueError, LookupError) as error:
        parser.exit(1, f"Lecture impossible : {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(has_errors)


if __name__ == "__main__":
    sys.exit(main())
