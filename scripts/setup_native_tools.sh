#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCAL_DIR="$ROOT/.local-tools/ffmpeg"
LOCAL_FFMPEG="$LOCAL_DIR/ffmpeg"
TMP_DIR="${TMPDIR:-/tmp}/quickops-ffmpeg"
FFMPEG_URL="https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"

has_cmd() {
  command -v "$1" >/dev/null 2>&1
}

install_with_sudo_if_possible() {
  if ! has_cmd sudo || ! has_cmd apt-get; then
    return 1
  fi

  if ! sudo -n true >/dev/null 2>&1; then
    echo "sudo is available but needs an interactive password; skipping system install."
    return 1
  fi

  echo "Installing native media tools with sudo apt-get..."
  sudo -n apt-get update
  sudo -n apt-get install -y ffmpeg
}

install_static_ffmpeg() {
  if [ -x "$LOCAL_FFMPEG" ]; then
    echo "Local ffmpeg already ready: $LOCAL_FFMPEG"
    return 0
  fi

  if ! has_cmd curl; then
    echo "curl is required to download static ffmpeg." >&2
    return 1
  fi

  echo "Installing static ffmpeg locally..."
  mkdir -p "$LOCAL_DIR" "$TMP_DIR"
  curl -L "$FFMPEG_URL" -o "$TMP_DIR/ffmpeg-release-amd64-static.tar.xz"
  tar -xf "$TMP_DIR/ffmpeg-release-amd64-static.tar.xz" -C "$TMP_DIR"
  found="$(find "$TMP_DIR" -maxdepth 2 -type f -name ffmpeg | sort | tail -n 1)"
  probe="$(find "$TMP_DIR" -maxdepth 2 -type f -name ffprobe | sort | tail -n 1)"
  if [ -z "$found" ] || [ -z "$probe" ]; then
    echo "Downloaded archive did not contain ffmpeg and ffprobe." >&2
    return 1
  fi
  cp "$found" "$LOCAL_DIR/ffmpeg"
  cp "$probe" "$LOCAL_DIR/ffprobe"
  chmod +x "$LOCAL_DIR/ffmpeg" "$LOCAL_DIR/ffprobe"
}

main() {
  if has_cmd ffmpeg; then
    echo "System ffmpeg ready: $(command -v ffmpeg)"
    return 0
  fi

  if install_with_sudo_if_possible; then
    echo "System ffmpeg installed: $(command -v ffmpeg)"
    return 0
  fi

  install_static_ffmpeg
  "$LOCAL_FFMPEG" -version | head -n 1
}

main "$@"
