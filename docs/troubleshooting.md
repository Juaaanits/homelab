# Troubleshooting notes

Use the [README](../README.md) for current architecture, operating commands, and
the roadmap. These notes capture lessons from earlier exercises; retired Ingress
paths are historical examples.

| Symptom or exercise | Cause and lesson | Solution or action taken |
|---|---|---|
| Prometheus could not scrape a running node-exporter Pod | The expected Service was missing. Verify selectors, EndpointSlices, DNS, and the application endpoint. | Added a ClusterIP Service named `node-exporter` on port 9100 with matching Pod selectors. |
| Cordoning did not prevent DaemonSet placement as expected | DaemonSets have special scheduling tolerations. Understand the controller before testing scheduling behavior. | Corrected the interpretation of the test: cordon alone does not exclude DaemonSet Pods. No workload fix was needed. |
| Port-forward stopped after a Pod restart | Port-forward is temporary and tied to a selected Pod. Reconnect or use a durable access mechanism. | Moved UI access to Ingress initially, then to Tailscale Serve for durable private access. |
| Ingress returned 404 | A backend Service name was wrong. Compare the route with actual Services and controller configuration. | Changed the Prometheus Ingress backend from `prometheus-server` to the actual `prometheus:9090` Service. That route has since been retired. |
| `curl -I` returned 405 | HEAD was unsupported while GET worked. Check the HTTP method before concluding routing is broken. | Repeated the request with GET and confirmed successful responses; no application change was needed. |
| Grafana remained reachable through a NodePort | The earlier Service exposure remained enabled. Remove obsolete access paths after verifying the replacement. | Changed the Grafana Service from NodePort to ClusterIP and verified the old node port stopped serving Grafana. |
| A plaintext Secret file was nearly committed | Keep sensitive values out of Git. Ignore rules are only one layer; review staged changes and scan for secrets. | Kept the plaintext manifest out of Git and created runtime Secrets directly in Kubernetes. Encrypted Git-managed secrets remain planned. |
| A reference SealedSecret could not decrypt | Ciphertext belongs to its sealing controller key. Generate it for the intended cluster and preserve recovery keys. | Identified the copied ciphertext as invalid for this cluster and excluded it from use. Removing the reference file and sealing new credentials remain planned. |
| `kubeseal` existed but sealing could not work | The CLI and cluster-side controller are separate prerequisites. | Identified the missing controller. Installing it and validating a complete sealing flow remain planned. |
| A ConfigMap changed but runtime settings did not | Applications may need reload or restart; subPath mounts do not receive ConfigMap updates. Verify effective application configuration. | Restarted Prometheus after configuration changes and checked its runtime configuration. The proxy run instructions also require restart after ConfigMap changes. |
| Docker had the image but k3s could not run it | Docker and containerd use separate image stores. Import the image or publish it to a registry. | Exported the Docker image with `docker save`, imported it with `sudo k3s ctr images import`, and verified the new Pod used `v0.2.0`. |
| YAML passed parsing but Kubernetes rejected it | Valid YAML is not necessarily a valid API resource. Use strict server-side dry runs to check field names and structure. | Created proper Deployment/Service resources, removed the duplicate incomplete Deployment, corrected probe/resource field names and indentation, then passed a strict server dry run. |
| A label-filtered query omitted the Deployment | Object metadata labels and Pod template labels are separate. Apply labels at the intended level. | Added `app: random-metrics` to Deployment metadata, separately from its selector and Pod template labels. |
| A short-lived test Pod produced an attach warning | The command completed before attachment. Interpret lifecycle warnings alongside exit status and logs. | Used the returned command output/logs to confirm the request completed; treated the attach warning as a short-lived Pod lifecycle event. |
| Prometheus scraped every minute instead of every 15 seconds | An empty configuration value fell back to a default. Check the source, ConfigMap, and loaded runtime settings. | Set scrape and evaluation intervals to `15s`, restarted Prometheus, and confirmed effective target intervals. |
| New health probes briefly reported connection refused | The process had not started listening. Check readiness, restarts, and later events; recurring failures require investigation. | Checked subsequent readiness and restart count: the Pod became ready with zero restarts. No probe timing change was required. |
| Deployment logs showed the old application's responses | The command selected a terminating Pod during rollout. Inspect the new Pod explicitly when validating a new image. | Queried the new Pod by name and confirmed both `/healthz` and `/metrics` returned HTTP 200. |
| Private HTTPS on port 443 served Traefik's default certificate | The request reached a competing listener. Dedicated Serve ports resolved the conflict; inspect the actual certificate and routing path. | Moved Prometheus Serve to HTTPS port 9446 and disabled the Serve listener on 443; verified its certificate and readiness response. |

An end-to-end alert exercise deliberately made node-exporter unavailable,
observed TargetDown progress to firing and Telegram notification, then restored
the workload and confirmed recovery. Controlled failure tests validate more than
resource existence alone.
