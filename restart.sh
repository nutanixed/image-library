#!/bin/bash
# Image Library Web Interface Restart Script
# This script restarts the docker container

echo "🔄 Restarting Image Library Web Interface Container..."

cd /home/nutanix/plex-docker
docker compose up -d nutanix-images-ui

echo "✅ Image Library container restart triggered"
echo "📝 Logs: docker compose logs -f nutanix-images-ui"
echo "🌐 Interface: http://localhost:8083"
