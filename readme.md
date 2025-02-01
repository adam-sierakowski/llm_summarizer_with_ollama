# Webpage summarizer with ollama and CLI

This projects generates summaries from documents loaded from URL.

This is largely based on https://github.com/rishabkumar7/langchain-ollama (thanks! 🎩).

Changes I've made:
- *update ollama invoking to fit current langchain documentation*
- add passing arguments to the script from the command line
- add appending detailed output to a .jsonl (jsonlines) file
- add parsing out deepseek's chain of thought (delimited by `<think></think>` markers)

Advantages of access through CLI: you can write an external bash script and call the summarizing module as many times as you like.

# Requirements

Install [Ollama](https://ollama.com/) and download some open-source models (I tested this with `llama3.2`, `deepseek-r1:14b`, `deepseek-r1:8b`, `deepseek-r1:1.5b`).

Set up a virtual environment and install the dependencies from `requirements.txt`.

# Example usage

`python main.py -i 'https://en.wikipedia.org/wiki/Interlocutor_(linguistics)' -o example_output.jsonl -l deepseek-r1:1.5b`

Here's a pretty-printed result of the above command:

```
{
  "url": "https://en.wikipedia.org/wiki/Interlocutor_(linguistics)",
  "model_used": "deepseek-r1:1.5b",
  "chain_of_thought": "<think>\nOkay, I need to summarize this text concisely. The reference materials discuss \"interlocutor\" and \"routelers,\" which are related to language use and quotation techniques. Here's how I can approach it:\n\n1. Start with the main topic.\n2. Mention key terms like interlocutor and routelers.\n3. Note their role in communication, particularly quotation.\n\nSo, a possible summary would be: The reference materials discuss concepts like \"interlocutor\" and \"routelers,\" examining their roles in language use and quoting techniques.\n</think>",
  "summary": "\n\n**Summary:** The references discuss key terms such as \"interlocutor\" and \"routelers,\" focusing on their roles in language use and quotation techniques."
}
```

The result of a few runs with different models is saved in `example_output.jsonl` in this repo.

# TODOs

## 1.

- Add a switch to save the date when the summary was retrieved.
- Add a switch so you can turn on and off the filtering of deepseek's chain of thought

## 2.

The script works despite printing the following errors:

`USER_AGENT environment variable not set, consider setting it to identify your requests.` (always)

`None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.` (sometimes)

`Token indices sequence length is longer than the specified maximum sequence length for this model (1480 > 1024). Running this sequence through the model will result in indexing error` (with some models)

I haven't tested [Rashib's original repo](https://github.com/rishabkumar7/langchain-ollama), but I think it would have the same issues.

