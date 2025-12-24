# Quick script to introspect LangChain package
import importlib

candidates = [
    "langchain.chains.llm",
    "langchain.chains",
    "langchain",
]

for c in candidates:
    try:
        m = importlib.import_module(c)
        print(f"Imported {c}: {m}")
    except Exception as e:
        print(f"Failed to import {c}: {e}")

# Try to import LLMChain and PromptTemplate from likely locations
for name, attr in [
    ("langchain.chains", "LLMChain"),
    ("langchain", "LLMChain"),
]:
    try:
        mod = importlib.import_module(name)
        if hasattr(mod, attr):
            print(f"{attr} found in {name}")
    except Exception as e:
        print(f"Failed to import {name}: {e}")

for name, attr in [
    ("langchain.prompts", "PromptTemplate"),
    ("langchain", "PromptTemplate"),
]:
    try:
        mod = importlib.import_module(name)
        if hasattr(mod, attr):
            print(f"{attr} found in {name}")
    except Exception as e:
        print(f"Failed to import {name}: {e}")
