#!/usr/bin/env bash
# refresh-project-links.sh — Rebuild .github discovery link farms for a target repo.
# Idempotent. Prunes stale links before rebuilding. Override files take precedence.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLKIT_HOME="${TOOLKIT_HOME:-${SCRIPT_DIR}}"

MODE="symlink"
DRY_RUN=0
PRUNE_ONLY=0
TARGET=""

while [ $# -gt 0 ]; do
  case "$1" in
    --copy)        MODE="copy"; shift ;;
    --symlink)     MODE="symlink"; shift ;;
    --dry-run)     DRY_RUN=1; shift ;;
    --prune-only)  PRUNE_ONLY=1; shift ;;
    *)             TARGET="$1"; shift ;;
  esac
done

TARGET="${TARGET:-$(pwd)}"
TARGET="$(cd "${TARGET}" && pwd)"

if [ ! -d "${TARGET}/.github" ]; then
  echo "ERROR: ${TARGET}/.github not found. Run link-to-project.sh first."
  exit 1
fi

python3 - "${TOOLKIT_HOME}" "${TARGET}" "${MODE}" "${DRY_RUN}" "${PRUNE_ONLY}" <<'PY'
import json, os, sys, pathlib, datetime, shutil

toolkit_home, target, mode, dry_run_s, prune_only_s = sys.argv[1:6]
dry_run = dry_run_s == "1"
prune_only = prune_only_s == "1"
toolkit = pathlib.Path(toolkit_home)
repo = pathlib.Path(target)

# (active_subdir, override_subdir, source_subdir, kind)
domains = [
    (".github/agents",       ".github/agents-overrides",       "agents",   "agent"),
    (".github/skills",       ".github/skills-overrides",       "skills",   "skill"),
    (".github/prompts",      ".github/prompts-overrides",      "prompts",  "prompt"),
    (".github/instructions", ".github/instructions-overrides", "instructions", "instruction"),
]

# Compat mirror for agents.
agents_compat = repo / ".github" / "AGENTS"

assets = []
pruned = []

def remove_link(p: pathlib.Path):
    if p.is_symlink() or p.is_file():
        p.unlink()
    elif p.is_dir():
        shutil.rmtree(p)

def install_link(source: pathlib.Path, dest: pathlib.Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() or dest.is_symlink():
        remove_link(dest)
    if mode == "symlink":
        try:
            os.symlink(source, dest)
            return "symlink"
        except OSError:
            pass
    # copy fallback
    if source.is_dir():
        shutil.copytree(source, dest)
    else:
        shutil.copy2(source, dest)
    return "copy"

# Prune stale links in each active path.
for active_rel, override_rel, src_rel, kind in domains:
    active = repo / active_rel
    if not active.exists():
        continue
    for entry in active.iterdir():
        # If it's a symlink whose target no longer exists, prune.
        if entry.is_symlink():
            try:
                target_path = entry.resolve(strict=True)
            except FileNotFoundError:
                pruned.append({"path": str(entry.relative_to(repo)), "reason": "broken"})
                if not dry_run:
                    entry.unlink()
                continue
        # If the source no longer has this asset, prune.
        name = entry.name
        override_source = repo / override_rel / name
        global_source = toolkit / src_rel / name
        if not override_source.exists() and not global_source.exists():
            pruned.append({"path": str(entry.relative_to(repo)), "reason": "no source"})
            if not dry_run:
                remove_link(entry)

# Prune agents compat folder.
if agents_compat.exists():
    for entry in agents_compat.iterdir():
        active_target = repo / ".github" / "agents" / entry.name
        if not active_target.exists():
            pruned.append({"path": str(entry.relative_to(repo)), "reason": "compat orphan"})
            if not dry_run:
                remove_link(entry)

if prune_only:
    # Write manifest with prune info only.
    manifest = {
        "toolkit_home": str(toolkit),
        "project_root": str(repo),
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "mode": "prune-only",
        "pruned": pruned,
        "assets": []
    }
    out = repo / ".ai-sdlc" / "link-manifest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    if not dry_run:
        out.write_text(json.dumps(manifest, indent=2))
    print(f"prune-only: removed {len(pruned)} entries")
    sys.exit(0)

# Rebuild link farms.
for active_rel, override_rel, src_rel, kind in domains:
    active = repo / active_rel
    override_dir = repo / override_rel
    global_dir = toolkit / src_rel
    active.mkdir(parents=True, exist_ok=True)
    override_dir.mkdir(parents=True, exist_ok=True)

    # Collect names from override + global. Override wins on name collision.
    names = {}
    if global_dir.is_dir():
        for entry in global_dir.iterdir():
            if entry.name.startswith('.'):
                continue
            names[entry.name] = ("default", entry)
    if override_dir.is_dir():
        for entry in override_dir.iterdir():
            if entry.name in ('.gitkeep',) or entry.name.startswith('.'):
                continue
            names[entry.name] = ("override", entry)

    for name, (kind_src, source) in names.items():
        dest = active / name
        if dry_run:
            print(f"would link {dest} -> {source} ({kind_src})")
        else:
            actual_mode = install_link(source, dest)
            assets.append({
                "type": kind,
                "name": name,
                "active_path": str(dest.relative_to(repo)),
                "source_path": str(source),
                "source_kind": kind_src,
                "mode": actual_mode,
            })

# Agents compat mirror — only on case-sensitive filesystems where .github/AGENTS
# and .github/agents are distinct directories. macOS APFS / HFS+ default to
# case-insensitive, where the two collide and the mirror would overwrite the
# active links with self-references.
def is_case_sensitive(parent: pathlib.Path) -> bool:
    parent.mkdir(parents=True, exist_ok=True)
    probe_lower = parent / "._tk_case_probe"
    probe_upper = parent / "._TK_CASE_PROBE"
    try:
        probe_lower.write_text("lower")
        # On case-insensitive FS, writing the uppercase variant overwrites the lowercase one.
        probe_upper.write_text("upper")
        result = probe_lower.read_text() == "lower"
    finally:
        for p in (probe_lower, probe_upper):
            try:
                p.unlink()
            except FileNotFoundError:
                pass
    return result

github_dir = repo / ".github"
if is_case_sensitive(github_dir):
    agents_compat.mkdir(parents=True, exist_ok=True)
    agents_active = repo / ".github" / "agents"
    if agents_active.is_dir():
        for entry in agents_active.iterdir():
            dest = agents_compat / entry.name
            if dry_run:
                print(f"would mirror {dest} -> {entry}")
                continue
            install_link(entry, dest)
else:
    print("note: skipping .github/AGENTS compat mirror (case-insensitive filesystem)")

# Write link-manifest.json.
manifest = {
    "toolkit_home": str(toolkit),
    "project_root": str(repo),
    "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    "mode": mode,
    "pruned": pruned,
    "assets": assets,
}
out = repo / ".ai-sdlc" / "link-manifest.json"
out.parent.mkdir(parents=True, exist_ok=True)
if not dry_run:
    out.write_text(json.dumps(manifest, indent=2))
print(f"refresh: {len(assets)} assets, {len(pruned)} pruned, mode={mode}")
PY
