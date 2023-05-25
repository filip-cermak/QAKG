import pytest
import RACE_chat_gpt


@pytest.mark.parametrize("string, expected_result", [
    ('Based on the given context, the correct option is: D: We walk to the park. The passage states, \"We can go to the park on foot,\" indicating that the group of people in the passage goes to the park by walking.', "D"),
    ("The correct option is: A: It's Sunday today.", "A"),
    ("The correct option is D: Wang Hao is in Beijing now.", "D"),
    ("Based on the given information, the correct option is: C: There are five people in Mike's family. The passage states that Mike lives with his parents and his two sisters in New York. Therefore, including Mike himself, there are five people in his family.", "C"),
    ("The correct option is B: There are six people in Mike's family.", "B")
])

def test_augment_punctuation(string, expected_result):
    assert RACE_chat_gpt.extract_answer(string) == expected_result

