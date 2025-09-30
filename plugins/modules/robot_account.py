# This file is here for ansible-doc purposes **only**. The actual
# implementation is in ../action/robot_account.py as an action plugin
# (i.e. it runs on the Ansible controller.)

DOCUMENTATION = r"""
---
module: robot_account
short_description: Manage a robot account
description:
- Robot accounts are a feature of Quay that encapsulate a set of person-neutral
  (“system account”) permissions to a number of repositories for basic
  operations on images (push, pull).

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
    description: The Quay namespace in which the robot account lives
  short_name:
    type: str
    required: true
    description: The short name of the robot account (without the C(namespace+) prefix)
"""
