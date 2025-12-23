# Plan de acción CVE (HIGH/CRITICAL) - Imagen: etl-app:1.0.0 @ sha256:a0cc9be8163a3f62645e780dd6ed513f8be3b0dc5ee40a52b04b1c3ca50a4d21

- Hallazgos clave:
  - CVE-2024-12345 en openssl (1.1.1w) - Severidad: HIGH - Componente: sistema
  - CVE-2025-67890 en python (3.12.0) - Severidad: CRITICAL - Componente: intérprete

- Remediación técnica:
  1) Actualizar base image a python:3.12.2-slim (ETA: 2026-01-10).
  2) Fijar versión de openssl a >= 1.1.1x donde el CVE está parchado.
  3) Ejecutar re-build y re-scan. Adjuntar nuevo SBOM y scan.

- Excepción temporal (si aplica):
  - Justificación: El CVE de openssl no es explotable en este contexto porque no se expone ningún servicio TLS directo.
  - Ticket: SEC-2025-001 - Revisión: 2026-01-15

- Criterios de cierre:
  - Trivy/Grype sin HIGH/CRITICAL en imagen final.
  - Documentación de digest nuevo y evidencia de remediación.
