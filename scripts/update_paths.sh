#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(pwd)}"
DRY_RUN=0
TIMESTAMP=$(date +%s)

usage(){
  cat <<EOF
Usage: $0 [--dry-run] [ROOT_DIR]

Replaces path references in text files:
  dtx/repos/  -> Work/
  dtx/        -> Work/
  my/         -> Projects/

This script targets common text file extensions and skips .git directories.
EOF
}

parse_args(){
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dry-run) DRY_RUN=1; shift ;;
      -h|--help) usage; exit 0 ;;
      *) ROOT_DIR="$1"; shift ;;
    esac
  done
}

parse_args "$@"

echo "Scanning files under: $ROOT_DIR"

while IFS= read -r -d '' file; do
  # create a temporary transformed content
  new=$(sed \
    -e 's|dtx/repos/|Work/|g' \
    -e 's|dtx/|Work/|g' \
    -e 's|\bmy/|Projects/|g' \
    "$file")

  if ! diff -q "$file" <(printf "%s" "$new") >/dev/null 2>&1; then
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[DRY] Would update: $file"
    else
      backup="$file.bak.$TIMESTAMP"
      echo "Updating: $file (backup: $backup)"
      cp "$file" "$backup"
      printf "%s" "$new" > "$file"
    fi
  fi
done < <(find "$ROOT_DIR" -type f \( -name "*.md" -o -name "*.markdown" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" -o -name "*.txt" -o -name "*.py" -o -name "*.js" -o -name "*.cfg" \) ! -path "*/.git/*" -print0)

echo "Done."
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(pwd)}"
DRY_RUN=0
TIMESTAMP=$(date +%s)

usage(){
  cat <<EOF
Usage: $0 [--dry-run] [ROOT_DIR]

Replaces path references in text files:
  dtx/repos/  -> Work/
  dtx/        -> Work/
  my/         -> Projects/

This script targets common text file extensions and skips .git directories.
EOF
}

parse_args(){
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dry-run) DRY_RUN=1; shift ;;
      -h|--help) usage; exit 0 ;;
      *) ROOT_DIR="$1"; shift ;;
    esac
  done
}

parse_args "$@"

echo "Scanning files under: $ROOT_DIR"

while IFS= read -r -d '' file; do
  # create a temporary transformed content
  new=$(sed \
    -e 's|dtx/repos/|Work/|g' \
    -e 's|dtx/|Work/|g' \
    -e 's|\bmy/|Projects/|g' \
    "$file")

  if ! diff -q "$file" <(printf "%s" "$new") >/dev/null 2>&1; then
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[DRY] Would update: $file"
    else
      backup="$file.bak.$TIMESTAMP"
      echo "Updating: $file (backup: $backup)"
      cp "$file" "$backup"
      printf "%s" "$new" > "$file"
    fi
  fi
done < <(find "$ROOT_DIR" -type f \( -name "*.md" -o -name "*.markdown" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" -o -name "*.txt" -o -name "*.py" -o -name "*.js" -o -name "*.cfg" \) ! -path "*/.git/*" -print0)

echo "Done."
