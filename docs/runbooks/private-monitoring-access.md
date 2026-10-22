# Private monitoring access

Status (2026-10-22): private HTTPS active on ports 9444–9446; all three
HTTPS health checks return 200. User confirmed phone access over mobile data,
Grafana login, and warning-free Prometheus access on 9446. Port 443 Serve
listener disabled after collision with Traefik. Old monitoring HTTP Ingress
manifests removed from this branch; corresponding live resources retired.

## Architecture

Phone or laptop running Tailscale -> Tailscale Serve HTTPS -> host-loopback
NGINX proxy -> Kubernetes Service -> monitoring Pod.

The server is `ubuntu.tail4beac2.ts.net`. Serve access follows tailnet access
rules; this does not add application authentication. Review tailnet permissions
in the Tailscale admin console. Do not enable Funnel.

The proxy uses host networking specifically to bind 127.0.0.1 on the Ubuntu
node, with no host filesystem mounts, service-account token, or capabilities.
It is a single-node design: node selector `ubuntu`, cluster DNS `10.43.0.10`,
and loopback ports 19090, 13000, 19093. Adjust these for another cluster.
Image nginx:1.28-alpine is versioned but not digest-pinned; review and scan the
image through the future CI pipeline. ConfigMap changes require a proxy restart.

## Reproduce

From this branch's worktree:

```bash
kubectl apply --dry-run=server --validate=strict -f k8s/private-access/proxy.yml
kubectl apply -f k8s/private-access/proxy.yml
kubectl rollout status deployment/monitoring-private-proxy -n monitoring --timeout=120s
curl -fsS http://127.0.0.1:19090/-/ready
curl -fsS http://127.0.0.1:13000/api/health
curl -fsS http://127.0.0.1:19093/-/ready
```

Enable persistent, tailnet-only HTTPS listeners on the Ubuntu server.
For the existing setup, first disable the former listener with
`sudo tailscale serve --https=443 off`:

```bash
sudo tailscale serve --bg --https=9446 http://127.0.0.1:19090
sudo tailscale serve --bg --https=9444 http://127.0.0.1:13000
sudo tailscale serve --bg --https=9445 http://127.0.0.1:19093
tailscale serve status
tailscale funnel status
```

Serve provisions HTTPS certificates. Hostnames appear in public certificate
transparency logs; application access remains restricted to the tailnet.
HTTPS terminates on the host; the proxy-to-Service hop uses cluster HTTP.

## Device validation

Install/open Tailscale on the phone and Ubuntu laptop, sign into the same tailnet,
and connect. Test:

- Prometheus: https://ubuntu.tail4beac2.ts.net:9446
- Grafana: https://ubuntu.tail4beac2.ts.net:9444
- Alertmanager: https://ubuntu.tail4beac2.ts.net:9445

Confirm trusted certificates, Grafana login, Prometheus target health, and
`up{job="random-metrics"} == 1`. Test the phone over mobile data with Tailscale
connected. Disconnect Tailscale and confirm these URLs no longer open.
Other tailnet devices may reach these endpoints if permitted by tailnet policy.

## Retire old HTTP access

The three old Ingress manifests have been removed from this branch.
Retire their live resources when migrating another installation:

```bash
kubectl delete ingress -n monitoring prometheus-ingress grafana-ingress alertmanager-ingress
```

Confirm old HTTP URLs no longer serve monitoring UIs and private HTTPS still
works. The chart files must also be removed to prevent later re-creation.
Do not change Traefik globally, SSH, or host firewall rules as part of this step.
A live browser check from a different device is required before retiring routes.

## Rollback

Disable only the listeners introduced here:

```bash
sudo tailscale serve --https=9446 off
sudo tailscale serve --https=9444 off
sudo tailscale serve --https=9445 off
kubectl delete -f k8s/private-access/proxy.yml
```

If old Ingress resources were removed, restore the manifests from Git and apply
them individually. Leave working runtime secrets and Grafana's PVC intact.

## Validation recorded

- Strict server dry run passed.
- Proxy Pod: ready, zero restarts at validation.
- Prometheus /-/ready: HTTP 200.
- Grafana /api/health: HTTP 200.
- Alertmanager /-/ready: HTTP 200.
- Serve activated by user; phone access over mobile data confirmed.
- Grafana and Alertmanager HTTPS certificates and health responses verified.
- Prometheus scrape query returns 1 through loopback proxy.
- Port 443 Serve listener disabled; Prometheus HTTPS on 9446 verified.
- Old monitoring Ingress resources and branch manifests removed.
- Tailnet-disconnected device test: pending user validation.

References:
- https://tailscale.com/docs/features/tailscale-serve
- https://tailscale.com/docs/reference/tailscale-cli/serve
