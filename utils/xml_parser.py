import json
import logging
import os
import time
from typing import Optional, TextIO

from lxml import etree
from lxml.etree import Element

from utils.config import ConditionalFilter


class XmlReader:
    """Reads XML file and filters elements based on filter settings and conditional filters if provided.

    Parses InvestmentVehicle data.

    Parameters
    ----------
    xml_file_path : str
        Path to the xml file to be parsed.
    filter_settings_path : Optional[str], optional
        Path to the json file containing filter settings (Priority run), by default None
    conditional_filters : Optional[ConditionalFilter], optional
        Conditional filters to be applied to the xml file (Second Priority run), by default None
    output_file_path : Optional[str], optional
        Output file path. If None, data will not be written to a file, by default None
    """
    def __init__(
            self,
            xml_file_path: str,
            filter_settings_path: Optional[str] = None,
            conditional_filters: Optional[ConditionalFilter] = None,
            output_file_path: Optional[str] = None,
    ):
        self.xml_file = xml_file_path
        self.filter_settings_path = filter_settings_path
        self.conditional_filter = conditional_filters
        self.output_file_path = output_file_path
        self.filter_config = None
        self.root = None
        self.processed_elements = 0
        self.writer = None

    def __enter__(self):
        self.load_xml_file()
        self.load_filter_settings()

        if self.output_file_path:
            self.writer = open(os.path.join("data", self.output_file_path), "w")

        logging.info(f"Loaded xml file: {self.xml_file}")
        logging.info(f"Loaded filter settings from: {self.filter_settings_path}")
        logging.info(f"Applied conditional filters: {self.conditional_filter}")
        logging.info(f"Write data to output file: {self.output_file_path}")

        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.writer:
            logging.info(f"Written: {self.writer.tell()} bytes to {self.output_file_path}")
            self.writer.close()
        logging.info(f"Processed {self.processed_elements} elements.")
        if exc_type:
            logging.warning(f"Exception occurred: {exc_type}, {exc_val}, {exc_tb}")
        else:
            logging.info("Successful run!")
        logging.info(f"Finished in {time.time() - self.start_time:3f} seconds.")

    def print_elements(self, element: Element, fo: Optional[TextIO] = None) -> None:
        """Recursively prints element's and all child's tags, attributes, and text.

        If a file object is provided, the output will be written to the output file.
        """
        self.processed_elements += 1
        element_path = element.getroottree().getpath(element)
        text = element.text
        attrs = element.attrib

        to_print = []
        if attrs:
            for k, v in attrs.items():
                to_print.append(f"{element_path}@{k}={v}")
        if text:
            to_print.append(f"{element_path}/#text={text}")

        to_print.append(element_path)
        if fo:
            fo.write("\n".join(to_print))

        print("\n".join(to_print))
        # Recursively print all children
        for child in element:
            self.print_elements(child, fo)

    def load_xml_file(self) -> None:
        """Load XML file into an ElementTree."""
        self.root = etree.parse(os.path.join("data", self.xml_file)).getroot()

    def load_filter_settings(self) -> None:
        """Load filter settings from a json file."""
        if self.filter_settings_path:
            with open(self.filter_settings_path, "r") as fo:
                self.filter_config = json.load(fo)

    def print_with_conditional_filtering(self) -> None:
        """Apply conditional filtering to an XML file if filter settings are provided. Otherwise, print all elements."""
        # Print elements based on conditional filtering if provided
        if self.conditional_filter:
            if self.conditional_filter.any() and not self.conditional_filter.all():
                raise ValueError("All arguments must be provided for conditional filtering.")

            elif self.conditional_filter.all():
                expression = f".//{self.conditional_filter.node_name}/" \
                             f"{self.conditional_filter.tag_name}" \
                             f"[@{self.conditional_filter.attr_name}={self.conditional_filter.attr_value}]/*"

                root = self.root.xpath(expression)
                if isinstance(root, list):
                    for e in root:
                        self.print_elements(e, self.writer)
        else:
            # Print all elements
            self.print_elements(self.root, self.writer)

    def print_from_output_filtering_settings(
            self,
            path: str,
            attr_name: Optional[str] = None,
            text: Optional[bool] = False,
    ) -> None:
        """Print elements from an output settings file."""
        if (
                text and attr_name
                or not text and not attr_name
        ):
            raise ValueError("At least one of text or attr_name must be provided.")

        output = []
        if text:
            try:
                elements = self.root.xpath(f"//{path}")
                output.append(f"Printing text for {path}:\n")
                for e in elements:
                    self.processed_elements += len(elements)
                    if self.writer:
                        output.append(e.text)
                    print(e.text)
            except Exception as e:
                logging.error(f"Failed to get text from {path}.")
                raise e

        else:
            elements = self.root.xpath(f"//{path.strip('/')}")

            if isinstance(elements, list):
                self.processed_elements += len(elements)
                output.append(f"Printing attribute: {attr_name} for {path}:\n")
                for e in elements:
                    if self.writer:
                        output.append(e.get(attr_name))
                    print(e.get(attr_name))

        output.append("\n")
        if self.writer:
            self.writer.write("\n".join(output))

    def run(self):
        """Run the XmlReader."""
        if self.filter_config:
            for rule in self.filter_config["rules"]:
                self.print_from_output_filtering_settings(**rule)

        else:
            self.print_with_conditional_filtering()
