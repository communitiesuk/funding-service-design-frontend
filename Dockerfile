ARG BASE_IMAGE_TAG="3.17.0-rc.828"
FROM ghcr.io/xgovformbuilder/digital-form-builder-runner:$BASE_IMAGE_TAG as base
ARG FORMS_DIR="forms-v3"
WORKDIR /usr/src/app
RUN rm -r runner/dist/server/forms && rm -r runner/src && rm -r runner/test
COPY form_jsons/public/* runner/dist/server/forms/
WORKDIR /usr/src/app
RUN rm runner/src/server/plugins/crumb.ts
COPY xform_overwrites/crumb.ts runner/src/server/plugins/crumb.ts

FROM base as app
WORKDIR /usr/src/app
USER root
RUN deluser --remove-home appuser && \
 addgroup -g 1001 appuser && \
 adduser -S -u 1001 -G appuser appuser
USER appuser

EXPOSE 3009

ENV NODE_ENV=production
ENV API_ENV=production
ENV PREVIEW_MODE=false
USER 1001
CMD [ "yarn", "runner", "start"]
