# LogSentinel

An AI-powered log analyzer and anomaly detection portfolio project built with:
- Python
- Bash
- Ansible
- Docker
- Prometheus
- Grafana
- GitHub Actions

## Project Overview

`LogSentinel` is designed to deploy a containerized LAMP stack, collect Apache access logs, analyze them with a Python anomaly detector, and surface metrics and alerts via Prometheus, Grafana, and Slack.

The project is implemented in phases:
- **Phase 1:** Ansible roles and multi-environment inventory
- **Phase 2:** Prometheus + Grafana deployment via Ansible
- **Phase 3:** Python log parser and Isolation Forest anomaly detector
- **Phase 4:** Bash watcher script that tails Apache logs and triggers detection
- **Phase 5:** Alerting with Pushgateway and Slack webhook
- **Phase 6:** GitHub Actions CI/CD to run Ansible on push to `main`

## Repository Structure

```
logsentinel/
├── alerter.py
├── detector.py
├── Dockerfile
├── parser.py
├── requirements.txt
├── sample_access.log
├── watcher.sh
ansible/
├── group_vars/
│   └── all/
│       └── vault.yml
├── inventories/
│   ├── dev/
│   │   └── hosts.yml
│   ├── staging/
│   │   └── hosts.yml
│   └── prod/
│       └── hosts.yml
├── roles/
│   ├── docker/
│   │   └── tasks/main.yml
│   ├── lamp/
│   │   └── tasks/main.yml
│   ├── monitoring/
│   │   └── tasks/main.yml
│   └── logsentinel/
│       └── tasks/main.yml
└── site.yml
monitoring/
├── grafana/
│   ├── dashboards/
│   │   └── node-exporter-dashboard.json
│   └── provisioning/
│       ├── datasources/
│       │   └── prometheus.yml
│       └── dashboards/
│           └── dashboard.yml
└── prometheus.yml
.github/
└── workflows/
    └── deploy.yml
```

## File and Folder Details

### `ansible/`

#### `inventories/`
- `dev/hosts.yml` — local development inventory with `localhost` and local Python interpreter.
- `staging/hosts.yml` — placeholder remote host inventory for staging.
- `prod/hosts.yml` — placeholder remote host inventory for production.

#### `group_vars/all/vault.yml`
Contains sensitive variables used by the playbook:
- `db_root_password`
- `db_name`
- `db_user`
- `db_password`
- `slack_webhook_url`
- `prometheus_pushgateway_url`

> This file should be encrypted with `ansible-vault encrypt` before using in a real environment.

#### `site.yml`
The main playbook. It currently applies these roles:
- `docker`
- `lamp`
- `monitoring`

#### `roles/docker/tasks/main.yml`
Installs Docker Engine on Debian/Ubuntu and RedHat-style systems, then enables and starts the Docker service.

#### `roles/lamp/tasks/main.yml`
Installs a LAMP stack:
- Apache
- MySQL / MariaDB
- PHP

Also secures the MySQL root password and creates a `logsentinel` database/user.

#### `roles/monitoring/tasks/main.yml`
Deploys monitoring containers:
- Prometheus
- Node Exporter
- Pushgateway
- Grafana

It also copies the Prometheus configuration from `monitoring/prometheus.yml`.

#### `roles/logsentinel/tasks/main.yml`
Placeholder role for future LogSentinel application deployment logic.

### `monitoring/`

#### `prometheus.yml`
Prometheus scrape configuration for:
- Prometheus itself
- Node Exporter
- Pushgateway

#### `grafana/provisioning/datasources/prometheus.yml`
Auto-provisions Grafana datasource to connect Grafana to Prometheus.

#### `grafana/provisioning/dashboards/dashboard.yml`
Auto-provisions dashboards from local JSON files.

#### `grafana/dashboards/node-exporter-dashboard.json`
Basic dashboard showing:
- CPU load
- Memory usage
- Disk IO rate

### `logsentinel/`

#### `parser.py`
Parses Apache access logs into structured records using regex. It normalizes:
- remote host
- timestamp
- HTTP method/path/protocol
- status code
- bytes sent
- referer and user agent
- response time in milliseconds

It supports combined Apache log format and optional response time values.

#### `detector.py`
Aggregates parsed records by client IP and builds a feature vector for each IP:
- total requests
- error rate
- average response time
- unique URL paths

Then it uses `sklearn.ensemble.IsolationForest` to detect anomalous IP activity.

#### `alerter.py`
Wraps the detector and adds observability and alerting:
- pushes custom metrics to Prometheus Pushgateway
- sends Slack alerts for anomalies
- writes JSON results to disk

Metrics emitted include:
- `logsentinel_anomaly_score`
- `logsentinel_anomaly`
- `logsentinel_error_rate`
- `logsentinel_average_response_time_ms`
- `logsentinel_total_requests`

#### `watcher.sh`
A Bash watcher that:
- tails an Apache access log file with `tail -F`
- buffers new lines into a temporary file
- invokes `alerter.py` after a number of lines
- pushes metrics to Pushgateway and optionally sends Slack alerts

