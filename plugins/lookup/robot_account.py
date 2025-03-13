DOCUMENTATION = '''
module: robot_account
short_description: Retrieve the details (including OAuth token) of a robot account
description:
- This lookup plugin fetches the details of a Quay robot account out of Quay's REST API.

version_added: 0.3.0
'''

EXAMPLES = '''

# 
- set_fact:
    _quay_puller_token: >-
      {{ lookup("epfl_si.quay.robot_account", quay_organization, quay_puller_robot_account_name,
                token=admin_token)["token"]
      }}
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
        
        return [robot for robot in response.json()["robots"]
                if robot["name"] == robot_account_name]
