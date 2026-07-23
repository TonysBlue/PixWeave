"""Standalone PixWeave CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .backend import LocalBackend
from .beta_launch import evaluate_beta_launch_package_file
from .beta_session import capture_session_file, summarize_session_economics_file
from .config import load_config
from .feedback import capture_feedback_file, triage_feedback_file
from .unit_economics import calculate_scenarios, load_scenarios


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pixweave", description="Standalone PixWeave product CLI")
    parser.add_argument("--config", default=None)
    sub = parser.add_subparsers(dest="command", required=True)
    beta_product = sub.add_parser("beta-product")
    beta_product.add_argument("--host", default="127.0.0.1")
    beta_product.add_argument("--port", type=int, default=18112)
    for name in ("validate-brand-kit", "campaign-manifest", "campaign-render", "prompt-pack", "product-shot-workflow", "visual-qa-scorecard"):
        command = sub.add_parser(name)
        command.add_argument("input", type=Path)
        if name == "campaign-render":
            command.add_argument("--output-dir", type=Path, default=None)
        else:
            command.add_argument("--output", type=Path, default=None)
    verify = sub.add_parser("campaign-render-verify")
    verify.add_argument("bundle_dir", type=Path)
    review = sub.add_parser("campaign-review")
    review.add_argument("bundle_dir", type=Path)
    review.add_argument("decisions", type=Path)
    review.add_argument("--output", type=Path, default=None)
    economics = sub.add_parser("unit-economics")
    economics.add_argument("input", type=Path)
    feedback = sub.add_parser("feedback-capture")
    feedback.add_argument("input", type=Path)
    feedback.add_argument("--output", type=Path, required=True)
    triage = sub.add_parser("feedback-triage")
    triage.add_argument("submission", type=Path)
    triage.add_argument("decision", type=Path)
    triage.add_argument("--output", type=Path, required=True)
    launch = sub.add_parser("beta-launch-readiness")
    launch.add_argument("input", type=Path)
    launch.add_argument("--output", type=Path, default=None)
    session = sub.add_parser("beta-session-capture")
    session.add_argument("input", type=Path)
    session.add_argument("--output", type=Path, required=True)
    session_economics = sub.add_parser("beta-session-economics")
    session_economics.add_argument("input", type=Path)
    session_economics.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config(args.config)
    backend = LocalBackend(config)
    try:
        if args.command == "beta-product":
            from .beta_product import serve
            serve(config, args.host, args.port)
        elif args.command == "validate-brand-kit":
            result = backend.validate_brand_kit_file(args.input)
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0 if result["ok"] else 1
        elif args.command == "campaign-manifest":
            print(json.dumps(backend.generate_campaign_manifest_file(args.input, args.output), indent=2, sort_keys=True))
        elif args.command == "campaign-render":
            print(json.dumps(backend.render_campaign_file(args.input, args.output_dir), indent=2, sort_keys=True))
        elif args.command == "campaign-render-verify":
            print(json.dumps(backend.verify_campaign_render_bundle_dir(args.bundle_dir), indent=2, sort_keys=True))
        elif args.command == "campaign-review":
            print(json.dumps(backend.record_campaign_review_file(args.bundle_dir, args.decisions, args.output), indent=2, sort_keys=True))
        elif args.command == "prompt-pack":
            print(json.dumps(backend.generate_prompt_manifest_file(args.input, args.output), indent=2, sort_keys=True))
        elif args.command == "unit-economics":
            print(json.dumps(calculate_scenarios(load_scenarios(args.input)), indent=2, sort_keys=True))
        elif args.command == "product-shot-workflow":
            print(json.dumps(backend.generate_product_shot_workflow_file(args.input, args.output), indent=2, sort_keys=True))
        elif args.command == "visual-qa-scorecard":
            print(json.dumps(backend.generate_visual_qa_scorecard_file(args.input, args.output), indent=2, sort_keys=True))
        elif args.command == "feedback-capture":
            print(json.dumps(capture_feedback_file(args.input, args.output), indent=2, sort_keys=True))
        elif args.command == "feedback-triage":
            print(json.dumps(triage_feedback_file(args.submission, args.decision, args.output), indent=2, sort_keys=True))
        elif args.command == "beta-launch-readiness":
            print(json.dumps(evaluate_beta_launch_package_file(args.input, args.output), indent=2, sort_keys=True))
        elif args.command == "beta-session-capture":
            print(json.dumps(capture_session_file(args.input, args.output), indent=2, sort_keys=True))
        elif args.command == "beta-session-economics":
            print(json.dumps(summarize_session_economics_file(args.input, args.output), indent=2, sort_keys=True))
        else:
            raise AssertionError(args.command)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0
