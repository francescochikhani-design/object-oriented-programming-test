#!/usr/bin/env bash
set -euo pipefail

dry_run=false
uninstall=false
quiet=false
verbose=false

for option in "$@"; do
    case "$option" in
        --dry-run) dry_run=true ;;
        --uninstall) uninstall=true ;;
        --quiet) quiet=true ;;
        --verbose) verbose=true ;;
        --help)
            printf '%s\n' 'Usage: bash env_install.sh [--dry-run] [--uninstall] [--quiet] [--verbose]'
            exit 0 ;;
        *) printf 'Unknown option: %s\n' "$option" >&2; exit 2 ;;
    esac
done

environment="$HOME/.local/share/oop-jupyter"
log_file="$HOME/env_install.log"

notice() {
    if ! "$quiet"; then
        if [[ -t 1 ]]; then printf '\n\033[32m%s\033[0m\n\n' "$1"
        else printf '\n%s\n\n' "$1"; fi
    fi
}

run() {
    local command status
    printf -v command '%q ' "$@"
    if "$dry_run"; then
        printf 'Would run: %s\n' "$command"
        return
    fi
    if "$verbose" && ! "$quiet"; then printf 'Running: %s\n' "$command"; fi
    if "$quiet"; then
        "$@" >> "$log_file" 2>&1 && status=0 || status=$?
    else
        "$@" && status=0 || status=$?
    fi
    printf '%s exit=%s %s\n' "$(date '+%F %T')" "$status" "$command" >> "$log_file"
    if (( status != 0 )); then
        printf 'Command failed (%s): %s\n' "$status" "$command" >&2
    fi
    return "$status"
}

ensure_python() {
    case "$(uname -s)" in
        Darwin)
            command -v brew >/dev/null || {
                printf 'Install Homebrew from https://brew.sh/ first.\n' >&2
                return 1
            }
            if ! command -v python3 >/dev/null; then run brew install python; fi
            run brew doctor || printf 'Homebrew reported warnings.\n' >&2
            ;;
        Linux)
            command -v apt-get >/dev/null || {
                printf 'This script supports apt-based Linux distributions.\n' >&2
                return 1
            }
            if ! command -v python3 >/dev/null ||
                ! python3 -m pip --version >/dev/null 2>&1 ||
                ! python3 -c 'import ensurepip' 2>/dev/null; then
                run sudo apt-get update
                run sudo apt-get install -y python3 python3-pip python3-venv
            fi
            ;;
        *) printf 'Use macOS or apt-based Linux (including WSL).\n' >&2; return 1 ;;
    esac
}

main() {
    if "$uninstall"; then
        if [[ -x "$environment/bin/python" ]]; then
            run "$environment/bin/python" -m pip uninstall -y notebook
        else
            notice 'No exercise environment found.'
        fi
        return
    fi
    ensure_python
    if ! "$dry_run"; then run python3 --version; fi
    if [[ ! -x "$environment/bin/python" ]]; then
        run python3 -m venv "$environment"
    fi
    run "$environment/bin/python" -m pip --version
    if [[ ! -x "$environment/bin/jupyter-notebook" ]]; then
        run "$environment/bin/python" -m pip install notebook
    fi
    notice "Launch with: \"$environment/bin/jupyter\" notebook"
}

main
