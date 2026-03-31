# Week 2 Submission - Task 1 & Task 2

## Project Structure

- `Task1/` → Single-container Flask app
- `Task2/` → Multi-container Flask + Redis app with Docker Compose

## Deliverables Checklist

- [ ] Screenshot of Task 1 app running locally
- [ ] Screenshot of Task 1 Dockerfile
- [ ] Screenshot of Task 1 image build logs
- [ ] Screenshot of running container with port mapping
- [ ] Screenshot of pushed Docker Hub image
- [ ] Docker Hub URL

## Docker Hub URL

Add your final URL here after pushing:

`https://hub.docker.com/r/YOUR_DOCKERHUB_USERNAME/my-docker-app`

## Short Explanation (8–10 lines)

1. The Docker image contains the Flask application code, Python runtime, and required libraries.
2. In Task 1, everything runs in one container, and port 5000 is mapped from container to host.
3. Docker networking allows isolated containers to communicate over a shared bridge network.
4. In Task 2, the Flask container reaches Redis using the service name `redis` as hostname.
5. Docker Compose automatically creates this internal network and attaches both services.
6. Redis stores state (`hits`) so the app can keep a shared counter across requests.
7. Containers are important because they make environments consistent across developer and server machines.
8. They start quickly, use fewer resources than full virtual machines, and simplify scaling.
9. Dockerfiles make builds reproducible, while Compose makes multi-service apps easy to run.
10. This improves reliability in development, testing, CI/CD, and production deployments.
