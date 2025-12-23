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
try:
    from langchain.chains import LLMChain
    print('LLMChain found in langchain.chains')
except Exception as e:
    print('LLMChain not in langchain.chains:', e)

try:
    from langchain import LLMChain
    print('LLMChain found directly in langchain')
except Exception as e:
    print('LLMChain not directly in langchain:', e)

try:
    from langchain.prompts import PromptTemplate
    print('PromptTemplate found in langchain.prompts')
except Exception as e:
    print('PromptTemplate not in langchain.prompts:', e)

try:
    from langchain import PromptTemplate
    print('PromptTemplate found directly in langchain')
except Exception as e:
    print('PromptTemplate not directly in langchain:', e)
