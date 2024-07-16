# CALCULATE:PROPOSAL:DATETIME

This GitHub Action composite is used to calculate the proposal height by datetime for a Cosmos SDK network using the provided RPC URL and average block time.

## Inputs

### `upgrade_date`

**Optional** The date and time for the upgrade in the format `MM/DD/YYYY HH:MM`. Example: `6/28/2023 14:30`. Default: `10`.

### `rpc_url`

**Required** The Cosmos SDK RPC URL you want to use.

### `average_block_time`

**Required** The calculated average block time of the network.

## Example Usage

To use this composite action in your GitHub workflow, add the following steps:

```yaml
name: "CALCULATE:PROPOSAL:DATETIME"
description: "Calculate the Proposal height by datetime."
inputs:
  upgrade_date:
    description: "ex. 6/28/2023 14:30"
    default: "10"
    required: false
  rpc_url:
    description: "the cosmosSDK RPC URL you want to use."
    required: true
  average_block_time:
    description: "The calculated average block time of the network."
    required: true
runs:
  using: "composite"
  steps:
    - uses: actions/checkout@v3
      with:
        repository: gzukel/github_actions_composites
        path: github_action_composites

    - uses: actions/setup-python@v4
      with:
        python-version: 'pypy3.10'

    - name: "REQUIREMENTS:INSTALL"
      shell: bash
      working-directory: "github_action_composites/cosmossdk_calculate_future_upgrade_height/"
      run: |
        pip install -r requirements.txt

    - name: "EXECUTE:CALCULATION"
      shell: bash
      working-directory: "github_action_composites/cosmossdk_calculate_future_upgrade_height/"
      env:
        RPC_URL: "${{ inputs.rpc_url }}"
        UPGRADE_DATE: "${{ inputs.upgrade_date }}"
        AVERAGE_BLOCK_TIME: "${{ inputs.average_block_time }}"
      run: |
        python calculate_upgrade_date.py
```

## Composite Action Details

This composite action performs the following steps:

1. **Checkout Repository**: Uses `actions/checkout@v3` to checkout the repository containing the composite action.
2. **Setup Python**: Uses `actions/setup-python@v4` to set up Python with the specified version `pypy3.10`.
3. **Install Requirements**: Installs the required Python packages from `requirements.txt` in the specified working directory.
4. **Execute Calculation**: Runs the Python script to calculate the future upgrade height and sets it as an environment variable.

## Notes

- Ensure that your GitHub workflow has the necessary permissions to interact with the Cosmos SDK network.
- Provide valid values for the `upgrade_date`, `rpc_url`, and `average_block_time` inputs when triggering the workflow.

## Outputs

The action sets an environment variable `UPGRADE_HEIGHT` with the calculated proposal height.

## Example Workflow

Here is an example of how to use this composite action in a workflow:

```yaml
name: Calculate Proposal Height

on:
  workflow_dispatch:
    inputs:
      upgrade_date:
        description: "The date and time for the upgrade. Format: MM/DD/YYYY HH:MM"
        default: "6/28/2023 14:30"
      rpc_url:
        description: "The Cosmos SDK RPC URL you want to use."
        required: true
      average_block_time:
        description: "The calculated average block time of the network."
        required: true

jobs:
  calculate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Calculate Proposal Height by Datetime
        uses: gzukel/github_action_composites/cosmossdk_calculate_future_upgrade_height@main
        with:
          upgrade_date: ${{ inputs.upgrade_date }}
          rpc_url: ${{ inputs.rpc_url }}
          average_block_time: ${{ inputs.average_block_time }}
```

