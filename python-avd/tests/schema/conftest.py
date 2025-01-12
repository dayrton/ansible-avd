# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from pathlib import Path
from sys import path

import pytest
from yaml import safe_load

# Override global path to load schema from source instead of any installed version.
# Avoids to load from pyavd to avoid relying on pyavd vendor things being generated.
path.insert(0, str(Path(__file__).parents[2].joinpath("pyavd")))

import schema.constants

ARTIFACTS_PATH = Path(__file__).parent.joinpath("artifacts")
EOS_DESIGNS_SCHEMA_PATH = ARTIFACTS_PATH.joinpath("eos_designs.schema.yml")
EOS_CLI_CONFIG_GEN_SCHEMA_PATH = ARTIFACTS_PATH.joinpath("eos_cli_config_gen.schema.yml")

# The schemas are read of test artifacts which are frozen copies of the regular schemas.
# We keep a frozen copy of the schemas here, so the expected outputs don't change as the schemas evolve.
with open(EOS_CLI_CONFIG_GEN_SCHEMA_PATH, encoding="UTF-8") as file:
    test_eos_cli_config_gen_schema = safe_load(file)
with open(EOS_DESIGNS_SCHEMA_PATH, encoding="UTF-8") as file:
    test_eos_designs_schema = safe_load(file)
STORE = {
    "eos_cli_config_gen": test_eos_cli_config_gen_schema,
    "eos_designs": test_eos_designs_schema,
}

# Overriding schema store directly in the loaded module (cached so imports inside the code will also get this)
schema.constants.STORE = STORE


@pytest.fixture(scope="module")
def artifacts_path() -> Path:
    return ARTIFACTS_PATH


@pytest.fixture(scope="module")
def output_path() -> Path:
    return ARTIFACTS_PATH.joinpath("output")


@pytest.fixture(scope="module")
def schema_store() -> dict[str, dict]:
    """
    Return dict with schemas
    {
        "eos_cli_config_gen": dict
        "eos_designs": dict
    }
    """
    return STORE


@pytest.fixture(scope="module")
def schema_paths() -> dict[str, dict]:
    """
    Return dict with schema paths
    {
        "eos_cli_config_gen": Path
        "eos_designs": Path
    }
    """
    return {
        "eos_cli_config_gen": EOS_CLI_CONFIG_GEN_SCHEMA_PATH,
        "eos_designs": EOS_DESIGNS_SCHEMA_PATH,
    }
