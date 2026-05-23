#!/usr/bin/env python3
import argparse
import json
from datetime import datetime

import requests

from detector import LogSentinelDetector
from parser import parse_file


def _escape_label_value(value):
    return value.replace("\\", "\\\\").replace('"', '\\"')


def build_metrics(anomalies):
    lines = []
    for entry in anomalies:
        host = _escape_label_value(entry["remote_host"])
        anomaly_flag = int(entry["anomaly"])
        labels = f'remote_host="{host}"'
        lines.append(f'logsentinel_anomaly_score{{{labels}}} {entry["anomaly_score"]}')
        lines.append(f'logsentinel_anomaly{{{labels}}} {anomaly_flag}')
        lines.append(f'logsentinel_error_rate{{{labels}}} {entry["error_rate"]}')
        lines.append(f'logsentinel_average_response_time_ms{{{labels}}} {entry["average_response_time_ms"]}')
        lines.append(f'logsentinel_total_requests{{{labels}}} {entry["total_requests"]}')
    return "\n".join(lines) + "\n"


def push_to_pushgateway(pushgateway_url, metrics, job="logsentinel"):
    if not pushgateway_url:
        return None
    endpoint = pushgateway_url.rstrip("/") + f"/metrics/job/{job}"
    response = requests.put(endpoint, data=metrics.encode("utf-8"), headers={"Content-Type": "text/plain; charset=utf-8"})
    response.raise_for_status()
    return response.text


def notify_slack(slack_webhook_url, anomalies, log_file):
    if not slack_webhook_url or not anomalies:
        return None

    top_anomalies = anomalies[:5]
    lines = [
        f"*LogSentinel anomaly alert* for `{log_file}`",
        f"Detected {len(anomalies)} anomalous remote hosts.",
        "",
    ]
    for entry in top_anomalies:
        lines.append(
            f"• `{entry['remote_host']}` — score={entry['anomaly_score']:.3f}, "
            f"errors={entry['error_rate']:.2f}, avg_rt={entry['average_response_time_ms']}ms, "
            f"requests={entry['total_requests']}"
        )
    payload = {"text": "\n".join(lines)}
    response = requests.post(slack_webhook_url, json=payload)
    response.raise_for_status()
    return response.text


def main():
    parser = argparse.ArgumentParser(description="Detect anomalies and send metrics/alerts.")
    parser.add_argument("--log-file", required=True, help="Path to the Apache access log file.")
    parser.add_argument("--pushgateway-url", required=False, default=None, help="Prometheus Pushgateway base URL.")
    parser.add_argument("--slack-webhook-url", required=False, default=None, help="Slack webhook URL for alert notifications.")
    parser.add_argument("--contamination", type=float, default=0.05, help="Expected anomaly ratio for Isolation Forest.")
    parser.add_argument("--output", required=False, help="Optional JSON output path for anomaly results.")
    parser.add_argument("--job", required=False, default="logsentinel", help="Pushgateway job name.")
    args = parser.parse_args()

    records = parse_file(args.log_file)
    detector = LogSentinelDetector(contamination=args.contamination)
    anomalies = detector.detect(records)

    result = {
        "log_file": args.log_file,
        "records_parsed": len(records),
        "anomalies": anomalies,
    }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2)

    if args.pushgateway_url:
        metrics = build_metrics(anomalies)
        push_to_pushgateway(args.pushgateway_url, metrics, job=args.job)

    if args.slack_webhook_url and anomalies:
        notify_slack(args.slack_webhook_url, anomalies, args.log_file)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
