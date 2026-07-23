"""Configuration for the standalone PixWeave product repository."""

from __future__ import annotations

import configparser
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProductConfig:
    workspace: Path
    data_root: Path
    artifacts_dir: Path
    logs_dir: Path
    product_name: str


def load_config(path: str | Path | None = None, *, workspace: Path | None = None) -> ProductConfig:
    root = (workspace or Path.cwd()).resolve()
    config_path = Path(path).resolve() if path else root / "config" / "pixweave.ini"
    if path is None and not config_path.exists():
        legacy_test_config = root / "config" / "sample.ini"
        if legacy_test_config.exists():
            config_path = legacy_test_config
    parser = configparser.ConfigParser()
    if config_path.exists():
        parser.read(config_path)
    data_root = Path(parser.get("paths", "data_root", fallback=str(Path.home() / "product-data" / "pixweave"))).expanduser().resolve()
    return ProductConfig(
        workspace=root,
        data_root=data_root,
        artifacts_dir=data_root / "artifacts",
        logs_dir=data_root / "logs",
        product_name=parser.get("product", "name", fallback="织象 PixWeave"),
    )


CompanyConfig = ProductConfig
