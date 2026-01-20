#!/bin/bash
poetry run isort .
poetry run ruff format .
