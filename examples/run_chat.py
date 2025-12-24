"""Example showing direct usage of `OllamaLLM` and using it with LangChain.

Run:
    python examples/run_chat.py
"""

import os
import sys

from dotenv import load_dotenv

# Import local package lazily inside the example functions to avoid modifying
# sys.path at import time and to keep flake8 happy.

# Load environment variables from .env at repository root (optional)
load_dotenv()


def direct_example():
    print("Direct example:")
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
    resp = (
        llm._call("Say hello in one sentence.")
        if hasattr(llm, "_call")
        else llm.generate_text("Say hello in one sentence.")
    )
    print(resp)


def langchain_example():
    print("\nLangChain example:")
    model = os.environ.get("OLLAMA_MODEL")
    if not model:
        print(
            "OLLAMA_MODEL is not set. Copy .env.example to .env and set "
            "OLLAMA_MODEL to your model name, then re-run this example."
        )
        return

    try:
        from langchain import LLMChain, PromptTemplate

        # Import OllamaLLM lazily so this example works without an editable install
        try:
            from langchain_ollama.ollama_wrapper import OllamaLLM
        except Exception:
            repo_root = os.path.dirname(os.path.dirname(__file__))
            sys.path.insert(0, os.path.join(repo_root, "src"))
            from langchain_ollama.ollama_wrapper import OllamaLLM

        # Some LangChain versions expect the model to follow their LLM base API
        llm = OllamaLLM(model=model)
        prompt = PromptTemplate("{input}", input_variables=["input"])
        chain = LLMChain(llm=llm, prompt=prompt)
        prompt_text = "Write a short haiku about coding."
        input_dict = {"input": prompt_text}
        out = chain.run(input_dict)
        print(out)
    except Exception as e:
        print("LangChain example failed: possible missing LangChain or API mismatch", e)


if __name__ == "__main__":
    direct_example()
    langchain_example()
