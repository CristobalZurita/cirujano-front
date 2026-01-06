import os
import pytest

from alembic.config import Config
from alembic import command


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    """Apply Alembic migrations before running tests."""
    here = os.path.dirname(os.path.dirname(__file__))
    alembic_cfg = Config(os.path.join(here, '..', 'alembic.ini'))
    alembic_cfg.set_main_option('script_location', os.path.join(here, '..', 'alembic'))
    # Use env vars / settings as configured by alembic/env.py
    command.upgrade(alembic_cfg, 'head')
    yield
    # No teardown: keep schema for inspection; tests should clean data if needed
