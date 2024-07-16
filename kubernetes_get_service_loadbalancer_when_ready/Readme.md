### GitHub Action: Wait for External IP and Save as Artifact

This GitHub Action waits for an external IP to be assigned to a Kubernetes service and saves it as an artifact.

#### Author
Grant Zukel

---

### Inputs

- **service_name**: The name of the Kubernetes service. (**Required**)
- **namespace**: The namespace of the Kubernetes service. (Default: `default`)
- **timeout**: The timeout in seconds to wait for the external IP. (Default: `600`)
- **sleep_interval**: The interval in seconds between checks for the external IP. (Default: `10`)

---

### Outputs

- **SERVICE_EXTERNAL_IP**: The external IP assigned to the Kubernetes service.

---

### Usage Example

To use this composite action in your GitHub workflow, add the following step:

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
      - name: "Wait for External IP"
        uses: gzukel/github_actions_composites/kubernetes_get_service_loadbalancer_when_ready@main
        with:
          service_name: 'your-service-name'
          namespace: 'default'
          timeout: 600
          sleep_interval: 10

      - name: "Use External IP"
        run: echo "External IP is ${{ steps.wait-for-ip.outputs.SERVICE_EXTERNAL_IP }}"
```

This composite action will wait for an external IP to be assigned to the specified Kubernetes service and save it as an artifact.

---