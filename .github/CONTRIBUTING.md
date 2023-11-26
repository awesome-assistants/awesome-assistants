# Contribution Guidelines

Please ensure your pull request adheres to the following guidelines:

- Search previous suggestions before making a new one, as yours may be a duplicate.
- Additions should be added alphabetically to the relevant category.
- New categories, or improvements to the existing categorization are welcome.
- Use the following format: [assistants](../assistants.yml) - Description.
- Keep descriptions short and simple, but descriptive.
- Make an individual pull request for each suggestion.
- The pull request should have a useful title and include a link to the package and why it should be included.
- Comply with [OpenAI Assistant](https://platform.openai.com/docs/assistants/overview/) API

Thank you for your suggestions!

## Assistant object

https://platform.openai.com/docs/api-reference/assistants/object

```json    
    {
      "id": "asst_abc123",
      "object": "assistant",
      "created_at": 1698984975,
      "name": "Math Tutor",
      "description": null,
      "model": "gpt-4",
      "instructions": "You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
      "tools": [
        {
          "type": "code_interpreter"
        }
      ],
      "file_ids": [],
      "metadata": {}
    }
```