### Documentation

#### Inputs
- **length**: The length of the random password. (**Required**, Default: `16`)

#### Outputs
- **RANDOM_PASSWORD**: The generated random password.

#### Example Usage
To use this composite action in your GitHub workflow, add the following steps:

```yaml
steps:
  - name: "Generate Random Password"
    uses: gzukel/github_actions_composites/generate_random_password@main
    with:
      length: 16

  - name: "Use Generated Password"
    run: echo "The generated password is stored in the environment variable: ${{ env.RANDOM_PASSWORD }}"
```

This composite action will generate a random password using the specified length, save it to an environment variable, and upload it as an artifact.