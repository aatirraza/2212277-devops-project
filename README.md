# DevOps Capstone Project - 2212277

## Overview
This repository contains a containerized FastAPI microservice connected to a persistent PostgreSQL database. The infrastructure is fully automated using a modern DevOps CI/CD toolchain, deploying directly to an AWS EC2 instance upon every push to the main branch.

## Technology Stack
* **Application Framework:** FastAPI (Python)
* **Database:** PostgreSQL 15 (with Docker volume persistence)
* **ORM:** SQLAlchemy 2.0
* **Containerization:** Docker & Docker Compose (Multi-stage builds)
* **Continuous Integration (CI):** GitHub Actions (Flake8 Linting & Pytest)
* **Continuous Deployment (CD):** GitHub Actions (Remote SSH to AWS EC2)
* **Cloud Infrastructure:** Ubuntu Server 24.04 LTS (AWS EC2)

## Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/aatirraza/2212277-devops-project.git](https://github.com/aatirraza/2212277-devops-project.git)
   cd 2212277-devops-project
