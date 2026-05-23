# LogSentinel Phase Guide

## Phase 1: Ansible roles and multi-environment inventory

### What was built
- `ansible/inventories/dev/hosts.yml`
- `ansible/inventories/staging/hosts.yml`
- `ansible/inventories/prod/hosts.yml`
- `ansible/group_vars/all/vault.yml`
- `ansible/site.yml`
- `ansible/roles/docker/tasks/main.yml`
- `ansible/roles/lamp/tasks/main.yml`
- placeholder roles:
  - `ansible/roles/monitoring/tasks/main.yml`
  - `ansible/roles/logsentinel/tasks/main.yml`

### Purpose
- Defines separate inventories for dev, staging, and prod.
- Uses a shared vault variable file for secrets.
- Implements Docker and LAMP installation tasks.

### How to test
```bash
ansible-playbook -i ansible/inventories/dev/hosts.yml ansible/site.yml
```

---

## Phase 2: Prometheus + Grafana deployment

### What was built
- `monitoring/prometheus.yml`
- Grafana provisioning files under `monitoring/grafana/provisioning`
- `monitoring/grafana/dashboards/node-exporter-dashboard.json`
- Updated `ansible/roles/monitoring/tasks/main.yml`
- Updated `ansible/site.yml` to include `monitoring`

### Purpose
- Deploys Prometheus, Grafana, Node Exporter, and Pushgateway containers.
- Configures Prometheus scraping and Grafana datasource/dashboard provisioning.

### How to test
1. Run the playbook:
```bash
ansible-playbook -i ansible/inventories/dev/hosts.yml ansible/site.yml
```
2. Visit:
- `http://localhost:9090` for Prometheus
- `http://localhost:3000` for Grafana
3. Confirm metrics are available in Prometheus.

---

## Phase 3: Python log parser and anomaly detector

### What was built
- `logsentinel/parser.py`
- `logsentinel/detector.py`
- `logsentinel/requirements.txt`
- `logsentinel/Dockerfile`
- `logsentinel/sample_access.log`

### Purpose
- Parses Apache access logs.
- Aggregates request behavior per remote host.
- Uses Isolation Forest to detect anomalous traffic patterns.

### How to test
```bash
python3 -m pip install -r logsentinel/requirements.txt
python3 logsentinel/detector.py --log-file logsentinel/sample_access.log
```

---

## Phase 4: Bash watcher script

### What was built
- `logsentinel/watcher.sh`

### Purpose
- Watches Apache access logs in real time.
- Triggers detection after a batch of new log lines.
- Handles log rotation with `tail -F`.

### How to test
```bash
chmod +x logsentinel/watcher.sh
./logsentinel/watcher.sh logsentinel/sample_access.log
```

---

## Phase 5: Prometheus Pushgateway and Slack alerting

### What was built
- `logsentinel/alerter.py`
- Updated `logsentinel/requirements.txt`
- Updated `logsentinel/Dockerfile`
- Updated `monitoring/prometheus.yml`
- Updated `ansible/roles/monitoring/tasks/main.yml`
- Updated `logsentinel/watcher.sh`

### Purpose
- Pushes anomaly metrics to Prometheus Pushgateway.
- Sends Slack alerts when anomalies are detected.
- Adds end-to-end observability for detected issues.

### How to test
```bash
python3 logsentinel/alerter.py \
  --log-file logsentinel/sample_access.log \
  --pushgateway-url http://localhost:9091 \
  --slack-webhook-url https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX \
  --output logsentinel/anomalies.json
```

---

## Phase 6: GitHub Actions CI/CD

### What was built
- `.github/workflows/deploy.yml`

### Purpose
- Runs Ansible on push to `main`.
- Supports `ANSIBLE_VAULT_PASSWORD` as a GitHub secret.

### How to test
- Push a commit to `main`
- Confirm the workflow runs successfully in GitHub Actions

---

## Recommended next improvements
- Encrypt `ansible/group_vars/all/vault.yml` with Ansible Vault.
- Add real `ansible/roles/logsentinel` deployment tasks.
- Build Grafana dashboards for Apache and anomaly metrics.
- Add Prometheus alert rules.
- Add unit tests for `parser.py` and `detector.py`.
- Add a `docker-compose` development manifest for the monitoring stack.
