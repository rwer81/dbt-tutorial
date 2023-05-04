# Deploy DBT Docker to Artifact Registry and  Run with Cloud Run as a REST API

# Deployment

If you don't have, install the gcloud CLI from https://cloud.google.com/sdk/docs/install and git from https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

#### Open command line and type to pull the repo.:

- `git clone https://github.com/rwer81/dbt-tutorial.git`

- `cd dbt_tutorial`

#### Using command line

- `gcloud auth login`

- `gcloud config set project <your_gcp_project_name>`

#### Set env
- `export PROJECT_ID=$(gcloud config get-value project)`

- `export GCP_REGION="<your_region>" `


#### Enable apis

- <pre>gcloud services enable compute.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com 
    storage.googleapis.com \
    run.googleapis.com</pre>

#### Create a Docker Repository in Google Cloud Artifact Registry
* You can change repo name

`export REPO_NAME=dbt-docker-repo`

<pre>gcloud artifacts repositories create $REPO_NAME \
    --repository-format=docker \
    --location=$GCP_REGION \
    --description="Docker repository"</pre>

## Option 1 - Set up with command by command

#### Configure auth
`gcloud auth configure-docker ${GCP_REGION}-docker.pkg.dev`

### BUILD DOCKER 
* You can change image, tag and service name

`export IMAGE_NAME="dbt-tutorial-img"`

`export TAG_NAME="v1"`

`export SERVICE_NAME="dbt-tutorial-run-service"`


#### Build and push image to artifact registry 
<pre>gcloud builds submit \
    --tag ${GCP_REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:${TAG_NAME}</pre>

#### Deploy app to Cloud Run
* You can change max instance value

<pre>gcloud run deploy $SERVICE_NAME \
    --platform managed \
    --region $GCP_REGION \
    --allow-unauthenticated \
    --max-instances 2 \
    --image ${GCP_REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:${TAG_NAME}</pre>

## Option 2- Set up from cloudbuild.yaml file (easier and includes additional tests)
  - Open clouduild.yaml file modify 'substitutions' sections in the end of the file.
  - Execute `gcloud builds submit --region $GCP_REGION --project $PROJECT_ID --config cloudbuild.yaml`

## Test
`export SERVICE_NAME="dbt-tutorial-run-service"`

#### Confirm service is running
`gcloud run services list \
    --platform managed \
    --region $GCP_REGION`

#### Test URL
`export SVC_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $GCP_REGION --format="value(status.url)")`

`curl -X GET $SVC_URL`

_IAM Notes:_

_If you encounter permission issues, Cloud Build(xxxx@cloudbuild.gserviceaccount.com service account) requires Cloud Run Admin, Service Account User, Storage Viewer, Artifact Registry Writer permissions._

# Usage

POST

`curl -d '{"command": "dbt list"}' -H "Content-Type: application/json" -X POST https://your_service_url/run_command`

GET

`curl -X GET https://your_service_url`
