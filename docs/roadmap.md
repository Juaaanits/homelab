# Roadmap

Updated 2026-10-22. Completed items record implemented learning milestones;
historical Ingress exercises do not describe current access.

## Private access milestone

- [x] Deploy loopback-only monitoring proxy with constrained container privileges
- [x] Enable Tailscale Serve HTTPS on 9444, 9445, and 9446
- [x] Verify all three HTTPS health endpoints
- [x] Verify exporter scrape reports UP
- [x] User confirms phone access over mobile data and Grafana login
- [x] Remove old monitoring HTTP Ingress resources and manifests
- [x] Disable conflicting Serve listener on port 443
- [ ] User verifies private URLs fail with Tailscale disconnected
- [ ] Review tailnet access rules for intended users/devices

## Next milestone

Complete Helm packaging and rendering before CI or Argo CD activation.
Resolve Chart.yaml / values.yaml naming, embedded template escaping, unused
values, and invalid reference SealedSecret. Plan ownership migration of existing
resources and preserve Grafana storage.


## Phase 1 - Host and remote administration

- [x] Repurpose MacBook Air
- [x] Install Ubuntu Server 24.04
- [x] Configure SSH
- [x] Develop through VS Code Remote SSH

## Phase 2 - Initial monitoring stack

- [x] Docker / Docker Compose monitoring
- [x] Prometheus
- [x] Grafana
- [x] Alertmanager
- [x] node-exporter
- [x] custom Python exporter
- [x] Tear down old Compose stack after Kubernetes migration

## Phase 3 - Kubernetes fundamentals

- [x] Install k3s
- [x] Configure `kubectl`
- [x] Create `monitoring` namespace
- [x] Deploy Prometheus
- [x] Deploy Grafana
- [x] Add Grafana persistent storage
- [x] Deploy node-exporter as DaemonSet
- [x] Deploy Alertmanager
- [x] Configure Services
- [x] Configure alerts
- [x] Validate Telegram alerting with a real forced outage

## Phase 4 - Networking

- [x] Traefik Ingress
- [x] `sslip.io`
- [x] Grafana Ingress
- [x] Prometheus Ingress
- [x] Alertmanager Ingress
- [x] Remove unnecessary Grafana NodePort
- [x] Verify Ingress → Service → EndpointSlice → Pod

## Phase 5 - Custom Kubernetes workload

- [x] Build `random-metrics:v0.1.0`
- [x] Import image into k3s/containerd
- [x] Deploy with Deployment
- [x] Add ClusterIP Service
- [x] Verify in-cluster DNS
- [x] Add Prometheus scrape target
- [x] Query `my_random_metric`
- [x] Configure explicit 15-second scrape/evaluation interval
- [x] Add explicit `/metrics`
- [x] Add `/healthz`
- [x] Add readiness probe
- [x] Add liveness probe
- [x] Add resource requests and limits
- [x] Add non-root / security context

## Phase 6 - Helm

- [ ] Create real `Chart.yaml`
- [ ] Create real `values.yaml`
- [ ] Template images and tags
- [ ] Template replica counts
- [ ] Template storage sizes
- [ ] Template Ingress hostnames
- [ ] Template resource settings
- [ ] Correctly escape Prometheus templates
- [ ] `helm lint`
- [ ] `helm template`

## Phase 7 - CI and image supply chain

- [ ] GitHub Actions
- [ ] Helm lint in CI
- [ ] Helm render validation
- [ ] Trivy scan
- [ ] Build random-metrics in CI
- [ ] Push versioned image to GHCR
- [ ] Remove local image-import dependency

## Phase 8 - GitOps

- [ ] Install Argo CD
- [ ] Connect repository
- [ ] Deploy Helm chart from Git
- [ ] Enable auto-sync
- [ ] Test drift detection
- [ ] Make Git the normal source of desired state

## Phase 9 - Policy as Code

- [ ] Install Kyverno
- [ ] Reject `:latest`
- [ ] Require standard labels
- [ ] Require resource requests
- [ ] Require resource limits where appropriate
- [ ] Require non-root workloads
- [ ] Disallow privilege escalation
- [ ] Intentionally test denied manifests

## Phase 10 - Secrets

- [ ] Install Sealed Secrets controller
- [ ] Seal Grafana credentials against this cluster
- [ ] Seal Telegram credentials against this cluster
- [ ] Remove dead reference SealedSecret
- [ ] Commit only encrypted SealedSecret resources
- [ ] Validate clean reconstruction

## Phase 11 - Terraform

- [ ] Define Terraform scope
- [ ] Automate repeatable bootstrap tasks where useful
- [ ] Document intentionally manual steps
- [ ] Test rebuild procedure

---

# Definition of Done

I will consider the portfolio version complete when:

- [ ] the monitoring stack is packaged with Helm
- [ ] CI validates every change
- [ ] the custom image is built and security-scanned automatically
- [ ] versioned images are published to GHCR
- [ ] Argo CD owns normal deployment/reconciliation
- [ ] Kyverno enforces baseline workload security
- [ ] credentials are represented in Git only as encrypted SealedSecrets
- [ ] no production workload depends on `:latest`
- [x] the custom workload has health probes and resource controls
- [ ] the stack can be recreated from repository state plus documented bootstrap steps
- [x] architecture and troubleshooting are documented

---

