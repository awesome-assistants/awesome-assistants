import tablib
import yaml
import pathlib
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_assistants():
    assistants_yml = pathlib.Path(__file__).parent.resolve().joinpath("assistants.yml")
    with open(assistants_yml, 'r') as f:
        assistants = yaml.safe_load(f)
    return assistants


def build():
    dataset = tablib.Dataset()
    dataset.headers = ['assistant', 'name', 'emoji', 'welcome_message', 'instructions', 'parse_mode']
    for key, entry in get_assistants().items():
        # logger.info('Processing assistant: %s', key)
        dataset.append([key, entry['name'], entry['emoji'], entry['welcome_message'], entry['instructions'], entry['parse_mode']])

    to_file(dataset, 'csv')
    to_file(dataset, 'json')
    to_file(dataset, 'html')
    to_file(dataset, 'latex')
    to_file(dataset, 'tsv')
    # to_file(dataset, 'xlsx', 'wb')
    # to_file(dataset, 'ods', 'wb')


def to_file(dataset, format, bin='w'):
    data = dataset.export(format)
    with open('build/assistants.'+format, bin) as file:
        file.write(data)


def replace_text_between(original_text, delimeter_a, delimter_b, replacement_text):
    leading_text = original_text.split(delimeter_a)[0]
    trailing_text = original_text.split(delimter_b)[1]
    return leading_text + delimeter_a + replacement_text + delimter_b + trailing_text


def get_assistants_markdown():
    md = ""
    for key, entry in get_assistants().items():
        md += f"- [{entry['emoji']} {entry['name']}](#{key.replace('_', '-')})\n"

    for key, entry in get_assistants().items():
        md += f"\n ### {entry['name']}\n\n"
        md += f"{entry['emoji']} {entry['welcome_message']} \n"
        md += f"\n```\n{entry['instructions']}\n``` \n"
        md += f"\n[↑ Go Back](#assistants)\n"
    return md


def update_readme():
    readme_file = pathlib.Path(__file__).parent.resolve().joinpath("README.md")
    start = '[//]: # (START-contents)'
    end = '[//]: # (END-contents)'
    with open(readme_file) as f:
        readme_stub = f.read()
    toc_str = get_assistants_markdown()
    readme = replace_text_between(readme_stub, start, end, "\n"+toc_str+"\n\n")
    if readme_stub != readme:
        with open(readme_file, 'w') as f:
            f.write(readme)
    else:
        logger.info('README.md is up to date.')


if __name__ == "__main__":
    build()
    update_readme()
