# Troubleshooting notes

Use the [README](../README.md) for current architecture, operating commands, and
the roadmap. These notes capture lessons from earlier exercises; retired Ingress
paths are historical examples.

| Symptom or exercise | Cause and lesson |
|---|---|
| Prometheus could not scrape a running node-exporter Pod | The expected Service was missing. Verify selectors, EndpointSlices, DNS, and the application endpoint. |
| Cordoning did not prevent DaemonSet placement as expected | DaemonSets have special scheduling tolerations. Understand the controller before testing scheduling behavior. |
| Port-forward stopped after a Pod restart | Port-forward is temporary and tied to a selected Pod. Reconnect or use a durable access mechanism. |
| Ingress returned 404 | A backend Service name was wrong. Compare the route with actual Services and controller configuration. |
| `curl -I` returned 405 | HEAD was unsupported while GET worked. Check the HTTP method before concluding routing is broken. |
| Grafana remained reachable through a NodePort | The earlier Service exposure remained enabled. Remove obsolete access paths after verifying the replacement. |
| A plaintext Secret file was nearly committed | Keep sensitive values out of Git. Ignore rules are only one layer; review staged changes and scan for secrets. |
| A reference SealedSecret could not decrypt | Ciphertext belongs to its sealing controller key. Generate it for the intended cluster and preserve recovery keys. |
| `kubeseal` existed but sealing could not work | The CLI and cluster-side controller are separate prerequisites. |
| A ConfigMap changed but runtime settings did not | Applications may need reload or restart; subPath mounts do not receive ConfigMap updates. Verify effective application configuration. |
| Docker had the image but k3s could not run it | Docker and containerd use separate image stores. Import the image or publish it to a registry. |
| YAML passed parsing but Kubernetes rejected it | Valid YAML is not necessarily a valid API resource. Use strict server-side dry runs to check field names and structure. |
| A label-filtered query omitted the Deployment | Object metadata labels and Pod template labels are separate. Apply labels at the intended level. |
| A short-lived test Pod produced an attach warning | The command completed before attachment. Interpret lifecycle warnings alongside exit status and logs. |
| Prometheus scraped every minute instead of every 15 seconds | An empty configuration value fell back to a default. Check the source, ConfigMap, and loaded runtime settings. |
| New health probes briefly reported connection refused | The process had not started listening. Check readiness, restarts, and later events; recurring failures require investigation. |
| Deployment logs showed the old application's responses | The command selected a terminating Pod during rollout. Inspect the new Pod explicitly when validating a new image. |
| Private HTTPS on port 443 served Traefik's default certificate | The request reached a competing listener. Dedicated Serve ports resolved the conflict; inspect the actual certificate and routing path. |

An end-to-end alert exercise deliberately made node-exporter unavailable,
observed TargetDown progress to firing and Telegram notification, then restored
the workload and confirmed recovery. Controlled failure tests validate more than
resource existence alone.
