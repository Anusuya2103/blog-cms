# 1. Requirement Analysis

## 1.1 Project Overview
BlogCMS is a full-stack Blog/Content Management System built to demonstrate a
complete DevOps lifecycle: from application development through
containerization, continuous integration, continuous delivery, and
deployment. The application itself (a blogging platform) is intentionally a
well-understood domain, so the project's complexity is concentrated in the
DevOps pipeline rather than in unfamiliar business logic.

## 1.2 Objectives
- Build a working 3-tier web application (frontend, backend API, database).
- Containerize every service independently using Docker.
- Orchestrate the multi-container stack using Docker Compose.
- Automate build, test, and deployment using a CI/CD pipeline (GitHub Actions).
- Demonstrate role-based access control, authentication, and a relational
  data model.
- Produce a deployable artifact (Docker images) that can run identically in
  development and production.

## 1.3 Scope
### In Scope
- User registration/login with JWT-based authentication.
- Role-based permissions: admin, author, reader.
- Blog post CRUD (create, read, update, delete) with draft/publish states.
- Category tagging and search/filter.
- Commenting system.
- Dockerized backend, frontend, and database.
- CI/CD pipeline: lint, test, build, containerize, push, deploy.

### Out of Scope
- Rich-text/WYSIWYG editing (plain text content only).
- Image/media upload and storage.
- Payment or subscription features.
- Multi-region / high-availability infrastructure.

## 1.4 Functional Requirements
| ID | Requirement |
|---|---|
| FR1 | Users can register and log in; the first registered user becomes admin. |
| FR2 | Authenticated authors/admins can create, edit, and delete their own posts. |
| FR3 | Admins can manage any post or category. |
| FR4 | Any visitor can view published posts without logging in. |
| FR5 | Authenticated users can comment on posts. |
| FR6 | Posts can be filtered by category or searched by keyword. |
| FR7 | The system exposes a health-check endpoint for monitoring. |

## 1.5 Non-Functional Requirements
| ID | Requirement |
|---|---|
| NFR1 | The full stack must start with a single `docker compose up` command. |
| NFR2 | Passwords must be hashed (bcrypt) — never stored in plain text. |
| NFR3 | API responses should return within ~500ms under normal local load. |
| NFR4 | The CI pipeline must block image builds if tests fail. |
| NFR5 | Docker images should run as a non-root user where feasible (backend). |

## 1.6 Tools & Technologies Selected
| Layer | Technology | Reasoning |
|---|---|---|
| Frontend | React (Vite) | Fast dev server, small production bundle, component reuse |
| Backend | FastAPI (Python) | Async-ready, automatic OpenAPI docs, strong typing via Pydantic |
| Database | MySQL 8.0 | Relational data (users/posts/comments), widely used in production |
| Containerization | Docker | Industry-standard, reproducible environments |
| Orchestration | Docker Compose | Sufficient for a 3-service stack; simpler than Kubernetes for this scope |
| CI/CD | GitHub Actions | Native to GitHub, free tier sufficient, YAML-based pipelines |
| Web server | Nginx | Serves static frontend build, reverse-proxies API calls |

## 1.7 Stakeholders
- **Developer/Student:** builds and documents the system (project author).
- **End users (simulated):** readers, authors, and admins interacting with the blog.
- **Evaluator/Reviewer:** assesses the project against DevOps learning outcomes.
