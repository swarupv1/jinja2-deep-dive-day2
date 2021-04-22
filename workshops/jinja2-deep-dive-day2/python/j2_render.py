#!/usr/bin/env python

import argparse
from pathlib import Path

import jinja2
import yaml

from libs import ipaddr

BASE_DIR = Path(__file__).parent.absolute()
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "templates"
VARS_DIR = BASE_DIR / "vars"

regions = {
    "EMEA": {
        "sites": ["london", "paris", "madrid"],
        "logging_hosts": ["10.1.54.4", "10.4.6.16"],
    }
}


def get_lab_prefix(template_name):
    lab_prefix = ""
    if "lab" in template_name:
        lab_prefix = template_name.split("-")[0]

    return lab_prefix


def load_file_vars(file_vars_name, lab_prefix):
    """Load yaml/json file with vars

    using yaml module as it parses both json and yaml files

    Args:
        file_vars_name (str): name of the file with vars
        lab_prefix (str): identifies lab number

    Returns:
        dict: dictionary with parsed vars
    """

    template_vars = {}

    if lab_prefix:
        file_all_vars = VARS_DIR / f"{lab_prefix}-all.yml"
        if file_all_vars.exists():
            with file_all_vars.open(mode="r", encoding="utf8") as fin:
                data = yaml.load(fin, Loader=yaml.SafeLoader)
                template_vars.update(data)

    file_vars_path = VARS_DIR / file_vars_name

    with file_vars_path.open(mode="r", encoding="utf8") as fin:
        template_vars.update(yaml.load(fin, Loader=yaml.SafeLoader))

    return template_vars


def render_template(template_name, template_data, strict, trim, lstrip):
    """Renders template using provided data

    Args:
        template_name (str): template file name
        template_data (dict): data used to render template

    Returns:
        str: rendered template output
    """
    undefined_class = jinja2.StrictUndefined if strict else jinja2.Undefined

    j2_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
        undefined=undefined_class,
        trim_blocks=trim,
        lstrip_blocks=lstrip,
    )
    j2_env.filters.update(ipaddr.FilterModule.filter_map)
    j2_template = j2_env.get_template(template_name)

    if not j2_template:
        raise FileNotFoundError

    rendered_template = j2_template.render(template_data)

    return rendered_template


def parse_cli_args():
    """Parse command line options"""
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument("-t", "--template", required=True)
    cli_parser.add_argument("-d", "--data-file", required=False)
    cli_parser.add_argument("-o", "--output-file", required=False)
    cli_parser.add_argument("-s", "--silent", action="store_true")
    cli_parser.add_argument("-strict", action="store_true")
    cli_parser.add_argument("-trim", action="store_true")
    cli_parser.add_argument("-strip", action="store_true")

    cli_args = cli_parser.parse_args()

    return cli_args


def main():
    cli_args = parse_cli_args()

    template_name = cli_args.template
    data_file = cli_args.data_file
    output_file = cli_args.output_file
    strict_check = cli_args.strict
    j2_trim = cli_args.trim
    j2_lstrip = cli_args.strip

    lab_prefix = get_lab_prefix(template_name)
    template_vars = {}
    if data_file:
        template_vars = load_file_vars(data_file, lab_prefix)
    render_result = render_template(
        template_name, template_vars, strict_check, j2_trim, j2_lstrip
    )

    if output_file:
        with Path(OUTPUT_DIR / output_file).open(mode="w", encoding="utf8") as fout:
            fout.write(render_result)

    if not cli_args.silent:
        print(f"==== LOADED TEMPLATE: {template_name}")
        print(f"==== LOADED DATA FILE: {data_file}")
        print("==== RENDERED TEMPLATE")
        print(f"{render_result}")

        if output_file:
            print(f"==== OUTPUT FILE: {output_file}")


if __name__ == "__main__":
    main()
