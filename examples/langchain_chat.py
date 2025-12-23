"""Example showing a minimal LangChain integration using the Ollama wrapper.

This example attempts to use LangChain's LLM base class wrapper defined in
`src/langchain_ollama/ollama_wrapper.py`. Depending on your LangChain version,
this may work out-of-the-box or require small API adjustments.
"""

import os

from dotenv import load_dotenv

# LangChain import compatibility across versions — do not raise on failure.
HAVE_LANGCHAIN = False
LLMChain = None
PromptTemplate = None
_lc_import_errors = []

# Try multiple import locations for LLMChain
try:
    from langchain.chains import LLMChain  # type: ignore

    HAVE_LANGCHAIN = True
except Exception as exc:
    _lc_import_errors.append(exc)
    try:
        from langchain import LLMChain  # type: ignore

        HAVE_LANGCHAIN = True
    except Exception as exc2:
        _lc_import_errors.append(exc2)

# Try multiple import locations for PromptTemplate
try:
    from langchain.prompts import PromptTemplate  # type: ignore

    HAVE_LANGCHAIN = True
except Exception as exc:
    _lc_import_errors.append(exc)
    try:
        from langchain import PromptTemplate  # type: ignore

        HAVE_LANGCHAIN = True
    except Exception as exc2:
        _lc_import_errors.append(exc2)

from langchain_ollama.ollama_wrapper import OllamaLLM

# Load environment variables from .env at repository root (optional)
load_dotenv()

MODEL = os.environ.get("OLLAMA_MODEL", "llama2")


def run_example():
    llm = OllamaLLM(model=MODEL)

    # If LangChain's LLM base isn't available, fall back to a simple loop that
    # calls the Ollama wrapper directly (it is callable and returns text).
    if "HAVE_LANGCHAIN" in globals() and HAVE_LANGCHAIN:
        prompt = PromptTemplate.from_template(
            "You are a helpful assistant. User: {input}"
        )
        chain = LLMChain(llm=llm, prompt=prompt)

        def _run_input(text: str) -> str:
            return chain.run(text)

    else:
        print(
            "LangChain's LLMChain/PromptTemplate not available — falling back to direct OllamaLLM calls.\n"
            "Install a compatible 'langchain' to use this example with LLMChain, or use 'examples/chat_direct.py'."
        )

        def _run_input(text: str) -> str:
            # OllamaLLM implements __call__ and returns generated text
            return llm(text)

    while True:
        user_input = input("User: ")
        if user_input.strip().lower() in ("exit", "quit"):
            break
        out = _run_input(user_input)
        print("Model:", out)


if __name__ == "__main__":
    run_example()
