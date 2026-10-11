# 5. Deployment & Maintenance

## 5.1 Deployment Process
1. Developer pushes/merges to `main`.
2. CI/CD pipeline runs lint → test → build → push (see `docs/02-system-design.md §2.5`).
3. Docker images `blog-cms-backend` and `blog-cms-frontend` are published to
   GitHub Container Registry (GHCR), tagged both `latest` and with the
   commit SHA (for traceability and rollback).
4. The deploy job calls a PaaS deploy hook. Set the `DEPLOY_HOOK_URL`
   repository secret to your Render / Railway / Fly.io deploy hook and the
   pipeline POSTs to it automatically:
   ```bash
   curl --fail -X POST "$DEPLOY_HOOK_URL"
   ```
   The provider then pulls the freshly pushed image and restarts the stack. On
   a plain VM the equivalent is an SSH step running:
   ```bash
   docker compose pull
   docker compose up -d
   ```
   With no secret set, the job logs a notice and passes, so forks and
   contributors can run the full pipeline without access to your
   infrastructure.

## 5.2 Rollback Strategy
Because every image is tagged with the Git commit SHA (not just `latest`),
rolling back is a matter of redeploying a previous known-good tag:
```bash
docker pull ghcr.io/<repo>/blog-cms-backend:<previous-sha>
docker pull ghcr.io/<repo>/blog-cms-frontend:<previous-sha>
```
then updating `docker-compose.yml` (or the deploy target) to reference that
tag and re-running `docker compose up -d`.

## 5.3 Environment Parity
The same Docker images and `docker-compose.yml` structure run in local
development and production, differing only via environment variables
(`JWT_SECRET_KEY`, `DATABASE_URL`) — eliminating "works on my machine"
inconsistencies.

## 5.4 Monitoring
- `/api/health` reports both application liveness and database
  connectivity, suitable for wiring into:
  - Docker's built-in `HEALTHCHECK` (already configured in both Dockerfiles)
  - An external uptime monitor (e.g., UptimeRobot, a Grafana/Prometheus probe)
- Container logs are available via `docker compose logs -f <service>` for
  troubleshooting.

## 5.5 Maintenance Plan
| Task | Frequency | Notes |
|---|---|---|
| Dependency updates | Monthly | Review `requirements.txt` / `package.json` for security patches |
| Database backups | Daily (production) | `mysqldump` the `db_data` volume or use managed MySQL backups |
| Secret rotation | Quarterly or on suspected leak | Rotate `JWT_SECRET_KEY`; existing tokens invalidate immediately |
| Log review | Weekly | Check for repeated 4xx/5xx patterns indicating abuse or bugs |

## 5.6 Future Enhancements
- Migrate orchestration to Kubernetes (Deployments/Services/Ingress) for
  auto-scaling and self-healing — a natural "Part 2" extension of this project.
- Add Prometheus + Grafana for metrics dashboards.
- Add GitOps-style deployment (ArgoCD/Flux) once running on Kubernetes.
- Add automated frontend tests and end-to-end tests (Playwright/Cypress).
- Add image upload support (e.g., to S3-compatible storage) for post covers.
