"""Tests for BACKEND_CORS_ORIGINS parsing."""

import pytest
from pydantic import ValidationError

from app.config import Settings


class TestParseCorsOrigins:
    def test_json_array_string(self):
        result = Settings.parse_cors_origins('["http://localhost:4331"]')
        assert result == ["http://localhost:4331"]

    def test_json_array_string_multiple_origins(self):
        result = Settings.parse_cors_origins('["http://a.example", "http://b.example"]')
        assert result == ["http://a.example", "http://b.example"]

    def test_comma_separated_string(self):
        result = Settings.parse_cors_origins("http://localhost,http://localhost:4321")
        assert result == ["http://localhost", "http://localhost:4321"]

    def test_single_origin_string(self):
        result = Settings.parse_cors_origins("https://example.com")
        assert result == ["https://example.com"]

    def test_strips_whitespace_around_comma_separated_origins(self):
        result = Settings.parse_cors_origins(" http://a.example , http://b.example ")
        assert result == ["http://a.example", "http://b.example"]

    def test_list_passthrough(self):
        result = Settings.parse_cors_origins(["http://a.example"])
        assert result == ["http://a.example"]

    @pytest.mark.parametrize(
        "garbage",
        [
            '["http://localhost"',  # malformed JSON (missing closing bracket)
            "[not, valid, json]",
            "[1, 2, 3]",  # valid JSON but not a list of strings
        ],
    )
    def test_garbage_value_raises(self, garbage):
        with pytest.raises(ValueError):
            Settings.parse_cors_origins(garbage)

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            Settings.parse_cors_origins("   ")


class TestSettingsFromEnv:
    """Exercise the full pydantic-settings env pipeline, not just the validator function.

    pydantic-settings normally json.loads() env values for list-typed fields before any
    field_validator runs, which would reject plain comma-separated strings outright. These
    tests catch that regression by actually instantiating Settings from os.environ.
    """

    def test_json_array_env_value(self, monkeypatch):
        monkeypatch.setenv("BACKEND_CORS_ORIGINS", '["http://localhost:4331"]')
        assert Settings().BACKEND_CORS_ORIGINS == ["http://localhost:4331"]

    def test_comma_separated_env_value(self, monkeypatch):
        monkeypatch.setenv("BACKEND_CORS_ORIGINS", "http://localhost,http://localhost:4321")
        assert Settings().BACKEND_CORS_ORIGINS == [
            "http://localhost",
            "http://localhost:4321",
        ]

    def test_garbage_env_value_raises(self, monkeypatch):
        monkeypatch.setenv("BACKEND_CORS_ORIGINS", '["http://localhost"')
        with pytest.raises(ValidationError):
            Settings()
