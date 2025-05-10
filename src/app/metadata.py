from pathlib import Path

import toml
from pydantic import BaseModel


class Author(BaseModel):
    name: str | None = None
    email: str | None = None


class PackageMetadata(BaseModel):
    """Class representing package metadata from pyproject.toml"""

    name: str
    version: str
    description: str
    authors: list[Author]

    @classmethod
    def load(cls) -> "PackageMetadata":
        """Load package metadata with automatic detection of source.

        Direct pyproject.toml parsing

        Returns:
            PackageMetadata: The loaded package metadata

        Raises:
            FileNotFoundError: If pyproject.toml cannot be found in development
            ValueError: If required metadata fields are missing
        """

        return cls._from_pyproject_toml()

    @classmethod
    def _from_pyproject_toml(cls, path: Path | None = None) -> "PackageMetadata":
        """Load metadata directly from pyproject.toml file"""
        toml_path = path or cls._find_pyproject_toml()

        with open(toml_path) as f:
            config = toml.load(f)

        config = config.get("project", {})
        authors = config.get("authors", [Author(name="Mohamad Amin Jafari", email="mhmdamin.jafari@gmail.com")])

        return cls(
            name=config["name"],
            version=config["version"],
            description=config.get("description", "Video Processor task"),
            authors=authors,
        )

    @staticmethod
    def _find_pyproject_toml() -> Path:
        """Search parent directories for pyproject.toml"""
        path = Path.cwd()
        while path != path.parent:
            potential_path = path / "pyproject.toml"
            if potential_path.exists():
                return potential_path
            path = path.parent
        raise FileNotFoundError("Could not find pyproject.toml in parent directories")


# Usage example:
metadata = PackageMetadata.load()
print(f"Loaded package: {metadata.name} v{metadata.version}")
