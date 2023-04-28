IAM SETTING
Store Docker container images in Artifact Registry

if you are using Local shell, ensure docker and gcloud CLI are installed.  
if docker not is installed, to install: 
https://docs.docker.com/engine/install/ubuntu/ 
if gcloud CLI is not installed, to install: 


Create a Docker Repository in Google Cloud Artifact Registry

gcloud artifacts repositories create my-docker-repo --repository-format=docker \
--location=us-central1 --description="Docker repository"

You can change repository name and location 

Configure Docker to use the Google Cloud CLI to authenticate requests to Artifact Registry.

burayı düzenle 
docker build -t us-central1-docker.pkg.dev/erudite-flag-384915/my-docker-repo/dbt-case-study-img2:v01 .

gcloud auth configure-docker us-central1-docker.pkg.dev

docker push us-central1-docker.pkg.dev/erudite-flag-384915/my-docker-repo/dbt-case-study-img2:v01

gcloud run deploy dbt-commands \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --image us-central1-docker.pkg.dev/erudite-flag-384915/my-docker-repo/dbt-case-study-img:v1