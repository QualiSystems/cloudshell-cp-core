import pytest

from cloudshell.cp.core.utils.name_generator import NameGenerator


def test_name_generator():
    generate_name = NameGenerator()

    assert generate_name("test").startswith("test-")
    assert generate_name("test", "postfix") == "test-postfix"
    assert generate_name("x" * 101).startswith("x" * 91 + "-")


def test_name_generator_postfix_is_too_long():
    generate_name = NameGenerator(max_length=10)
    with pytest.raises(ValueError):
        generate_name("test", "postfix-too-long")
