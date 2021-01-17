# Todo List App

## Running the App

Application can be built and run using Docker and Docker Compose:

To build:
```
docker-compose build
```
To run:
```
docker-compose up -d
```

The `docker-compose.yaml` configuration requires the following environment variables to be set for the app to run correctly: 
- `AUTHOR` - set this to be your Docker Hub account
- `VERSION` - defines the tag for the Docker image
- `SECRET_KEY` - required for CSRF protection provided by WTForms

The `DATABASE_URI` has been set to `sqlite:///data.db` for simplicity's sake.

## Using the Jenkinsfile

The `Jenkinsfile` defines the pipeline job configuration. It is found at [jenkins/Jenkinsfile](jenkins/Jenkinsfile).

The variables set in `environment{}` determine the following:
- `VERSION` is set to be `1.${BUILD_ID}`, where `BUILD_ID` is the Jenkins job's build number
- `AUTHOR` is set to be `htrvolker`, but should be set to your Docker Hub username
  - Getting Jenkins to push to Docker Hub requires the `jenkins` user to `docker login`
- `TEST_DATABASE_URI` has been set to `sqlite:///data.db` and is used by the unit and integration tests
- `TEST_SECRET_KEY` is set to `test` and is used by the integration tests
- `CHROMEDRIVER_PATH` defines where the `chromedriver` will be installed and is set to `/home/jenkins/chromedriver`
- `DB_PASSWORD` and `SECRET_KEY` are set using Jenkins Credentials, and so need to be set on your Jenkins build server

The instructions for each pipeline step are defined in separate `bash` scripts.

Post-build actions are defined in the `post{}` section of the pipeline. They publish the reports produced by the `test.sh` script and require JUnit and Cobertura to be installed on your Jenkins instance.
