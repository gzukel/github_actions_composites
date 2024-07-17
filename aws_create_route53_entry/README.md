Sure, here's the updated README for your composite action with the addition of handling `AWS_SESSION_TOKEN` for assuming roles:

```markdown
# UPSERT:ROUTE53:DOMAIN

This GitHub Action checks the provided `input_address` to determine if it should be an A or CNAME record and then upserts the DNS record in AWS Route 53.

## Inputs

### `hostname`

**Required** The hostname you want to update. Default: `hostname.root_domain.com`

### `input_address`

**Required** The IP or CNAME you want to add to the hostname. Default: `load_balancer_user.com`

### Using Static AWS Keys

```yaml
name: "UPSERT:ROUTE53:DOMAIN"

on:
  workflow_dispatch:
    inputs:
      hostname:
        description: Hostname you want to update.
        default: hostname.root_domain.com
      input_address:
        description: The IP or CNAME you want to add to the hostname.
        default: load_balancer_user.com

jobs:
  upsert_route53:
    name: "UPSERT:ROUTE53:DOMAIN"
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        os: [ 'ubuntu-latest' ]

    steps:
      - uses: actions/checkout@v4

      - name: Determine Record Type
        id: determine_record_type
        run: |
          input_address="${{ github.event.inputs.input_address }}"
          if [[ "$input_address" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo "::set-output name=record_type::A"
          else
            echo "::set-output name=record_type::CNAME"
          fi

      - name: "UPSERT:RECORD:ROUTE53"
        uses: gzukel/github_actions_composites_aws_create_route53_entry@main
        with:
          aws_access_key_id: "${{ secrets.AWS_ACCESS_KEY_ID }}"
          aws_secret_access_key: "${{ secrets.AWS_SECRET_ACCESS_KEY }}"
          aws_route53_hosted_zone_id: "${{ secrets.ROUTE53_ZONEID }}"
          aws_route53_rr_action: "UPSERT"
          aws_route53_rr_name: "${{ github.event.inputs.hostname }}"
          aws_route53_rr_type: "${{ steps.determine_record_type.outputs.record_type }}"
          aws_route53_rr_ttl: "60"
          aws_route53_rr_value: "${{ github.event.inputs.input_address }}"
```

### Using IAM Role with OIDC

You can utilize roles to do this if you are running your runners and you add a step to assume role and pass in the temporary credentials of the assumed role to the step. Or you can utilize OIDC to assume a role and pass in the temporary credentials created from the assumed role to the step.

```yaml
name: "UPSERT:ROUTE53:DOMAIN"

on:
  workflow_dispatch:
    inputs:
      hostname:
        description: Hostname you want to update.
        default: hostname.root_domain.com
      input_address:
        description: The IP or CNAME you want to add to the hostname.
        default: load_balancer_user.com

jobs:
  upsert_route53:
    name: "UPSERT:ROUTE53:DOMAIN"
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        os: [ 'ubuntu-latest' ]

    steps:
      - uses: actions/checkout@v4

      - name: Assume Role
        id: assume_role
        uses: aws-actions/configure-aws-credentials@v1
        with:
          role-to-assume: arn:aws:iam::123456789012:role/my-github-actions-role
          role-session-name: GitHubActions
          aws-region: us-east-1

      - name: Determine Record Type
        id: determine_record_type
        run: |
          input_address="${{ github.event.inputs.input_address }}"
          if [[ "$input_address" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo "::set-output name=record_type::A"
          else
            echo "::set-output name=record_type::CNAME"
          fi

      - name: "UPSERT:RECORD:ROUTE53"
        uses: gzukel/github_actions_composites_aws_create_route53_entry@main
        with:
          aws_access_key_id: "${{ steps.assume_role.outputs.aws_access_key_id }}"
          aws_secret_access_key: "${{ steps.assume_role.outputs.aws_secret_access_key }}"
          aws_session_token: "${{ steps.assume_role.outputs.aws_session_token }}"
          aws_route53_hosted_zone_id: "${{ secrets.ROUTE53_ZONEID }}"
          aws_route53_rr_action: "UPSERT"
          aws_route53_rr_name: "${{ github.event.inputs.hostname }}"
          aws_route53_rr_type: "${{ steps.determine_record_type.outputs.record_type }}"
          aws_route53_rr_ttl: "60"
          aws_route53_rr_value: "${{ github.event.inputs.input_address }}"
```

## Composite Action Details

This composite action performs the following steps:

1. **Determine Record Type**: This step checks if the provided `input_address` is an IP address (A record) or a domain name (CNAME record) and sets the `record_type` accordingly.
2. **UPSERT:RECORD:ROUTE53**: Uses the determined `record_type` to upsert the DNS record in AWS Route 53.

## Notes

- Ensure that your GitHub workflow has the necessary permissions to interact with your AWS account and Route 53.
- Store your AWS credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) and Route 53 hosted zone ID (`ROUTE53_ZONEID`) as secrets in your GitHub repository settings if you are using AWS keys.
- Provide valid values for the `hostname` and `input_address` inputs when triggering the workflow.

## Secrets

- **AWS_ACCESS_KEY_ID**: Your AWS access key ID.
- **AWS_SECRET_ACCESS_KEY**: Your AWS secret access key.
- **ROUTE53_ZONEID**: The hosted zone ID for your Route 53 configuration.

## Using IAM Roles

You can also configure your GitHub Actions workflow to assume an IAM role using OIDC or by using an assume role step. This avoids the need to store AWS keys directly in your repository.

### Using OIDC to Assume a Role

Refer to the [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html) for more details on setting up OIDC for your GitHub Actions.

### Example Workflow with OIDC

```yaml
name: "UPSERT:ROUTE53:DOMAIN"

on:
  workflow_dispatch:
    inputs:
      hostname:
        description: Hostname you want to update.
        default: hostname.root_domain.com
      input_address:
        description: The IP or CNAME you want to add to the hostname.
        default: load_balancer_user.com

jobs:
  upsert_route53:
    name: "UPSERT:ROUTE53:DOMAIN"
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        os: [ 'ubuntu-latest' ]

    steps:
      - uses: actions/checkout@v4

      - name: Assume Role
        id: assume_role
        uses: aws-actions/configure-aws-credentials@v1
        with:
          role-to-assume: arn:aws:iam::123456789012:role/my-github-actions-role
          role-session-name: GitHubActions
          aws-region: us-east-1

      - name: Determine Record Type
        id: determine_record_type
        run: |
          input_address="${{ github.event.inputs.input_address }}"
          if [[ "$input_address" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo "::set-output name=record_type::A"
          else
            echo "::set-output name=record_type::CNAME"
          fi

      - name: "UPSERT:RECORD:ROUTE53"
        uses: gzukel/github_actions_composites_aws_create_route53_entry@main
        with:
          aws_access_key_id: "${{ steps.assume_role.outputs.aws_access_key_id }}"
          aws_secret_access_key: "${{ steps.assume_role.outputs.aws_secret_access_key }}"
          aws_session_token: "${{ steps.assume_role.outputs.aws_session_token }}"
          aws_route53_hosted_zone_id: "${{ secrets.ROUTE53_ZONEID }}"
          aws_route53_rr_action: "UPSERT"
          aws_route53_rr_name: "${{ github.event.inputs.hostname }}"
          aws_route53_rr_type: "${{ steps.determine_record_type.outputs.record_type }}"
          aws_route53_rr_ttl: "60"
          aws_route53_rr_value: "${{ github.event.inputs.input_address }}"
```

This README provides clear instructions on how to use the composite action, including necessary inputs, example workflow configurations for using AWS keys and IAM roles, and details about the action's functionality.