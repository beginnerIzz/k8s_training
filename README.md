# k8s_training

PHASE 1.1-

To achieve familiarity with Kubernetes, we start by deploying two types of deployment which are Postgres for the database and Flask for web-server

All deployment will be deployed on "Minikube" as this is the best way to interect with kubenetes cluster as it will not require any resources on Cloud and fully dependant on local resources

Objective: 

1. Deploy postgres and add data into it
2. Access the data through web-server (Flask)


To connect with the postgres database
   kubectl exec -it (pod-name) -- psql -U postgres


Phase 1.2-

Once successfully deploy Postgres and Flask, we are trying to add Prometheus-Server and Graphana to monitor our resources with the basic metrics provided by Prometheus

As we get familiar with the deployment process of pulling image and clusters configuration through YAML files, we can skip these two components manual configuration and utilise helm-chart existing template  

Objective: 

1.  Deploy Prometheus-Server and Graphana
2.  Utilise helm-chart template

Phase 1.3-

While everthing run as intended locally, we start to push all our working project to Git. Hence, we can start to use Flux in our system

Flux is a GitOps tool that continuously syncs our Kubernetes cluster with the desired state defined in our Git repository

Objective: 

1. Install Flux
2. Ensure automated and consistent Kubernetes deployments directly from our Git repository, ensuring reliable, version-controlled infrastructure changes

Phase 1.4-

Instead of deploying a services by config kubenetes manifest, we are trying to package all of relevant services using helm-charts and deploy everything at once

1. Create a template to deploy services using helm-charts
