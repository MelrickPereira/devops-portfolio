import re
from datetime import datetime

LOG_PATTERN = re.compile(
    r'(?P<remote_host>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] '
    r'"(?P<request>[^"]*)" (?P<status>\d{3}) (?P<size>\S+)'
    r'(?: "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)")?'
    r'(?: (?P<response_time>\d+))?'
)


def parse_line(line):
    """Parse a single Apache access-log line into a normalized record."""
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None

    data = match.groupdict()
    request = data.get("request") or ""
    method, path, protocol = "", "", ""
    request_parts = request.split()
    if len(request_parts) == 3:
        method, path, protocol = request_parts
    elif len(request_parts) == 2:
        method, path = request_parts
    elif len(request_parts) == 1:
        path = request_parts[0]

    timestamp = _parse_timestamp(data["timestamp"])
    status = int(data["status"])
    bytes_sent = 0 if data["size"] == "-" else int(data["size"])
    response_time_ms = int(data["response_time"]) if data.get("response_time") else 0

    return {
        "remote_host": data["remote_host"],
        "timestamp": timestamp,
        "method": method,
        "path": path,
        "protocol": protocol,
        "status": status,
        "bytes_sent": bytes_sent,
        "referer": data.get("referer") or "",
        "user_agent": data.get("user_agent") or "",
        "response_time_ms": response_time_ms,
    }


def _parse_timestamp(timestamp_text):
    formats = ["%d/%b/%Y:%H:%M:%S %z", "%d/%b/%Y:%H:%M:%S"]
    for fmt in formats:
        try:
            return datetime.strptime(timestamp_text, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unsupported timestamp format: {timestamp_text}")


def parse_file(path):
    """Parse an Apache access log file into a list of record dictionaries."""
    records = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = parse_line(line)
            if record is not None:
                records.append(record)
    return records
