import os
import sys


def _prepare_path():
    # Ensure package import works when running from source or bundled
    if getattr(sys, 'frozen', False):
        # PyInstaller bundle; imports should already work
        return
    here = os.path.dirname(__file__)
    root = os.path.abspath(os.path.join(here))
    if root not in sys.path:
        sys.path.insert(0, root)


def main():
    _prepare_path()
    from necesse_smu.cli import main as cli_main  # type: ignore
    return cli_main()


if __name__ == '__main__':
    raise SystemExit(main())
