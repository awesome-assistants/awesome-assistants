from main import AwesomeAssistantsBuilder


def test_awesome_assistants():
    aww = AwesomeAssistantsBuilder({})
    all_assistants = aww.get_assistants()
    assert isinstance(all_assistants, list)
    for x in all_assistants:
        assert x["id"]
        assert x["emoji"]
        assert x["name"]
        assert x["welcome_message"]
        assert x["parse_mode"]
        if x["id"] != "empty":
            assert x["instructions"]

    assistant = aww.get_assistant("assistant")
    assert isinstance(assistant, dict)
