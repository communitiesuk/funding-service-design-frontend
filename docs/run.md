# Run Service

Then run:

    flask run

A local dev server will be created on

    http://127.0.0.1:5000/

This is configurable in .flaskenv

You should see the following:

<img src="https://user-images.githubusercontent.com/65361824/153576751-9cb8799f-4737-40c4-9f6f-d38d4bcc188e.png" alt="landing-page" width="300"/>

### Build with Paketo

[Pack](https://buildpacks.io/docs/tools/pack/cli/pack_build/)

[Paketo buildpacks](https://paketo.io/)

```pack build <name your image> --builder paketobuildpacks/builder:base```

Example:

```
[~/work/repos/funding-service-design-frontend] pack build paketo-demofsd-app --builder paketobuildpacks/builder:base
***
Successfully built image paketo-demofsd-app
```

You can then use that image with docker to run a container

```
docker run -d -p 8080:8080 --env PORT=8080 --env FLASK_ENV=dev [envs] paketo-demofsd-app
```

`envs` needs to include values for each of:
RSA256_PUBLIC_KEY_BASE64
AUTHENTICATOR_HOST
ACCOUNT_STORE_API_HOST
APPLICATION_STORE_API_HOST
NOTIFICATION_SERVICE_HOST
APPLICANT_FRONTEND_HOST
FORMS_SERVICE_PUBLIC_HOST
FORMS_SERVICE_PRIVATE_HOST
FUND_STORE_API_HOST
SENTRY_DSN
COOKIE_DOMAIN
GITHUB_SHA

```
docker ps -a
CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS                    PORTS                    NAMES
42633142c619   paketo-demofsd-app          "/cnb/process/web"       8 seconds ago    Up 7 seconds              0.0.0.0:8080->8080/tcp   peaceful_knuth
```
