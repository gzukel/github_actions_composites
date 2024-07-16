Here is the README.md content for your GitHub Action:

```markdown
# WAIT:FOR:KUBERNETES:ROLLOUT

This GitHub Action checks and waits for the rollout status of a Kubernetes pod and fails if not successful.

## Inputs

### `namespace`

**Required** The namespace of the Kubernetes deployment.

### `deployment`

**Required** The name of the Kubernetes deployment.

## Example Usage

To use this composite action in your GitHub workflow, add the following steps:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Wait for Kubernetes Pod Rollout
        uses: gzukel/github_actions_composites/kubernetes_deployment_rollout_status@main
        with:
          namespace: 'your-namespace'
          deployment: 'your-deployment-name'
```

## Composite Action Details

This composite action performs the following steps:

1. **CHECKOUT:REPOSITORY**: Checks out your repository using `actions/checkout@v4`.
2. **INSTALL:KUBECTL**: Installs the latest version of `kubectl` using `azure/setup-kubectl@v3`.
3. **WAIT:FOR:ROLLOUT**: Waits for the rollout status of the specified Kubernetes deployment in the given namespace and fails if the rollout is not successful.

## Notes

- Ensure that your GitHub workflow has the necessary permissions to interact with your Kubernetes cluster.
- Make sure to provide valid values for the `namespace` and `deployment` inputs.
```

This README provides clear instructions on how to use the composite action, including the necessary inputs and an example workflow configuration.