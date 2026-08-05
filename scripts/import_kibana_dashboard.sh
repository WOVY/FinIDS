#!/bin/sh
# Phase 5 #42: docker compose up 이후 Kibana Saved Objects(대시보드)를 자동 임포트한다.
# 사용법: ./scripts/import_kibana_dashboard.sh [kibana_url]

set -eu

KIBANA_URL="${1:-http://localhost:5601}"
NDJSON_PATH="$(dirname "$0")/../kibana/saved_objects.ndjson"

echo "[kibana-import] Kibana(${KIBANA_URL}) 준비 대기 중..."
until curl -sf "${KIBANA_URL}/api/status" > /dev/null 2>&1; do
  sleep 2
done

echo "[kibana-import] Saved Objects 임포트: ${NDJSON_PATH}"
curl -sf -X POST "${KIBANA_URL}/api/saved_objects/_import?overwrite=true" \
  -H "kbn-xsrf: true" \
  --form "file=@${NDJSON_PATH}"

echo
echo "[kibana-import] 완료"
