#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `check_dockerfile` package."""

# Third party modules
import pytest

# First party modules
import check_dockerfile


def test_version():
    assert check_dockerfile.__version__.count(".") == 2


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0
