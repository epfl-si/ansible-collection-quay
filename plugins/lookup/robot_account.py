DOCUMENTATION = '''
module: robot_account
short_description: Retrieve the details (including OAuth token) of a robot account
description:
- This lookup plugin fetches the details of a Quay robot account out of Quay's REST API.

version_added: 0.3.0
'''

EXAMPLES = '''

- name: "`Secret/my-puller-robot`"
  kubernetes.core.k8s:
    state: present
    definition:
      apiVersion: v1
      kind: Secret
      metadata:
        name: my-puller-robot
        namespace: my-namespace
      type: kubernetes.io/dockerconfigjson
      stringData:
        .dockerconfigjson: >-
          {{ lookup("epfl_si.quay.robot_account", my_organization, my_robot_account_name,
                                                  token=_my_token)
          | epfl_si.quay.format_docker_config_json | string }}
  vars:
    _my_token: ...

'''

import requests

from ansible.plugins.lookup import LookupBase
from ansible_collections.epfl_si.quay.plugins.module_utils.quay_actions import QuayActionMixin

class LookupModule (LookupBase):
    def run (self, terms, variables=None, hostname=None, token=None):
        [organization, robot_account_name] = terms
        if token is None:
            token = variables["ansible_quay_bearer_token"]

        if hostname is None:
            hostname = variables["ansible_quay_hostname"]

        response = requests.get(
            f"https://{hostname}/api/v1/organization/{organization}/robots",
            headers=dict(Authorization=f"bearer {token}"))
        response.raise_for_status()
        
        ret = [robot for robot in response.json()["robots"]
                if robot["name"] == robot_account_name]

        # For the benefit of ../filter/format_docker_config_json.py (or for any other purpose):
        for robot in ret:
            robot["quay_hostname"] = hostname

        return ret
