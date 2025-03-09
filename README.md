# msrv-vlm (Microservice VLM)

The goal of msrv-vlm is to have a simple service that can receive an image and a prompt, and return a response in a machine readable and structure format.

## Supports

Currently we only support Gemini and inputs as PNG. 

## Prerequisites

- Docker or Kubernetes (e.g., Minikube or a Kubernetes cluster)
- Poetry

## Building the Docker Image

To build the Docker image, run the following command in the project root directory:

```sh
docker build  --no-cache -t msrv-llm:0.0.1 .
```

## Running the Application with Docker

To run the application using Docker, use the following command:

```sh
docker run -p 5000:5000 msrv-llm:0.0.1
```

## Deploying the Application with Kubernetes


1. Apply the deployment file to your Kubernetes cluster:

    ```sh
    kubectl delete -f deployment.yaml
    
    kubectl apply -f deployment.yaml
    ```

2. Expose the deployment as a service:

    ```sh
    kubectl expose deployment msrv-vlm --type=LoadBalancer --port=5000
    ```

3. Get the external IP address of the service:

    ```sh
    kubectl get services
    ```

4. Access the application using the external IP address and port 5000.

## Example Usage

To use the client to upload an image and a prompt, run the following command:

```sh
python client.py icd1.png "is this radiology?" json 
```

Return will be likely : 

```json
{
    "answer": "no"
}
```

Example of JSON-LD:

```sh
python client.py icd1.png "is this radiology?" json-ld 
```

Return will be likely : 

```json-ld
{
    "@context": "http://schema.org",
    "@type": "ImageObject",
    "content": {s
        "@context": "https://schema.org",
        "@type": "ImageObject",
        "caption": "This is a histology image, not a radiology image."
    }
}
```