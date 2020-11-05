from prettytable import PrettyTable


class FilterModule:
    """Defines a filter module object."""

    @staticmethod
    def filters():
        """Returns the Ansible filter bindings dictionary."""
        return {
            "build_table": FilterModule.build_table,
        }

    @staticmethod
    def build_table(table_data):
        """Builds a text table from list data."""
        table = PrettyTable()
        # Set the table column headers
        table.field_names = table_data.get("headers")

        # Add in row data one by one
        for row in table_data.get("rows"):
            table.add_row(row)

        # Return the pure text representation of the table
        return table.get_string()
