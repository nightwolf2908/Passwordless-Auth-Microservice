# Passwordless Intelligent Authentication Architecture

Backend: ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F27?style=for-the-badge&logo=python&logoColor=white)
Frontend: ![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
Infraestructura: ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white) ![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
Automatización: ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white) ![Ruff](https://img.shields.io/badge/Ruff-D7FF64?style=for-the-badge&logo=ruff&logoColor=black)

---

## 📈 Estado del Proyecto

A continuación se muestra el estado actual de la integración continua gestionada de forma automática por servidores remotos:

[![CI/CD Pipeline](https://github.com/TU_USUARIO_DE_GITHUB/Passwordless-Auth-Microservice/actions/workflows/ci-cd.yml/badge.flow.svg)](https://github.com/nightwolf2908/Passwordless-Auth-Microservice/actions)

---

## 📋 Descripción del Sistema

Este repositorio contiene una arquitectura desacoplada basada en microservicios para la gestión de autenticación síncrona/asíncrona **sin contraseñas (Passwordless)**. El sistema integra un Frontend inteligente capaz de determinar si un usuario requiere un flujo de registro completo o de inicio de sesión directo evaluando el estado de la infraestructura en caliente.

El stack de desarrollo se ejecuta de manera estrictamente aislada en contenedores, previniendo el consumo innecesario de almacenamiento local y garantizando la portabilidad del entorno.

### Componentes Clave de la Arquitectura:
* **Frontend (Nginx):** Single Page Application estructurada en Vanilla JS que optimiza las transiciones de estados de formularios reactivos y consume endpoints asíncronos mediante Fetch API.
* **API Gateway (FastAPI):** Backend de alta velocidad encargado de la lógica de enrutamiento, asignación de hashes temporales y persistencia dual.
* **Caché Volátil (Redis):** Manejo estricto de códigos OTP (One-Time Password) efímeros con políticas automáticas de expiración (TTL de 300 segundos).
* **Almacenamiento Persistente (PostgreSQL):** Base de datos relacional para el resguardo e indexación definitiva de identidades validadas.

---

## 🛠️ Requisitos e Instalación

Al estar completamente containerizado, el único requisito para desplegar el ecosistema completo en tu máquina local es disponer de **Docker** y **Docker Compose**.

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TU_USUARIO_DE_GITHUB/Passwordless-Auth-Microservice.git](https://github.com/TU_USUARIO_DE_GITHUB/Passwordless-Auth-Microservice.git)
   cd Passwordless-Auth-Microservice
Levantar la arquitectura completa:

Bash
docker compose up --build
Acceder a los servicios:

Frontend Interactivo: http://localhost:80 0 http://localhost

Documentación Interactiva de la API (Swagger): http://localhost:8000/docs

🤖 Pipeline de CI/CD (DevOps)
El proyecto incluye un flujo de integración continua automatizado por medio de GitHub Actions (.github/workflows/ci-cd.yml) estructurado en las siguientes fases jerárquicas:

Etapa de Calidad de Código: Inspección estricta de sintaxis, imports muertos y formato mediante el linter ultra-veloz Ruff. Cualquier desviación detiene el pipeline inmediatamente.

Etapa de Construcción: Pruebas automatizadas de compilación de imágenes Docker (Dockerfile) tanto para el entorno de Python como el de Nginx en entornos aislados de Ubuntu.