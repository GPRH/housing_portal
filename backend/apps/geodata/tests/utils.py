"""Utilities for Resource tests."""

import pytest
import os
import shutil
from django.conf import settings


@pytest.fixture(scope='class')
def clear_temp(request):
    """Cleanup temp directories."""
    def teardown():
        path = settings.MEDIA_ROOT
        if os.path.exists(path):
            shutil.rmtree(path)
    request.addfinalizer(teardown)


@pytest.fixture(scope='class')
def clear_exports(request):
    """Cleanup export test directories."""
    def teardown():
        path = settings.EXPORTS_DIR
        if os.path.exists(path):
            shutil.rmtree(path)
    request.addfinalizer(teardown)
