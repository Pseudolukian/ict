from ..core.data_structures.OneCloud.API_KEY import API_key, IncorrectApiKey
from unittest.mock import MagicMock, patch
import random, string, os
import pytest

def key_generator(key_status: str = "correct") -> str:
    correct_lenght = 64
    incorrect_lenght = [char for char in str(random.randint(20, 80)) if char != 64]
    
    if key_status == "correct":
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=correct_lenght))
        return key
    elif key_status == "incorrect":
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=int(incorrect_lenght[0])))
        return key
    
def test_incorrect_key():
    incorrect_key = "q" * 63

    with patch("API_key.input_key", MagicMock(return_value="q" * 64)):
        with pytest.raises(IncorrectApiKey):
            api_key_instance = API_key(API_key=incorrect_key)

def test_correct_key():
    correct_key = "q" * 64
    api_key_instance = API_key(API_key=correct_key)

    assert str(api_key_instance) == correct_key, "API_key instance should store the correct key."
    assert os.environ["API_KEY"] == correct_key, "API_KEY environment variable should store the correct key."