from abc import ABC, abstractmethod
import functools

import requests

from ansible_collections.epfl_si.actions.plugins.module_utils.ansible_api import AnsibleResults

class QuayActionMixin(ABC):
    """Things that are useful to more than one action plugin.

    Classes that want to use this mixin must inherit from it, and make
    sure that `self.api` is set to an instance of
    `ansible_collections.epfl_si.actions.plugins.module_utils.subactions.AnsibleActions`.
    In order to use the `.changed` and `.failed` methods, `self.result` should further be
    set (typically to `AnsibleResults.empty()` or the empty dict). Finally, it is highly
    recommended to override the `moniker` property, to make status and error messages more
    useful.
    """

    @property
    def quay_bearer_token (self):
        return self.ansible.jinja.expand("{{ ansible_quay_bearer_token }}")

    @property
    def quay_hostname (self):
        return self.ansible.jinja.expand("{{ ansible_quay_hostname }}")

    @property
    def quay_request (self):
        url_base = f"https://{self.quay_hostname}"

        def authify (headers):
            if "Authorization" not in headers:
                headers["Authorization"] = f"bearer {self.quay_bearer_token}"
            return headers

        class QuayRequests:
            @classmethod
            def request (cls, method, endpoint, json, headers={}):
                response = requests.request(
                    method,
                    f"{url_base}{endpoint}",
                    json=json, headers=authify(headers))

                response.raise_for_status()
                return response

            @classmethod
            def get (cls, endpoint, json=None, headers={}):
                return cls.request("GET", endpoint, json, headers)

            @classmethod
            def post (cls, endpoint, json, headers={}):
                return cls.request("POST", endpoint, json, headers)

            @classmethod
            def put (cls, endpoint, json, headers={}):
                return cls.request("PUT", endpoint, json, headers)

            @classmethod
            def delete (cls, endpoint, json=None, headers={}):
                return cls.request("DELETE", endpoint, json, headers)

        return QuayRequests

    @property
    def moniker (self):
        """A short string describing this instance.

        You will probably want to override this in a subclass.
        """
        return self.__class__.__name__

    def changed (self, change_description):
        AnsibleResults.update(self.result, { "changed": True })
        self.result.setdefault("actions", []).append(f"{self.moniker}: {change_description}")

    def failed (self, change_description, error=None):
        AnsibleResults.update(self.result, { "failed": True })
        self.result["msg"] = f"{self.moniker}: {change_description}: {error if error else 'failed'}"


def returns_none_on_404 (f):
    def ff (*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            else:
                raise
    return ff
