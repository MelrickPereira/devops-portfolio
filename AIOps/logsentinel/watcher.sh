#!/usr/bin/env bash
set -euo pipefail

LOG_FILE="${1:-/var/log/apache2/access.log}"
ALERTER_SCRIPT="${2:-$(dirname "$0")/alerter.py}"
OUTPUT_FILE="${3:-/tmp/logsentinel_anomalies.json}"
MIN_LINES="${4:-10}"
CONTAMINATION="${5:-0.05}"
PUSHGATEWAY_URL="${6:-http://localhost:9091}"
SLACK_WEBHOOK_URL="${7:-}"
JOB_NAME="${8:-logsentinel}"

if [ ! -f "$ALERTER_SCRIPT" ]; then
  echo "ERROR: alerter script not found at $ALERTER_SCRIPT" >&2
  exit 1
fi

if [ ! -f "$LOG_FILE" ]; then
  echo "ERROR: log file not found at $LOG_FILE" >&2
  exit 1
fi

TMP_WINDOW_FILE="$(mktemp /tmp/logsentinel_watch.XXXXXX)"
LINE_COUNTER=0

cleanup() {
  rm -f "$TMP_WINDOW_FILE"
}
trap cleanup EXIT INT TERM

echo "Watching Apache log: $LOG_FILE"
echo "Alerter: $ALERTER_SCRIPT"
echo "Output: $OUTPUT_FILE"
echo "Trigger after $MIN_LINES new lines"
echo "Pushgateway: $PUSHGATEWAY_URL"
echo "Slack webhook: ${SLACK_WEBHOOK_URL:-<not configured>}"

run_detection() {
  if [ "$LINE_COUNTER" -eq 0 ]; then
    return
  fi

  python3 "$ALERTER_SCRIPT" \
    --log-file "$TMP_WINDOW_FILE" \
    --contamination "$CONTAMINATION" \
    --output "$OUTPUT_FILE" \
    --pushgateway-url "$PUSHGATEWAY_URL" \
    --slack-webhook-url "$SLACK_WEBHOOK_URL" \
    --job "$JOB_NAME"

  LINE_COUNTER=0
  : > "$TMP_WINDOW_FILE"
}

# Start tailing the file and run detection every MIN_LINES lines.
# Using -F to handle log rotation.
tail -F "$LOG_FILE" | while IFS= read -r line; do
  echo "$line" >> "$TMP_WINDOW_FILE"
  LINE_COUNTER=$((LINE_COUNTER + 1))
  if [ "$LINE_COUNTER" -ge "$MIN_LINES" ]; then
    run_detection
  fi
done
