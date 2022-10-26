# Pipelines

## Frontend Python application
Deploy to Gov PaaS (`govcloud.yml`) - Builds, tests and deploys a simple python application to PaaS in Dev on every push, and Test if on main. Not triggerred on updates to the form_jsons folder.

## Form Runner
Build and Deploy Forms (`build-deploy-forms.yml`) - This builds the form runner (using `Dockerfile`) with the forms contained in `form_jsons` and deploys to dev (and if on `main`, to test as well).

Note that the form runner deployment is only triggered automatically on update of the contents of `form_jsons` in this repo, it does not automatically trigger on an update of the form runner image.

The form runner image is created from the [Digital Form Builder Repo](https://github.com/communitiesuk/digital-form-builder) using the pipeline [DLUHC Build and Publish](https://github.com/communitiesuk/digital-form-builder/actions/workflows/dluhc-build-and-publish.yml). This pushes a new image to https://github.com/communitiesuk/digital-form-builder/pkgs/container/digital-form-builder-dluhc-runner. Any tag from that docker repo can be used in the `Dockerfile` in this repo but if you just want to redeploy the forms with the latest version of the form runner you can manually trigger [Build and Deploy Formst](https://github.com/communitiesuk/funding-service-design-frontend/actions/workflows/build-deploy-forms.yml) in this repo which will just pickup the `latest` tag of the form runner.
