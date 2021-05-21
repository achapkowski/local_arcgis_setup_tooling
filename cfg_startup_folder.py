import os
import argparse
import subprocess
from pathlib import Path
import logging

_logger = logging.getLogger()

__version__ = "1.0.0"
# -------------------------------------------------------------------------
def set_logging(verbose: int = 0):
    """sets the logger and format"""
    if verbose > 0:
        logging.basicConfig(format="%(levelname)s : %(message)s", level=logging.DEBUG)
        _logger = logging.getLogger("simple_example")
        _logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        _logger.addHandler(ch)
    return


# -------------------------------------------------------------------------
def main(input_path: str, verbose: int = 0):
    """driver method"""
    set_logging(verbose=verbose)
    input_path = os.path.normpath(input_path)

    os.makedirs(input_path, exist_ok=True)

    ## Call out to create the configuration file.
    subprocess.call("jupyter notebook --generate-config -y")

    home = str(Path.home())

    fp = os.path.join(home, ".jupyter", "jupyter_notebook_config.py")

    if os.path.isfile(fp):
        with open(fp, "r") as reader:
            _logger.debug("Updating the settings for the configuration file")
            text = reader.read()
            text = text.replace(
                """#c.NotebookApp.notebook_dir = ''""",
                f"""c.NotebookApp.notebook_dir = r'{input_path}'""",
            )

        _logger.debug("writing out the configuration")
        with open(fp, "w") as writer:
            writer.write(text)
        print("Configuration completed, enjoy")
        print('Run "jupyter notebook" to start notebook server.')
    else:
        print("Cannot find the jupyter_notebook_config.py file.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--startup-folder",
        required=True,
        help="The location where Jupyter Notebook will start.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--verbose", "-v", action="count", default=0)
    args = parser.parse_args()
    main(input_path=args.startup_folder, verbose=args.verbose)
