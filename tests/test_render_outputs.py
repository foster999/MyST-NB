from unittest.mock import patch

from importlib_metadata import EntryPoint
import pytest

from myst_nb.render_outputs import load_renderer, MystNbEntryPointError


def test_load_renderer_not_found():
    with pytest.raises(MystNbEntryPointError):
        load_renderer("other")


@patch.object(EntryPoint, "load", lambda self: EntryPoint)
def test_load_renderer_not_subclass():
    with pytest.raises(MystNbEntryPointError):
        load_renderer("default")


@pytest.mark.sphinx_params("basic_run.ipynb", conf={"jupyter_execute_notebooks": "off"})
def test_basic_run(sphinx_run, file_regression):
    sphinx_run.build()
    assert sphinx_run.warnings() == ""
    doctree = sphinx_run.get_resolved_doctree("basic_run")
    file_regression.check(doctree.pformat(), extension=".xml")


@pytest.mark.sphinx_params(
    "complex_outputs.ipynb", conf={"jupyter_execute_notebooks": "off"}
)
def test_complex_outputs(sphinx_run, file_regression):
    sphinx_run.build()
    assert sphinx_run.warnings() == ""
    doctree = sphinx_run.get_resolved_doctree("complex_outputs")
    file_regression.check(doctree.pformat().replace(".jpeg", ".jpg"), extension=".xml")


@pytest.mark.sphinx_params(
    "complex_outputs.ipynb",
    conf={"jupyter_execute_notebooks": "off"},
    buildername="latex",
)
def test_complex_outputs_latex(sphinx_run, file_regression):
    sphinx_run.build()
    assert sphinx_run.warnings() == ""
    doctree = sphinx_run.get_resolved_doctree("complex_outputs")
    file_regression.check(doctree.pformat().replace(".jpeg", ".jpg"), extension=".xml")


@pytest.mark.sphinx_params(
    "basic_stderr.ipynb", conf={"jupyter_execute_notebooks": "off"}
)
def test_stderr_tag(sphinx_run, file_regression):
    sphinx_run.build()
    assert sphinx_run.warnings() == ""
    doctree = sphinx_run.get_resolved_doctree("basic_stderr")
    file_regression.check(doctree.pformat(), extension=".xml")


@pytest.mark.sphinx_params(
    "basic_stderr.ipynb",
    conf={"jupyter_execute_notebooks": "off", "nb_output_stderr": "remove"},
)
def test_stderr_remove(sphinx_run, file_regression):
    sphinx_run.build()
    assert sphinx_run.warnings() == ""
    doctree = sphinx_run.get_resolved_doctree("basic_stderr")
    file_regression.check(doctree.pformat(), extension=".xml")


@pytest.mark.sphinx_params(
    "metadata_image.ipynb",
    conf={"jupyter_execute_notebooks": "off", "nb_render_key": "myst"},
)
def test_metadata_image(sphinx_run, file_regression):
    sphinx_run.build()
    assert sphinx_run.warnings() == ""
    doctree = sphinx_run.get_resolved_doctree("metadata_image")
    file_regression.check(doctree.pformat().replace(".jpeg", ".jpg"), extension=".xml")


# @pytest.mark.sphinx_params(
#     "unknown_mimetype.ipynb", conf={"jupyter_execute_notebooks": "off"}
# )
# def test_unknown_mimetype(sphinx_run, file_regression):
#     sphinx_run.build()
#     warning = (
#         "unknown_mimetype.ipynb.rst:10002: WARNING: MyST-NB: "
#         "output contains no MIME type in priority list"
#     )
#     assert warning in sphinx_run.warnings()
#     doctree = sphinx_run.get_resolved_doctree("unknown_mimetype")
#     file_regression.check(doctree.pformat(), extension=".xml")
