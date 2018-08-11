{% set python_version_params = {} -%}
{%- for version_available in readme.python_versions -%}
  {{ version_available.version }} ?= {{ python.version }}
  {%- if version_available.version == python.version -%}
    {%- set python_version_params = python_version_params.update(version_available) -%}
  {%- endif -%}
{%- endfor -%}
