import argparse
import logging
import os
from datetime import datetime

from pydantic import ValidationError

from utils.config import Configuration
from utils.xml_parser import XmlReader


def main(config: Configuration) -> None:
    with XmlReader(
            xml_file_path=config.xml_file,
            filter_settings_path=config.filter_settings,
            conditional_filters=config.conditional_filters,
            output_file_path=config.output_file,
    ) as reader:
        reader.run()


if __name__ == '__main__':
    # Set up logging
    if not os.path.exists("data/logs"):
        os.makedirs("data/logs")

    logging.basicConfig(
        # Make sure it appears in the data directory
        filename=os.path.join("data", "logs", f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"),
        level=logging.NOTSET,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    # Load configuration
    try:
        cfg = Configuration()
    except ValidationError as e:
        logging.warning("Failed to load from env variables. Trying to load from command line.")
        try:
            parser = argparse.ArgumentParser(
                description="Process an xml file.",
                formatter_class=argparse.ArgumentDefaultsHelpFormatter
            )
            parser.add_argument('--xml-file', '-f', type=str, help="Xml file name to process must be in data folder.")
            parser.add_argument('--output-file', '-o',
                                type=str, default=None, help="Output file path, supports txt format for now.")
            parser.add_argument('--filters', type=str, default=None, help="Json filter configuration file.")

            args = parser.parse_args()
            logging.warning(f"args: {args}")
            cfg = Configuration(
                xml_file=args.xml_file,
                filter_settings=args.filters,
                output_file=args.output_file,
            )
        except ValidationError as e:
            logging.error("Failed to create configuration from command line arguments.")
            raise e
        except Exception as e:
            logging.warning("Failed to load from command line. Using default values.")
            raise ValueError("Both env variables and command line arguments are missing.")

    main(cfg)
