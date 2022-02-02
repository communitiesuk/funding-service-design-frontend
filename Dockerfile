# syntax=docker/dockerfile:1
FROM ghcr.io/xgovformbuilder/digital-form-builder-runner:latest
COPY json-forms/* /app/runner/dist/server/forms
CMD [ "yarn", "runner", "start"]