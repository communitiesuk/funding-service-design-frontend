# Pipelines

## Frontend Python application
Deploy to Gov PaaS (`govcloud.yml`) - Builds, tests and deploys the python frontend application to PaaS in Dev on every push, and Test if on main. Not triggerred on updates to the form_jsons folder.

## Form Runner
There are 2 docker images involved in creating our deployed image of the form runner.

[Funding Service Design Frontend Runner](https://github.com/communitiesuk/funding-service-design-frontend/pkgs/container/funding-service-design-frontend%2Frunner)
This is the image we deploy to PaaS, built in this repo. It uses the [Dockerfile](https://github.com/communitiesuk/funding-service-design-frontend/blob/main/Dockerfile) to create the image, which takes the `Digital Form Builder DLUHC Runner` image (see below) as the base image, and imports the `form_jsons` from this repo over the top to produce our custom form runner image.

This image is built, pushed and deployed by [Build and Deploy Forms](https://github.com/communitiesuk/funding-service-design-frontend/actions/workflows/build-deploy-forms.yml). That workflow is triggered from any push to `form_jsons` in this repo, it does not automatically trigger on an update of the form runner base image.

[Digital Form Builder DLUHC Runner](https://github.com/communitiesuk/digital-form-builder/pkgs/container/digital-form-builder-dluhc-runner)
This is the image created from our fork of the form runner at https://github.com/communitiesuk/digital-form-builder. It is the base image of what is deployed to PaaS (see above) but does not contain our form_jsons.

Every push of our fork creates a new image, tagged with the commit ID. Any of these can be used in `Dockerfile` in the frontend repo to test branch changes. Pushes to main of our fork create a new image tagged with `latest`. Pushes of our fork do not automatically redeploy the form runner with our forms - to do this you must manually trigger [Build and Deploy Forms](https://github.com/communitiesuk/funding-service-design-frontend/actions/workflows/build-deploy-forms.yml)