#### `requirements.txt`
Python dependencies:
- `scikit-learn`
- `numpy`
- `requests`

#### `Dockerfile`
Builds a minimal Python container with the LogSentinel detector and alerter.

#### `sample_access.log`
A small sample access log for local testing and learning.

### `.github/workflows/deploy.yml`
GitHub Actions workflow that:
- runs on push to `main`
- checks out the repo
- sets up Python 3.12
- installs Ansible
- optionally reads `ANSIBLE_VAULT_PASSWORD` from GitHub Secrets
- runs `ansible-playbook -i ansible/inventories/dev/hosts.yml ansible/site.yml`

## How to Run Locally

### 1. Use WSL on Windows
Because Ansible and the Bash watcher are Linux-native, WSL is the recommended environment for this repo.

From PowerShell:
```powershell
wsl
cd /mnt/c/Users/perei/Documents/GitHub/devops-portfolio/AIOps
```

### 2. Install Python dependencies
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r logsentinel/requirements.txt
```

### 3. Run the sample detector
```bash
python3 logsentinel/detector.py --log-file logsentinel/sample_access.log
```

### 4. Run the alerter with Pushgateway and Slack
```bash
python3 logsentinel/alerter.py \
  --log-file logsentinel/sample_access.log \
  --pushgateway-url http://localhost:9091 \
  --slack-webhook-url https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX \
  --output logsentinel/anomalies.json
```

### 5. Run the watcher script
```bash
chmod +x logsentinel/watcher.sh
./logsentinel/watcher.sh \
  logsentinel/sample_access.log \
  logsentinel/alerter.py \
  /tmp/logsentinel_anomalies.json \
  10 \
  0.05 \
  http://localhost:9091 \
  https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
```

### 6. Run Ansible with the dev inventory
```bash
ansible-playbook -i ansible/inventories/dev/hosts.yml ansible/site.yml
```

## How to Test Each Phase

### Phase 1: Ansible roles
- Verify inventory paths exist
- Verify `ansible/site.yml` references `docker`, `lamp`, and `monitoring`
- Run `ansible-playbook -i ansible/inventories/dev/hosts.yml ansible/site.yml`

### Phase 2: Monitoring stack
- Verify Prometheus and Grafana containers start
- Visit `http://localhost:9090` and `http://localhost:3000`
- Check `monitoring/prometheus.yml` contains node exporter and pushgateway scraping

### Phase 3: Log parsing and detection
- Run `python3 logsentinel/detector.py --log-file logsentinel/sample_access.log`
- Confirm output contains `anomalies`

### Phase 4: Watcher script
- Run `bash -n logsentinel/watcher.sh` to validate script syntax
- Execute the watcher against `sample_access.log`

### Phase 5: Pushgateway and Slack alerts
- Ensure Pushgateway is deployed by the monitoring role
- Send an alert and verify metrics appear in Prometheus
- Confirm Slack webhook alert text is delivered

### Phase 6: GitHub Actions
- Push to `main`
- Check workflow `.github/workflows/deploy.yml`
- Set `ANSIBLE_VAULT_PASSWORD` secret if `vault.yml` is encrypted

## Learning Notes

### Why use Ansible with Docker?
Ansible provides declarative infrastructure automation. In this project it:
- installs Docker
- runs containerized monitoring services
- manages configuration files

Docker keeps Prometheus, Grafana, and Pushgateway isolated and reproducible.

### Why use Isolation Forest?
`IsolationForest` is an unsupervised anomaly detection algorithm that:
- isolates unusual observations in a dataset
- works well on numeric features without labels
- is well-suited to log-based anomaly detection where ground truth is unavailable

### What the Python detector learns
The detector is not a rule engine. Instead it learns patterns from aggregated behavior per IP address:
- high error rates
- slow response times
- unusual request volume
- many distinct requested paths

### Why Pushgateway?
Pushgateway enables short-lived applications to expose Prometheus metrics by pushing them instead of being scraped directly.

### Why Slack alerts?
Slack provides a real-time channel to notify engineers when anomalies are found.

## What is still placeholder

`ansible/roles/logsentinel/tasks/main.yml` is intentionally left as a placeholder for deploying the actual LogSentinel application code and configuration in future work.

## Improvements to make next

- Add real LogSentinel application container deployment in `roles/logsentinel`
- Expand Grafana dashboards for Apache and anomaly metrics
- Add alert rules in Prometheus
- Add production-ready secrets handling with Ansible Vault
- Add automated tests for Python parser and detector
- Add Grafana provisioning for dashboards and alerts

## Useful commands

```bash
# Validate Bash watcher syntax
bash -n logsentinel/watcher.sh

# Validate Python files
python3 -m py_compile logsentinel/*.py

# Test Ansible inventory
ansible-inventory -i ansible/inventories/dev/hosts.yml --list

# Run GitHub Action locally with act (optional)
act -j deploy
```
