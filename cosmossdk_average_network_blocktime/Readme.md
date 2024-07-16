# CALCULATE:AVERAGE:NETWORK:BLOCKTIME

This GitHub Action composite is used for calculating the average block time of a Cosmos SDK network using the provided RPC URL.

## Inputs

### `avg_time_sample_size`

**Optional** The sample size of blocks you want to calculate your average over. Default: `10`.

### `rpc_url`

**Required** The Cosmos SDK RPC URL you want to use.

## Example Usage

To use this composite action in your GitHub workflow, add the following steps:

```yaml
name: "CALCULATE:AVERAGE:NETWORK:BLOCKTIME"
description: "This composite is used for calculating average block time of a cosmos sdk network using the rpc url."
inputs:
  avg_time_sample_size:
    description: "The sample size of blocks you want to calculate your average over."
    default: "10"
    required: false
  rpc_url:
    description: "The Cosmos SDK RPC URL you want to use."
    required: true
runs:
  using: "composite"
  steps:
    - uses: actions/checkout@v3
      with:
        repository: gzukel/github_action_composites
        path: github_action_composites

    - uses: actions/setup-python@v4
      with:
        python-version: 'pypy3.10'

    - name: "REQUIREMENTS:INSTALL"
      shell: bash
      working-directory: "github_action_composites/cosmossdk_average_network_blocktime/"
      run: |
        pip install -r requirements.txt

    - name: "EXECUTE:CALCULATION"
      shell: bash
      working-directory: "github_action_composites/cosmossdk_average_network_blocktime/"
      env:
        AVG_TIME_SAMPLE_SIZE: "${{ inputs.avg_time_sample_size }}"
        RPC_URL: "${{ inputs.rpc_url }}"
      run: |
        python calculate_average_block_time_to_environment_var.py
```

## Composite Action Details

This composite action performs the following steps:

1. **Checkout Repository**: Uses `actions/checkout@v3` to checkout the repository containing the composite action.
2. **Setup Python**: Uses `actions/setup-python@v4` to set up Python with the specified version `pypy3.10`.
3. **Install Requirements**: Installs the required Python packages from `requirements.txt` in the specified working directory.
4. **Execute Calculation**: Runs the Python script to calculate the average block time and sets it as an environment variable.

## Notes

- Ensure that your GitHub workflow has the necessary permissions to interact with the Cosmos SDK network.
- Provide valid values for the `avg_time_sample_size` and `rpc_url` inputs when triggering the workflow.

## Outputs

The action sets an environment variable `AVERAGE_BLOCK_TIME` with the calculated average block time.

## Example Workflow

Here is an example of how to use this composite action in a workflow:

```yaml
name: Calculate Average Block Time

on:
  workflow_dispatch:
    inputs:
      avg_time_sample_size:
        description: "The sample size of blocks you want to calculate your average over."
        default: "10"
      rpc_url:
        description: "The Cosmos SDK RPC URL you want to use."
        required: true

jobs:
  calculate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Calculate Average Block Time
        uses: gzukel/github_action_composites/cosmossdk_average_network_blocktime@main
        with:
          avg_time_sample_size: ${{ inputs.avg_time_sample_size }}
          rpc_url: ${{ inputs.rpc_url }}
```
