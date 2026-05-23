import argparse
import json
from collections import defaultdict
from statistics import mean

from sklearn.ensemble import IsolationForest

from parser import parse_file


class LogSentinelDetector:
    def __init__(self, contamination=0.05, n_estimators=100, random_state=42):
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.model = None

    def _aggregate_by_ip(self, records):
        buckets = defaultdict(list)
        for record in records:
            buckets[record["remote_host"]].append(record)

        rows = []
        for remote_host, bucket in buckets.items():
            total_requests = len(bucket)
            error_requests = sum(1 for record in bucket if record["status"] >= 500)
            response_times = [record["response_time_ms"] for record in bucket if record["response_time_ms"] > 0]
            average_response_time = int(mean(response_times)) if response_times else 0
            unique_paths = len({record["path"] for record in bucket})
            error_rate = error_requests / total_requests if total_requests else 0.0

            rows.append({
                "remote_host": remote_host,
                "total_requests": total_requests,
                "error_rate": error_rate,
                "average_response_time_ms": average_response_time,
                "unique_paths": unique_paths,
            })

        return rows

    def _feature_matrix(self, aggregated_rows):
        return [
            [
                float(row["total_requests"]),
                float(row["error_rate"]),
                float(row["average_response_time_ms"]),
                float(row["unique_paths"]),
            ]
            for row in aggregated_rows
        ]

    def detect(self, records):
        aggregated = self._aggregate_by_ip(records)
        if len(aggregated) < 2:
            return []

        X = self._feature_matrix(aggregated)
        self.model = IsolationForest(
            n_estimators=self.n_estimators,
            contamination=self.contamination,
            random_state=self.random_state,
        )
        self.model.fit(X)

        raw_scores = self.model.score_samples(X)
        predictions = self.model.predict(X)

        anomalies = []
        for row, score, prediction in zip(aggregated, raw_scores, predictions):
            anomalies.append({
                "remote_host": row["remote_host"],
                "total_requests": row["total_requests"],
                "error_rate": row["error_rate"],
                "average_response_time_ms": row["average_response_time_ms"],
                "unique_paths": row["unique_paths"],
                "anomaly_score": float(-score),
                "anomaly": prediction == -1,
            })

        anomalies.sort(key=lambda entry: entry["anomaly_score"], reverse=True)
        return anomalies


def main():
    parser = argparse.ArgumentParser(description="Detect anomalies in Apache access logs.")
    parser.add_argument("--log-file", required=True, help="Path to the Apache access log file.")
    parser.add_argument("--contamination", type=float, default=0.05, help="Ratio of anomalies expected in the dataset.")
    parser.add_argument("--output", required=False, help="Optional path to write JSON results.")
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
        with open(args.output, "w", encoding="utf-8") as output_handle:
            json.dump(result, output_handle, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
