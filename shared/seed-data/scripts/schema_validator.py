"""
JSON Schema validation for seed data exports.

Uses fastjsonschema for high-performance validation against formal JSON schemas.
Complements validators.py by providing structural validation (types, formats, patterns)
while validators.py provides domain-specific validation (foreign keys, enums).
"""

import fastjsonschema
import json
from pathlib import Path
from typing import List, Dict, Any, Optional


class SchemaValidator:
    """Validates exported seed data against JSON schemas."""

    # Map file types to schema filenames
    SCHEMA_MAP = {
        'case_sets': 'schema_caseset.json',
        'cases': 'schema_cases.json',
        'algorithms': 'schema_algorithms.json'
    }

    def __init__(self, schemas_dir: Path):
        """
        Initialize schema validator.

        Args:
            schemas_dir: Directory containing JSON schema files
        """
        self.schemas_dir = schemas_dir
        self.validators = {}
        self._load_and_compile_schemas()

    def _load_and_compile_schemas(self):
        """
        Load and compile all schemas for fast validation.

        Schemas are compiled once at initialization for optimal performance.
        fastjsonschema compiles JSON schemas to Python code.
        """
        for file_type, schema_filename in self.SCHEMA_MAP.items():
            schema_path = self.schemas_dir / schema_filename

            if not schema_path.exists():
                print(f"Warning: Schema file not found: {schema_path}")
                continue

            try:
                with open(schema_path, 'r') as f:
                    schema = json.load(f)

                # Compile schema to Python code for fast validation
                self.validators[file_type] = fastjsonschema.compile(schema)

            except Exception as e:
                print(f"Error loading schema {schema_filename}: {str(e)}")

    def validate(
        self,
        records: List[Dict[str, Any]],
        file_type: str,
        file_name: str
    ) -> List[str]:
        """
        Validate records against JSON schema.

        Args:
            records: List of records to validate
            file_type: Type of file ('case_sets', 'cases', or 'algorithms')
            file_name: Name of the file being validated (for error messages)

        Returns:
            List of error messages (empty if valid)
        """
        # Check if we have a validator for this file type
        if file_type not in self.validators:
            if file_type in self.SCHEMA_MAP:
                # Schema exists but failed to load
                return [f"{file_name}: No schema validator available (schema file may be missing or invalid)"]
            else:
                # Unknown file type
                return [f"{file_name}: Unknown file type '{file_type}' (no schema defined)"]

        try:
            # Validate entire array against schema
            self.validators[file_type](records)
            return []  # Validation passed

        except fastjsonschema.JsonSchemaValueException as e:
            # Format validation error for user-friendly output
            error_msg = self._format_validation_error(e, file_name, file_type)
            return [error_msg]

        except Exception as e:
            # Unexpected error during validation
            return [f"{file_name}: Unexpected validation error: {str(e)}"]

    def _format_validation_error(
        self,
        error: fastjsonschema.JsonSchemaValueException,
        file_name: str,
        file_type: str
    ) -> str:
        """
        Format validation error for clear display.

        Args:
            error: fastjsonschema JsonSchemaValueException
            file_name: Name of file being validated
            file_type: Type of file

        Returns:
            Formatted error message
        """
        # Extract key error information
        error_message = error.message
        error_path = self._format_error_path(error)

        # Get schema filename for reference
        schema_file = self.SCHEMA_MAP.get(file_type, 'unknown')

        # Build comprehensive error message
        if error_path:
            msg = f"{file_name}: Schema validation failed at {error_path} - {error_message}"
        else:
            msg = f"{file_name}: Schema validation failed - {error_message}"

        msg += f" (schema: {schema_file})"

        return msg

    def _format_error_path(self, error: fastjsonschema.JsonSchemaValueException) -> str:
        """
        Format the JSON path where validation failed.

        Args:
            error: fastjsonschema JsonSchemaValueException

        Returns:
            Formatted path string (e.g., "records[3].id" or "records[0].case_ids[2].code")
        """
        try:
            # fastjsonschema provides path as a deque
            if hasattr(error, 'path') and error.path:
                path_parts = list(error.path)

                # Build user-friendly path
                formatted_parts = []
                for i, part in enumerate(path_parts):
                    if isinstance(part, int):
                        # Array index
                        formatted_parts.append(f"[{part}]")
                    else:
                        # Object property
                        if i > 0:
                            formatted_parts.append(f".{part}")
                        else:
                            formatted_parts.append(str(part))

                return ''.join(formatted_parts)
        except:
            pass

        return ""

    def get_schema_info(self) -> Dict[str, str]:
        """
        Get information about loaded schemas.

        Returns:
            Dictionary mapping file types to schema filenames
        """
        return {
            file_type: schema_file
            for file_type, schema_file in self.SCHEMA_MAP.items()
            if file_type in self.validators
        }

    def is_schema_loaded(self, file_type: str) -> bool:
        """
        Check if schema is loaded for a file type.

        Args:
            file_type: Type of file ('case_sets', 'cases', or 'algorithms')

        Returns:
            True if schema is loaded and ready
        """
        return file_type in self.validators
