# `epfl_si.quay` Ansible Collection

This collection provides action plugins to manipulate the Quay API.

## Generate a token
1. Navigate to quay.io/organization
1. Select your organization
1. In OAuth Applications, click Create New Application
1. Enter a name, for instance 'ansible' and continue
1. Select the application and click Generate Token
1. Check the following settings:
  - [x] Administer Organization
  - [x] Administer Repositories
  - [x] Create Repositories
  - [x] View all visible repositories
  - [x] Read/Write to any accessible repositories
1. Save the token in the variable 'ansible_quay_bearer_token'
