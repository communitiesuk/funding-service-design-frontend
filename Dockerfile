ARG BASE_IMAGE_TAG="fs-1322-add-expiry-and-accountid-invalidation"
FROM ghcr.io/communitiesuk/digital-form-builder-dluhc-runner:$BASE_IMAGE_TAG as base
ARG FORMS_DIR="forms-v3"
WORKDIR /usr/src/app
RUN rm -r runner/dist/server/forms && rm -r runner/src && rm -r runner/test
COPY ./form_jsons/public/* runner/dist/server/forms/
COPY ./form_jsons/config/* runner/config/
CMD [ "yarn", "runner", "build"]

FROM base as app
WORKDIR /usr/src/app
USER root
RUN deluser --remove-home appuser && \
 addgroup -g 1001 appuser && \
 adduser -S -u 1001 -G appuser appuser
USER appuser

EXPOSE 3009

ENV NODE_ENV=production
USER 1001
CMD [ "yarn", "runner", "start"]
