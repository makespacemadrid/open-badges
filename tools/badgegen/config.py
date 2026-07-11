"""Rutas, constantes y carga de credenciales de badgegen."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

CANVAS_SIZE = 1254
TARGET_DIAMETER = 1180
ROUNDNESS_THRESHOLD = 0.985
MIN_FIXABLE_RATIO = 0.95
JSDELIVR_PURGE = "https://purge.jsdelivr.net/gh/makespacemadrid/open-badges@main/{file}"


def load_env_file(path: Path) -> None:
    """Carga KEY=VALUE de un .env en os.environ sin pisar valores existentes."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


@dataclass(frozen=True)
class Settings:
    repo_root: Path

    @classmethod
    def locate(cls) -> "Settings":
        root = Path(__file__).resolve().parents[2]
        settings = cls(repo_root=root)
        load_env_file(settings.env_path)
        return settings

    @property
    def manifest_path(self) -> Path:
        return self.repo_root / "badges.yaml"

    @property
    def candidates_dir(self) -> Path:
        return self.repo_root / "candidates"

    @property
    def review_dir(self) -> Path:
        return self.repo_root / "review"

    @property
    def readme_path(self) -> Path:
        return self.repo_root / "README.md"

    @property
    def missing_path(self) -> Path:
        return self.repo_root / "missing-images.md"

    @property
    def env_path(self) -> Path:
        return self.repo_root / "tools" / ".env"

    @property
    def catalog_path(self) -> Path:
        env = os.environ.get("BADGEGEN_CATALOG")
        if env:
            return Path(env)
        return self.repo_root.parent / "InfraSelfService" / "src" / "lib" / "badges" / "catalog.ts"
