# Todo List App

## Running the App

Application can be built and run using Docker and Docker Compose:

To build:
```bash
docker-compose build
```
To run:
```bash
docker-compose up -d
```

The `docker-compose.yaml` configuration requires the following environment variables to be set for the app to run correctly: 
- `AUTHOR` - set this to be your Docker Hub account
- `VERSION` - defines the tag for the Docker image
- `SECRET_KEY` - required for CSRF protection provided by WTForms

The `DATABASE_URI` has been set to `sqlite:///data.db` for simplicity's sake.

## Using the Jenkinsfile

The `Jenkinsfile` defines the pipeline job configuration. It is found at [jenkins/Jenkinsfile](jenkins/Jenkinsfile).

There are a number of variables set in the `environment{}`.

The following are set by default:
- `VERSION` is set to be `1.${BUILD_ID}`, where `BUILD_ID` is the Jenkins job's build number
- `TEST_DATABASE_URI` has been set to `sqlite:///data.db` and is used by the unit and integration tests
- `TEST_SECRET_KEY` is set to `test` and is used by the integration tests
- `CHROMEDRIVER_PATH` defines where the `chromedriver` will be installed and is set to `/home/jenkins/chromedriver`

And these need to be defined using Jenkins Credentials:
- `AUTHOR` should be set to your Docker Hub username
- `SECRET_KEY` should be set to a secure key

The instructions for each pipeline step are defined in separate `bash` scripts. The testing stage requires the use of `sudo` commands to install the required software dependencies, and so the `jenkins` user must be given `sudo` privileges to run the following:

```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv unzip chromium-browser
```

Post-build actions are defined in the `post{}` section of the pipeline. They publish the reports produced by the `test.sh` script and require JUnit and Cobertura plugins to be installed on your Jenkins instance (JUnit tends to be installed by default).

The `Jenkinsfile` does not currently install Docker or Docker Compose. As such, these must be installed manually. Getting Jenkins to push to Docker Hub requires the `jenkins` user to have performed `docker login`.
