# This file is here for ansible-doc purposes **only**. The actual
# implementation is in ../action/robot_account_permission.py as an action plugin
# (i.e. it runs on the Ansible controller.)

DOCUMENTATION = r"""
---
module: robot_account_permission
short_description: Manage one permission for a robot account
description:
- TODO

- "This action plugin reads from the following Ansible variables:"

- C(ansible_quay_hostname)
- The hostname of the Quay server to send REST API calls to.

- C(ansible_quay_bearer_token)
- The bearer token to pass in every REST API call to C(ansible_quay_hostname).

options:
  state:
    type: str
    default: V(present)
    description: The desired postcondition, either V(present) or V(absent)
  organization:
    type: str
    required: true
    description: The Quay namespace (first path component of the images' URL) in which the repository lives
  repository_name:
    type: str
    required: true
    description: The Quay namespace (first path component of the images' URI path) that the repository lives in
  robot_account_name:
    type: str
    required: true
    description: The name of the robot account to configure the permission for
  permission:
    type: str
    default: "read"
    description: One of "read", "write" or "admin"
"""
