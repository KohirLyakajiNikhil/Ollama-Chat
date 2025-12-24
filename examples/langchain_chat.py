"""Example showing a minimal LangChain integration using the Ollama wrapper.

This example attempts to use LangChain's LLM base class wrapper defined in
`src/langchain_ollama/ollama_wrapper.py`. Depending on your LangChain version,
this may work out-of-the-box or require small API adjustments.
"""


import os
import sys
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate




def run_example():

    load_dotenv()
    model = os.environ.get("OLLAMA_MODEL")
    if not model:
        print(
            "OLLAMA_MODEL is not set. Copy .env.example to .env and set "
            "OLLAMA_MODEL to your model name, then re-run this example."
        )
        return
    # Import locally so running examples directly works without an editable
    # install. If the import fails, add `src/` to sys.path and retry once.
    try:
        from langchain_ollama.ollama_wrapper import OllamaLLM
    except Exception:
        repo_root = os.path.dirname(os.path.dirname(__file__))
        sys.path.insert(0, os.path.join(repo_root, "src"))
        from langchain_ollama.ollama_wrapper import OllamaLLM
    llm = OllamaLLM(model=model)
    print("Contextual LangChain chat agent. Type 'exit' to quit.")
    history = []  # List of (user, assistant) message tuples
    prompt = PromptTemplate.from_template("""{context}Assistant:""")
    while True:
        user_input = input("User: ")
        if user_input.strip().lower() in ("exit", "quit"):
            break
        history.append(("user", user_input))
        # Build context string
        context = ""
        for role, msg in history:
            if role == "user":
                context += f"User: {msg}\n"
            else:
                context += f"Assistant: {msg}\n"
        # Compose prompt with context using PromptTemplate
        prompt_text = prompt.format(context=context)
        out = llm(prompt_text)
        print("Model:", out)
        history.append(("assistant", out))


if __name__ == "__main__":
    run_example()
