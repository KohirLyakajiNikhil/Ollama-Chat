def test_extract_from_verbose_repr():
    from langchain_ollama.ollama_wrapper import _extract_assistant_content

    sample = (
        "model='gemma3:latest' created_at='2025-12-24T06:52:44.6682627Z' done=True "
        "done_reason='stop' total_duration=9359118400 load_duration=4685449200 "
        "prompt_eval_count=10 prompt_eval_duration=1862828100 eval_count=54 eval_duration=2716643400 "
        "message=Message(role='assistant', content='Hello there! How\u2019s your day going so far? "
        "Is there anything I can help you with today? 😊 \n\nDo you want to:\n\n*   Chat about something?\n*   Get information on a topic?\n*   Play a game?', thinking=None, images=None, tool_name=None, tool_calls=None) logprobs=None"
    )

    extracted = _extract_assistant_content(sample)
    assert "Hello there!" in extracted
    assert "Chat about something?" in extracted
