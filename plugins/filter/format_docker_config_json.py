import base64

DOCUMENTATION = '''
module: format_docker_config_json
short_description: Turn a robot account structure into a C(.dockerconfigjson) fragment
description:
- This filter massages the return value of C(epfl_si.quay.robot_account) into a C(.dockerconfigjson) fragment
  suitable for putting in a Kubernetes Secret.

version_added: 0.4.0
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

class FilterModule(object):
    '''
    Parse a string of the form `foo.bar/myimage:mytag`
    '''

    def filters(self):
        return {
            'format_docker_config_json': self.format_docker_config_json
        }

    def format_docker_config_json (self, robot_account_struct):
        basic_auth = base64.b64encode(f'{robot_account_struct["name"]}:{robot_account_struct["token"]}'.encode()).decode("ascii")
        quay_hostname = robot_account_struct["quay_hostname"]

        return """{
  "auths": {
    "%(quay_hostname)s": {
      "auth": "%(basic_auth)s",
      "email": ""
    }
  }
}""" % dict(
          quay_hostname=quay_hostname,
          basic_auth=basic_auth)
