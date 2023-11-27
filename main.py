import tablib
import yaml
import pathlib
import logging
import argparse
import re

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
        if self.config.parse_prompts_folder:
            d = self.parse_prompts_folder()
            with open(f'build/for-import.yml', 'w') as file:
                file.write(yaml.dump(d))

    def get_assistants(self):
        assistants_yml = pathlib.Path(__file__).parent.resolve().joinpath("assistants.yml")
        with open(assistants_yml, 'r') as f:
            assistants = yaml.safe_load(f)
        return assistants

    def build(self):
        assistants = self.get_assistants()
        dataset = tablib.Dataset()
        dataset.headers = ['id', 'name', 'emoji', 'welcome_message', 'instructions', 'parse_mode']
        for key, entry in assistants.items():
            dataset.append([key, entry['name'], entry['emoji'], entry['welcome_message'], entry['instructions'],
                            entry['parse_mode']])

        self.to_file(dataset, 'csv')
        self.to_file(dataset, 'yaml')
        self.to_file(dataset, 'json')
        self.to_file(dataset, 'html')
        self.to_file(dataset, 'latex')
        self.to_file(dataset, 'tsv')

    # Method was used to parse prompts from https://github.com/LouisShark/chatgpt_system_prompt/tree/main/prompts/gpts
    # used one time, but might be used in the future
    def parse_prompts_folder(self):
        dataset = []

        assistants = pathlib.Path(__file__).parent.joinpath("prompts")
        files = [f for f in assistants.iterdir() if f.is_file()]
        for file in files:
            with open(file, 'r') as f:
                if file.name.startswith('.'):
                    continue

                # logger.info('Processing assistant: %s', f.name)
                i = f.read()

                # Extract URL from a string
                url_extract_pattern = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)|$"
                links = re.findall(url_extract_pattern, i)
                id = file.stem.replace(' ', '_').lower()
                name = file.stem.replace('_', ' ').title()
                welcome = f"Hi, I am <b>{name}</b>. How can I help you?"
                i = self.find_between(i, '```markdown', '```')

                # skip agents that have ads inside
                content_link = re.findall(url_extract_pattern, i)[0]
                if content_link != '':
                    continue

                dataset.append([{'id': id,
                                'name': name,
                                'emoji': "🤖",
                                'instructions': i,
                                'welcome_message': welcome,
                                'parse_mode': 'markdown',
                                'category': 'gpt'
                                }])

        logger.info('Processed %s assistants', len(dataset))
        return dataset

    @staticmethod
    def to_file(dataset, format, bin='w'):
        data = dataset.export(format)
        with open(f'build/assistants.{format}', bin) as file:
            file.write(data)

    @staticmethod
    def find_between(s, start, end):
        return s.split(start)[1].split(end)[0].strip()

    @staticmethod
    def replace_text_between(original_text, delimiter_a, delimiter_b, replacement_text):
        leading_text = original_text.split(delimiter_a)[0]
        trailing_text = original_text.split(delimiter_b)[1]
        return leading_text + delimiter_a + replacement_text + delimiter_b + trailing_text

    def get_assistants_markdown(self):
        assistants = self.get_assistants()
        md = ""
        for key, entry in assistants.items():
            md += f"- [{entry['emoji']} {entry['name']}](#{key.replace('_', '-')})\n"

        for key, entry in assistants.items():
            md += f"\n ### {entry['name']}\n\n"
            md += f"{entry['emoji']} {entry['welcome_message']} \n"
            md += f"\n```\n{entry['instructions']}\n``` \n"
            md += f"\n[↑ Go Back](#assistants)\n"
        return md

    def update_readme(self):
        readme_file = pathlib.Path(__file__).parent.resolve().joinpath("README.md")
        start = '[//]: # (START-contents)'
        end = '[//]: # (END-contents)'
        with open(readme_file) as f:
            readme_stub = f.read()
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
                        default=False, action='store_true', help="Build files")
    parser.add_argument("-ur", "--update-readme", dest="update_readme",
                        default=False, action='store_true', help="Update README.md file")
    parser.add_argument("-ppf", "--parse-prompts-folder", dest="parse_prompts_folder",
                        default=False, action='store_true', help="One time method")
    aww = AwesomeAssistantsBuilder(parser.parse_args())
    aww.run()
