import argparse
import sys

from .config import load_config
from .updater import run_update


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Necesse Server and Mod Updater")
    parser.add_argument("--config", "-c", help="Path to config.json", default=None)
    args = parser.parse_args(argv)

    cfg = load_config(args.config)
    return run_update(cfg)


if __name__ == "__main__":
    sys.exit(main())
