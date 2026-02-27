#!/usr/bin/env bash
# Helper script to build and run the homeserver Flask app in Docker.
# Usage: ./run.sh [-p port] [-u host_upload_dir] [-n container_name]

set -euo pipefail

PORT=5000
UPLOAD_PATH="$(pwd)/uploads"
NAME="homeserver"

usage() {
    cat <<'EOF'
Usage: $0 [-p port] [-u upload_path] [-n name] [-h]

Options:
  -p PORT          Host port to bind and pass through to the container (also sets PORT env var).
  -u UPLOAD_PATH   Host directory to mount for uploads (container sees it at /data/uploads).
  -n NAME          Docker image and container name (default: homeserver).
  -h               Show this help message.

Example:
  ./run.sh -p 8080 -u /tmp/myuploads -n myserver
EOF
}

while getopts ":p:u:n:h" opt; do
    case ${opt} in
        p) PORT="${OPTARG}" ;; 
        u) UPLOAD_PATH="${OPTARG}" ;; 
        n) NAME="${OPTARG}" ;; 
        h) usage; exit 0 ;;
        *) echo "Unknown option: ${opt}"; usage; exit 1 ;;
    esac
done

# build the image
echo "Building Docker image '${NAME}'..."
docker build -t "${NAME}" .

# stop/remove any existing container with the same name
if docker ps -a --format '{{.Names}}' | grep -qx "${NAME}"; then
    echo "Removing existing container '${NAME}'..."
    docker rm -f "${NAME}" >/dev/null 2>&1 || true
fi

# run the container
echo "Running container '${NAME}' (port ${PORT}, uploads path '${UPLOAD_PATH}')..."
docker run -d \
    --name "${NAME}" \
    -p "${PORT}:${PORT}" \
    -e PORT="${PORT}" \
    -e UPLOAD_FOLDER="/data/uploads" \
    -v "${UPLOAD_PATH}:/data/uploads" \
    "${NAME}"

echo "Container started. Access the app at http://localhost:${PORT}/"
