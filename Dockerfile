ARG BASE_IMAGE_TAG="3.17.0-rc.828"
FROM ghcr.io/xgovformbuilder/digital-form-builder-runner:$BASE_IMAGE_TAG as base
ARG FORMS_DIR="forms-v3"
WORKDIR /usr/src/app
RUN rm -r runner/dist/server/forms && rm -r runner/src && rm -r runner/test
COPY json-forms/* /app/runner/dist/server/forms
# COPY runner/src/server/$FORMS_DIR runner/dist/server/forms
# COPY runner/src/server/views/ runner/dist/server/views/

FROM base as app
WORKDIR /usr/src/app
USER root
RUN deluser --remove-home appuser && \
 addgroup -g 1001 appuser && \
 adduser -S -u 1001 -G appuser appuser
USER appuser

EXPOSE 3009

USER 1001
PRIVACY_POLICY_URL="https://www.gov.uk/government/publications/fcdo-privacy-notice-consular-services-in-the-uk-and-at-british-embassies-high-commissions-and-consulates-overseas/foreign-commonwealth-development-office-privacy-notice-consular-services-in-the-uk-and-missions-overseas"
CMD [ "yarn", "runner", "start"]