import tablib
import yaml
import pathlib
import logging
import argparse

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class AwesomeAssistantsBuilder:
    def __init__(self, config):
        self.config = config

    def run(self):
        if self.config.export:
            self.build()
        if self.config.update_readme:
            self.update_readme()

    def get_assistants(self):
        assistants_yml = pathlib.Path(__file__).parent.resolve().joinpath("assistants.yml")
        with open(assistants_yml, 'r') as f:
            assistants = yaml.safe_load(f)
        return assistants

    def get_assistant(self, search_id):
        for x in self.get_assistants():
            if x['id'] == search_id:
                break
        else:
            x = None
        return x

    def build(self):
        assistants = self.get_assistants()
        dataset = tablib.Dataset()
        dataset.headers = ['id', 'name', 'emoji', 'welcome_message', 'instructions', 'parse_mode']
        for entry in assistants:
            logger.debug(entry['id'])
            dataset.append([entry['id'],
                            entry['name'],
                            entry['emoji'],
                            entry['welcome_message'],
                            entry['instructions'],
                            entry['parse_mode']])

        self.to_file(dataset, 'csv')
        self.to_file(dataset, 'yaml')
        self.to_file(dataset, 'json')
        self.to_file(dataset, 'html')
        self.to_file(dataset, 'latex')
        self.to_file(dataset, 'tsv')

    @staticmethod
    def to_file(dataset, format, bin='w'):
        data = dataset.export(format)
        with open(f'build/assistants.{format}', bin) as file:
            file.write(data)

    @staticmethod
    def replace_text_between(original_text, delimiter_a, delimiter_b, replacement_text):
        leading_text = original_text.split(delimiter_a)[0]
        trailing_text = original_text.split(delimiter_b)[1]
        return leading_text + delimiter_a + replacement_text + delimiter_b + trailing_text

    def get_assistants_markdown(self):
        assistants = self.get_assistants()
        md = ""
        md += "\n" + "Total assistants: **" + str(len(assistants)) + "** \n\n"
        md += "".join(
            f"1. [{entry['emoji']} {entry['name']}](#{entry['id'].replace('_', '-')})\n"
            for entry in assistants
        )
        for entry in assistants:
            md += f"\n ### {entry['name']}\n\n"
            md += f"{entry['emoji']} {entry['welcome_message']} \n"
            md += f"\n```\n{entry['instructions']}\n``` \n"
            md += f"\n[↑ Go Back](#assistants)\n"
        return md

    def update_readme(self):
        readme_file = pathlib.Path(__file__).parent.resolve().joinpath("README.md")
        readme_stub = pathlib.Path(readme_file).read_text()
        start = '[//]: # (START-contents)'
        end = '[//]: # (END-contents)'
        toc_str = self.get_assistants_markdown()
        readme = self.replace_text_between(readme_stub, start, end, "\n" + toc_str + "\n\n")
        if readme_stub != readme:
            with open(readme_file, 'w') as f:
                f.write(readme)
        else:
            logger.info('README.md is up to date.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--export", dest="export",
                        default=True, action='store_true', help="Build files")
    parser.add_argument("-ur", "--update-readme", dest="update_readme",
                        default=True, action='store_true', help="Update README.md file")
    aww = AwesomeAssistantsBuilder(parser.parse_args())
    aww.run()
