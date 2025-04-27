# Kubernetes Pod Security Monitoring & Enforcement

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/bharats487/k8s-pod-security-monitor.svg)](https://github.com/bharats487/k8s-pod-security-monitor/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/bharats487/k8s-pod-security-monitor.svg)](https://github.com/bharats487/k8s-pod-security-monitor/issues)
[![Last Commit](https://img.shields.io/github/last-commit/bharats487/k8s-pod-security-monitor.svg)](https://github.com/bharats487/k8s-pod-security-monitor/commits/master)

This project provides real-time monitoring and best-practice enforcement for Kubernetes pod security, combining:

- **Live monitoring** of pod security violations (Python backend + web dashboard)
- **Automated enforcement** of Pod Security Standards and Gatekeeper policies
- **Helm chart** for easy deployment of security controls

---

## Features
- Real-time alerts for pods violating security best practices (privileged, missing securityContext, etc.)
- Web dashboard for instant visibility
- Enforce Kubernetes Pod Security Admission (PSA) at namespace level
- Gatekeeper policy to block privileged containers
- Helm chart for automated setup

---

## Directory Structure

- `backend/` — Python Flask backend for real-time pod monitoring
- `frontend/` — Simple web dashboard for alerts
- `helm-chart/` — Helm chart to label namespaces and enforce privileged-block policy
- `k8s_pod_security_enforcement.yaml` — Example manifest for PSA enforcement
- `gatekeeper_privileged_block.yaml` — Gatekeeper constraint YAML

---

## Quick Start

### 1. Real-Time Monitoring
1. Install Python requirements:
   ```sh
   pip install -r requirements.txt
   ```
2. Ensure your kubeconfig is set (access to cluster).
3. Run backend:
   ```sh
   python backend/main.py
   ```
4. Open `frontend/index.html` in your browser.

### 2. Enforce Pod Security Admission (PSA)
- Apply PSA enforcement to a namespace:
  ```sh
  kubectl apply -f k8s_pod_security_enforcement.yaml
  ```

### 3. Enforce Gatekeeper Policy
- [Install Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/install/)
- Apply privileged-block constraint:
  ```sh
  kubectl apply -f gatekeeper_privileged_block.yaml
  ```

### 4. Automated via Helm
1. Edit `helm-chart/values.yaml` to set your namespace (default: `secure-apps`).
2. Deploy with Helm:
   ```sh
   helm install pod-security-enforcement ./helm-chart
   ```

---

## Extend & Customize
- Add more constraints in `helm-chart/templates/`
- Extend monitoring logic in `backend/main.py`
- Integrate dashboard with alerting systems (Slack, email, etc.)

---

## References & Best Practices
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/)
- [Pod Security Admission Controller](https://kubernetes.io/docs/concepts/security/pod-security-admission/)

---

**For production use, always test policies in audit mode first and review official Kubernetes/Gatekeeper documentation.**
