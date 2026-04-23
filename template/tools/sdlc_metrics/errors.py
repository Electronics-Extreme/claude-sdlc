"""Typed exceptions for sdlc-metrics. Never `raise Exception(...)`."""
from __future__ import annotations


class MetricsError(Exception):
    """Base for all sdlc-metrics errors."""


class PricingMissingError(MetricsError):
    """Transcript references a model not in pricing.yaml."""


class SecretsDetectedError(MetricsError):
    """Transcript contains a pattern matching a secret; refused per NFR-METRICS-SEC-1."""


class AdapterError(MetricsError):
    """Adapter couldn't parse a transcript."""


class BudgetBreachError(MetricsError):
    """Phase budget exceeded; non-zero CI gate."""


class ConfigError(MetricsError):
    """Config file malformed or missing required fields."""
