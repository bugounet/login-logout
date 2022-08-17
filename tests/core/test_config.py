from os import environ

import pytest

from msio.logme.core.config import load_config_file_from_env


@pytest.mark.parametrize("project_name", ("my_backend", "logme"))
def test_load_config_file_from_env(project_name):
    environ["MSIO_LOG_ME_PROJECT_NAME"] = project_name
    config = load_config_file_from_env()
    assert config.PROJECT_NAME is not None
    assert config.PROJECT_NAME == project_name
