import pytest
from unittest.mock import MagicMock, patch
from google.genai import types
from src.agent import agent_loop

_REAL_PART = types.Part(text="model response")


@pytest.fixture
def args():
    a = MagicMock()
    a.verbose = False
    a.user_prompt = "do something"
    return a


def _make_response(text=None, function_calls=None, candidates=None):
    response = MagicMock()
    response.text = text
    response.function_calls = function_calls or []
    response.candidates = candidates or []
    response.usage_metadata = MagicMock(
        prompt_token_count=10, candidates_token_count=5
    )
    return response


def _make_tool_result(name="get_files_info", response_value="ok"):
    part = types.Part.from_function_response(name=name, response={"result": response_value})
    content = MagicMock(spec=types.Content)
    content.parts = [part]
    return content


def _make_fc(name="get_files_info"):
    fc = MagicMock()
    fc.name = name
    return fc


@patch("src.agent.LOOPS", 3)
@patch("src.agent.call_function")
@patch("src.agent.Client")
def test_final_response_no_function_calls(mock_client, mock_call_fn, args, capsys):
    mock_client.return_value.models.generate_content.return_value = _make_response(
        text="All done!"
    )
    result = agent_loop([MagicMock()], args)
    assert result is None
    assert "All done!" in capsys.readouterr().out


@patch("src.agent.LOOPS", 3)
@patch("src.agent.call_function")
@patch("src.agent.Client")
def test_one_tool_call_then_done(mock_client, mock_call_fn, args):
    fc = _make_fc()
    candidate = MagicMock()
    candidate.content = MagicMock()
    candidate.content.parts = [_REAL_PART]

    first_response = _make_response(
        function_calls=[fc], candidates=[candidate]
    )
    second_response = _make_response(text="Done")
    mock_client.return_value.models.generate_content.side_effect = [
        first_response, second_response
    ]
    mock_call_fn.return_value = _make_tool_result()

    result = agent_loop([MagicMock()], args)
    assert result is None
    assert mock_client.return_value.models.generate_content.call_count == 2


@patch("src.agent.LOOPS", 3)
@patch("src.agent.call_function")
@patch("src.agent.Client")
def test_loop_exhaustion(mock_client, mock_call_fn, args, capsys):
    fc = _make_fc()
    candidate = MagicMock()
    candidate.content = MagicMock()
    candidate.content.parts = [_REAL_PART]

    mock_client.return_value.models.generate_content.return_value = _make_response(
        function_calls=[fc], candidates=[candidate]
    )
    mock_call_fn.return_value = _make_tool_result()

    result = agent_loop([MagicMock()], args)
    assert result == 1
    assert "Error" in capsys.readouterr().out


@patch("src.agent.LOOPS", 3)
@patch("src.agent.call_function")
@patch("src.agent.Client")
def test_empty_parts_raises(mock_client, mock_call_fn, args):
    fc = _make_fc()
    candidate = MagicMock()
    candidate.content = MagicMock()
    candidate.content.parts = [_REAL_PART]

    mock_client.return_value.models.generate_content.return_value = _make_response(
        function_calls=[fc], candidates=[candidate]
    )
    bad_result = MagicMock(spec=types.Content)
    bad_result.parts = []
    mock_call_fn.return_value = bad_result

    with pytest.raises(Exception, match="parts list is empty"):
        agent_loop([MagicMock()], args)


@patch("src.agent.LOOPS", 3)
@patch("src.agent.call_function")
@patch("src.agent.Client")
def test_invalid_response_raises(mock_client, mock_call_fn, args):
    fc = _make_fc()
    candidate = MagicMock()
    candidate.content = MagicMock()
    candidate.content.parts = [_REAL_PART]

    mock_client.return_value.models.generate_content.return_value = _make_response(
        function_calls=[fc], candidates=[candidate]
    )
    part = MagicMock()
    part.function_response = None
    bad_result = MagicMock(spec=types.Content)
    bad_result.parts = [part]
    mock_call_fn.return_value = bad_result

    with pytest.raises(Exception, match="invalid response"):
        agent_loop([MagicMock()], args)


@patch("src.agent.LOOPS", 3)
@patch("src.agent.call_function")
@patch("src.agent.Client")
def test_verbose_mode(mock_client, mock_call_fn, args, capsys):
    args.verbose = True
    mock_client.return_value.models.generate_content.return_value = _make_response(
        text="Done verbosely"
    )
    agent_loop([MagicMock()], args)
    out = capsys.readouterr().out
    assert "Prompt tokens" in out
    assert "Response tokens" in out
