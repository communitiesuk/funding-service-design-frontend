# syntax=docker/dockerfile:1
FROM ghcr.io/xgovformbuilder/digital-form-builder-runner:latest
COPY form_jsons/public/* /app/runner/src/server/forms