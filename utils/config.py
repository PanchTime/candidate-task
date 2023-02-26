from typing import Optional

from pydantic import BaseSettings, validator, Field


class ConditionalFilter(BaseSettings):
    node_name: Optional[str]
    tag_name: Optional[str]
    attr_name: Optional[str]
    attr_value: Optional[str]

    def all(self) -> bool:
        return all([self.node_name, self.tag_name, self.attr_name, self.attr_value])

    def any(self) -> bool:
        return any([self.node_name, self.tag_name, self.attr_name, self.attr_value])

    @validator("node_name")
    def strip_any_slashes(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return v.strip("/")


class Configuration(BaseSettings):
    xml_file: str
    filter_settings: Optional[str]
    conditional_filters: Optional[ConditionalFilter]
    output_file: Optional[str]

    class Config:
        env_nested_delimiter = "__"

    @validator("xml_file")
    def check_xml_file(cls, v: str) -> str:
        if not v.endswith(".xml"):
            raise ValueError("xml_file is not in XML format.")
        return v
