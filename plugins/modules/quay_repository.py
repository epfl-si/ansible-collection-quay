# This file is here for ansible-doc purposes **only**. The actual
# implementation is in ../action/quay_repository.py as an action plugin
# (i.e. it runs on the Ansible controller.)

DOCUMENTATION = r"""
---
module: quay_repository
short_description: Manage a Quay repository
description:
- A Quay *repository* is a place to store images whose names differ only
  by their *tags*.

- Using the Quay REST API, this action plugin can create, update and
  delete either “plain” repositories in your Quay instance (that you
  push to from some other means), or set up mirroring from some other
  Docker registry such as the Docker Hub, GHCR.io and more.

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
  name:
    type: str
    required: true
    description: The name of the repository, i.e. the second path component of the images' URI path
  description:
    type: str
    required: true
    description: The short blurb that explains what the repository is for.
  visibility:
    type: str
    required: true
    description: Either "public" or "private"
  mirror:
    type: complex
    description: The mirroring configuration to set up for this repository
    suboptions:
      from:
        type: str
        required: true
        description: The name (sans tag) of the original image to mirror from
      tags:
        type: list
        required: true
        description: The list of tags to mirror, as strings
      sync_interval:
        type: str
        default: 3600
        description: How often (in seconds) to check upstream for new images with the given C(tag) s
      robot_account:
        type: str
        required: true
        description: The name of the robot account that will be doing the mirroring
      timeout_seconds:
        type: int
        default: 600
        description: The timeout for remote (“Skopeo”) queries that Quay will perform to initialize and maintain the mirror.
"""
