from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class PixWeaveRepositoryTest(unittest.TestCase):
    def test_product_repository_has_independent_cli_and_runtime(self) -> None:
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            ["python3.11", "-m", "pixweave", "--help"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("beta-product", result.stdout)
        self.assertNotIn("worker-run", result.stdout)
        self.assertNotIn("chairman", result.stdout.lower())

    def test_product_config_keeps_runtime_data_outside_git(self) -> None:
        from pixweave.config import load_config

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cfg = load_config(root / "missing.ini", workspace=root)
            self.assertEqual(cfg.workspace, root)
            self.assertEqual(cfg.data_root, Path.home() / "product-data" / "pixweave")
            self.assertEqual(cfg.artifacts_dir, cfg.data_root / "artifacts")

    def test_checked_in_service_is_loopback_only(self) -> None:
        root = Path(__file__).resolve().parents[1]
        service = (root / "deploy" / "pixweave-beta.service").read_text(encoding="utf-8")
        self.assertIn("--host 127.0.0.1", service)
        self.assertNotIn("--host 0.0.0.0", service)

    def test_product_manifest_declares_repository_and_verification(self) -> None:
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / "product.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["product_id"], "pixweave")
        self.assertEqual(manifest["repository"], "git@github.com:TonysBlue/PixWeave.git")
        self.assertEqual(manifest["local_path"], "~/products/pixweave")
        self.assertEqual(manifest["runtime_data_root"], "~/product-data/pixweave")
        self.assertEqual(manifest["canonical_test"], "python3.11 -m unittest discover -s tests -v")


if __name__ == "__main__":
    unittest.main()
