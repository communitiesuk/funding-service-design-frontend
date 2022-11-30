import pytest
from invoke import MockContext
from invoke import Result
from tasks import fix_trans_tags


@pytest.mark.parametrize(
    "input, expected",
    [
        pytest.param(
            "{% trans %}\n\n Random\nString\tExample \n\n{% endtrans %}",
            "\n\n {% trans %}Random String Example{% endtrans %} \n\n",
        ),
        pytest.param(
            "<html>{% trans %}\n\n Random\nString\tExample \n\n{% endtrans"
            " %}</html>",
            "<html>\n\n {% trans %}Random String Example{% endtrans %}"
            " \n\n</html>",
        ),
        pytest.param(
            "\n{% trans %}\nNew\nline\n{% endtrans"
            " %}\n{%trans%}\nA\ntab\t{%endtrans%}",
            "\n\n{% trans %}New line{% endtrans %}\n\n\n{%trans%}A"
            " tab{%endtrans%}\t",
        ),
    ],
)
def test_remove_whitespace_newlines_from_trans_tags_file(
    tmpdir, input, expected
):
    c = MockContext(run=Result("Darwin\n"))

    f = tmpdir.join("f.html")
    f.write(input)

    assert fix_trans_tags(c, f.strpath) == 0

    assert f.read() == expected


def test_remove_whitespace_newlines_from_trans_tags_dir(tmpdir):
    c = MockContext(run=Result("Darwin\n"))

    f = tmpdir.join("f.html")
    f.write("{% trans %}a\nb{% endtrans %}")

    assert fix_trans_tags(c, str(tmpdir)) == 0

    assert f.read() == "{% trans %}a b{% endtrans %}"
