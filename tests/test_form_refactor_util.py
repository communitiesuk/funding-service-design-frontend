import pytest
from scripts import form_refactor_util


@pytest.mark.parametrize(
    "mutation_key", list(form_refactor_util._MUTATIONS.keys())
)
def test_mutation_function(mutation_key, tmpdir):
    input_json = open(
        f"tests/form_refactor_util/{mutation_key}-input.json",
        "r",
        encoding="utf-8",
    ).read()
    expected_json = open(
        f"tests/form_refactor_util/{mutation_key}-expected.json",
        "r",
        encoding="utf-8",
    ).read()

    test_file = tmpdir.join(f"test-{mutation_key}.json")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(input_json)

    retv = form_refactor_util.main(
        (
            mutation_key,
            "--dir",
            str(tmpdir),
        )
    )

    assert retv == 0
    assert test_file.read() == expected_json
