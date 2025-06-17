# Version 0.6.4

- Fix a few bugs related to mirroring

# Version 0.6.3

- Fix more permayellows in `epfl_si.quay.quay_repository`

# Version 0.6.2

- Fix `module 'datetime' has no attribute 'UTC'` on Python 3.10.x

# Version 0.6.1

- Fix a permayellow involving `epfl_si.quay.quay_repository` and mirroring

# Version 0.6.0

- Better error messages in case Kubernetes rejects our changes
- Update `quay_repository` state (using an HTTP PUT request)

# Version 0.5.0

- Tolerate `mirror.tags` being a single string, rather than a list

# Version 0.4.0

- Introduce the `format_docker_config_json` filter

# Version 0.3.0

- Introduce the `robot_account` lookup plugin

# Version 0.2.0

- Introduce the `robot_account_permission` task

# Version 0.1.0

- Introduce the `quay_repository` task, with support for mirroring
