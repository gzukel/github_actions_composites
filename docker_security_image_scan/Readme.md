# ANCHORE:DOCKER:SCAN

**Author**: Grant Zukel

## Description

This GitHub Action composite performs a security scan on a Docker image using Anchore. The scan can be configured to fail the pipeline if vulnerabilities are found.

## Inputs

### `docker_image_name`

**Required** The name of the Docker image you want to scan.

### `fail_pipeline_on_fail`

**Optional** Whether to fail the pipeline if the scan finds vulnerabilities. Default: `true`.

## Example Usage

To use this composite action in your GitHub workflow, add the following steps:

```yaml
name: "Docker Security Scan"

on:
  push:
    branches:
      - main

jobs:
  scan:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Run Docker Security Scan
        uses: gzukel/github_actions_composite/docker_security_image_scan@main
        with:
          docker_image_name: "your-docker-image:latest"
          fail_pipeline_on_fail: "true"
```

## Composite Action Details

This composite action performs the following steps:

1. **Anchore Docker Image Scan**: Runs a security scan on the specified Docker image using Anchore's inline scan script. The action can be configured to fail the pipeline if vulnerabilities are found.

## Notes

- Ensure that your GitHub workflow has the necessary permissions to pull the Docker image.
- Provide valid values for the `docker_image_name` input.
- The `fail_pipeline_on_fail` input determines whether the pipeline should fail if the scan finds vulnerabilities. Set it to `true` to fail the pipeline or `false` to continue the pipeline regardless of the scan results.

## Example Workflow

Here is an example of how to use this composite action in a workflow:

```yaml
name: Docker Security Scan

on:
  workflow_dispatch:
    inputs:
      docker_image_name:
        description: "The name of the Docker image you want to scan."
        required: true
      fail_pipeline_on_fail:
        description: "Fail the pipeline if the scan finds vulnerabilities."
        default: "true"

jobs:
  scan:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Run Docker Security Scan
        uses: gzukel/github_actions_composite/docker_security_image_scan@main
        with:
          docker_image_name: ${{ inputs.docker_image_name }}
          fail_pipeline_on_fail: ${{ inputs.fail_pipeline_on_fail }}
```
