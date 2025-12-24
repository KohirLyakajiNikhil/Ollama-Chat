"""Example showing direct usage of `OllamaLLM` and using it with LangChain.

Run:
    python examples/run_chat.py
"""

import os

from dotenv import load_dotenv

from langchain_ollama.ollama_wrapper import OllamaLLM

# Load environment variables from .env at repository root (optional)
load_dotenv()


def direct_example():
    print("Direct example:")
    model = os.environ.get("OLLAMA_MODEL")
    if not model:
        print(
            "OLLAMA_MODEL is not set. Copy .env.example to .env and set OLLAMA_MODEL to your model name, then re-run this example."
        )
        return

    llm = OllamaLLM(model=model)
    resp = (
        llm._call("Say hello in one sentence.")
        if hasattr(llm, "_call")
        else llm.generate_text("Say hello in one sentence.")
    )
    print(resp)


def langchain_example():
    print("\nLangChain example:")
    try:
        from langchain import LLMChain, PromptTemplate

        # Some LangChain versions expect the model to follow their LLM base API
        llm = OllamaLLM(model="test-model")
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
