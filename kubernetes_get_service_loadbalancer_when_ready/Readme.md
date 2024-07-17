### GitHub Action: Wait for External IP and Save as Artifact

This GitHub Action waits for an external IP to be assigned to a Kubernetes service or ingress and saves it as an artifact.

#### Author
Grant Zukel

---

### Inputs

- **resource_type**: The type of Kubernetes resource (`service` or `ingress`). (**Required**)
- **resource_name**: The name of the Kubernetes resource. (**Required**)
- **namespace**: The namespace of the Kubernetes resource. (Default: `default`)
- **timeout**: The timeout in seconds to wait for the external IP. (Default: `600`)
- **sleep_interval**: The interval in seconds between checks for the external IP. (Default: `10`)
- **kubeconfig_location**: The location of the Kubernetes config file. (**Required**)

---

### Outputs

- **EXTERNAL_IP**: The external IP assigned to the Kubernetes resource.

---

### Usage Example

To use this composite action in your GitHub workflow, add the following steps:

```yaml
name: Wait for External IP and Save as Artifact

on:
  push:
    branches:
      - main

jobs:
  wait-for-ip:
    runs-on: ubuntu-latest

    steps:
      - name: "Checkout Repository"
        uses: actions/checkout@v4

      - name: "Wait for External IP"
        uses: gzukel/github_actions_composites/wait_for_external_ip_and_save_as_artifact@main
        with:
          resource_type: 'service' # or 'ingress'
          resource_name: 'your-resource-name'
          namespace: 'default'
          timeout: 600
          sleep_interval: 10
          kubeconfig_location: '/path/to/your/kubeconfig'

      - name: "Use External IP"
        run: echo "External IP is ${{ steps.wait-for-ip.outputs.EXTERNAL_IP }}"
```

This composite action will wait for an external IP to be assigned to the specified Kubernetes service or ingress and save it as an artifact.

---

### GitHub Action YAML

```yaml
name: 'Wait for External IP and Save as Artifact'
description: 'Waits for an external IP to be assigned to a Kubernetes service or ingress and saves it as an artifact.'
author: 'Grant Zukel'
branding:
  icon: cloud
  color: gray-dark
inputs:
  resource_type:
    description: 'The type of Kubernetes resource (service or ingress).'
    required: true
  resource_name:
    description: 'The name of the Kubernetes resource (service or ingress).'
    required: true
  namespace:
    description: 'The namespace of the Kubernetes resource.'
    required: true
    default: 'default'
  timeout:
    description: 'The timeout in seconds to wait for the external IP.'
    required: true
    default: 600
  sleep_interval:
    description: 'The interval in seconds between checks for the external IP.'
    required: true
    default: 10
  kubeconfig_location:
    description: 'The location of the Kubernetes config file.'
    required: true
runs:
  env:
    KUBECONFIG: "${{ inputs.kubeconfig_location }}"
  using: 'composite'
  steps:
    - name: "CHECKOUT:REPOSITORY"
      uses: actions/checkout@v4

    - name: "INSTALL:KUBECTL"
      uses: azure/setup-kubectl@v3
      with:
        version: 'latest'

    - name: "WAIT:FOR:EXTERNAL:IP"
      id: wait-for-ip
      run: |
        RESOURCE_TYPE="${{ inputs.resource_type }}"
        RESOURCE_NAME="${{ inputs.resource_name }}"
        NAMESPACE="${{ inputs.namespace }}"
        TIMEOUT=${{ inputs.timeout }}
        SLEEP_INTERVAL=${{ inputs.sleep_interval }}
        EXTERNAL_IP=""

        end=$((SECONDS+TIMEOUT))
        while [ $SECONDS -lt $end ]; do
          if [ "$RESOURCE_TYPE" == "service" ]; then
            EXTERNAL_IP=$(kubectl get svc $RESOURCE_NAME -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
          elif [ "$RESOURCE_TYPE" == "ingress" ]; then
            EXTERNAL_IP=$(kubectl get ingress $RESOURCE_NAME -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
          else
            echo "Error: Unknown resource type $RESOURCE_TYPE"
            exit 1
          fi

          if [ -n "$EXTERNAL_IP" ]; then
            echo "External IP assigned: $EXTERNAL_IP"
            break
          fi

          echo "Waiting for external IP..."
          sleep $SLEEP_INTERVAL
        done

        if [ -z "$EXTERNAL_IP" ]; then
          echo "Error: Timed out waiting for external IP"
          exit 1
        fi

        echo "EXTERNAL_IP=$EXTERNAL_IP" >> ${GITHUB_ENV}
        echo $EXTERNAL_IP > EXTERNAL_IP.txt

    - name: "UPLOAD:ARTIFACT"
      uses: actions/upload-artifact@v2
      with:
        name: external-ip
        path: EXTERNAL_IP.txt
```