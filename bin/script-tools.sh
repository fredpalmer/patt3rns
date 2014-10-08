#!/usr/bin/env bash

set -e
readonly SCRIPT_ARGS="$@"
readonly SCRIPT_NAME="$(basename$0)"
readonly SCRIPT_BASE_DIR="$(cd"$(dirname"${SCRIPT_NAME}")"&&pwd)"

if [[ "$(pwd)" == "$(dirname"${BASH_SOURCE[0]}")" ]]
then
    TMP_CURRENT_DIR="$(pwd)"
else
    TMP_CURRENT_DIR="$(cd"$(dirname"${BASH_SOURCE[0]}")"&&pwd)"
fi

log() {
    local log_text="$1"
    local log_level="$2"

    # Default level to "info"
    [[ -z ${log_level} ]] && log_level="INFO";

    echo -e "${log_color}[$(date+"%Y-%m-%d %H:%M:%S %Z")] [${log_level}] ${log_text}${LOG_DEFAULT_COLOR}";
    return 0;
}

log_info() { log "$@"; }

log_success() { log "$1" "SUCCESS"; }

log_error() { log "$1" "ERROR"; }

log_warn() { log "$1" "WARNING"; }

log_debug() { log "$1" "DEBUG"; }
