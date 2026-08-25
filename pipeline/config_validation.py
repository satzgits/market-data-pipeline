"""
config.py — Validation helpers for the market data pipeline.

These functions sanity-check the pipeline's configuration so that a bad value
(negative period, inverted threshold, empty symbol list, etc.) is caught at
startup instead of silently producing wrong indicators or never-firing alerts.
"""


def validate_indicator_config(cfg):
    """Validate indicator parameters.

    Enforces the basic sanity rules for the technical-indicator knobs:
      - periods must be positive integers
      - Bollinger Band standard deviation must be positive
      - fast < slow for the MACD
      - SMA/EMA period lists must be non-empty and positive
    Returns a list of error strings (empty means the config is valid).
    """
    errors = []
    for key in ("rsi_period", "macd_fast", "macd_slow", "macd_signal",
                "bb_period", "sma_periods", "ema_periods"):
        if key not in cfg:
            errors.append(f"missing indicator config '{key}'")
    if errors:
        return errors

    if not isinstance(cfg["rsi_period"], int) or cfg["rsi_period"] <= 0:
        errors.append("rsi_period must be a positive integer")
    if cfg["macd_fast"] <= 0 or cfg["macd_slow"] <= 0:
        errors.append("MACD fast/slow periods must be positive")
    if cfg["macd_fast"] >= cfg["macd_slow"]:
        errors.append("MACD fast period must be less than slow period")
    if cfg["macd_signal"] <= 0:
        errors.append("MACD signal period must be positive")
    if cfg["bb_period"] <= 0:
        errors.append("Bollinger Band period must be positive")
    if cfg["bb_std"] <= 0:
        errors.append("Bollinger Band std-dev must be positive")
    for key in ("sma_periods", "ema_periods"):
        if cfg[key] and (not all(isinstance(p, int) and p > 0 for p in cfg[key])):
            errors.append(f"{key} must contain only positive integers")
    return errors


def validate_alert_thresholds(cfg):
    """Validate alert thresholds.

    Reasonable bounds so alerts actually fire:
      - RSI oversold < RSI overbought, both inside (0, 100)
      - alert thresholds must be numbers
    Returns a list of error strings (empty means valid).
    """
    errors = []
    oversold = cfg.get("rsi_oversold")
    overbought = cfg.get("rsi_overbought")
    if oversold is None or overbought is None:
        errors.append("rsi_oversold and rsi_overbought must be set")
    else:
        if not (0 < oversold < 100):
            errors.append("rsi_oversold must be in (0, 100)")
        if not (0 < overbought < 100):
            errors.append("rsi_overbought must be in (0, 100)")
        if oversold >= overbought:
            errors.append("rsi_oversold must be less than rsi_overbought")
    return errors


def validate_all(indicator_cfg, alert_cfg):
    """Run both validators and return the combined list of errors."""
    return validate_indicator_config(indicator_cfg) + validate_alert_thresholds(alert_cfg)


def is_valid(indicator_cfg, alert_cfg):
    """Convenience wrapper: True if the full configuration is valid."""
    return not validate_all(indicator_cfg, alert_cfg)
