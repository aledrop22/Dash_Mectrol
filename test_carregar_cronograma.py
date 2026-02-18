import shutil
from pathlib import Path

import pytest

from app_qualidade import carregar_dados_cronograma, buscar_arquivo_cronograma


def test_loader_handles_dash_file(tmp_path, monkeypatch):
    """The cronograma loader should pick the correct sheet even when the
    structure differs from the usual quality cronograma (no Transportadora, etc.).

    We simulate the folder lookup by copying the known problematic Excel to a
    temporary directory and patching ``buscar_arquivo_cronograma`` to return it.
    """
    source = Path(__file__).parent / "3.1_DASH_MENSAL_01_26.xlsx"
    assert source.exists(), "sample dash file must be present for the test"

    dest = tmp_path / "cronograma.xlsx"
    shutil.copy(source, dest)

    # patch the lookup so the loader thinks the file lives under some folder
    monkeypatch.setattr(
        "app_qualidade.buscar_arquivo_cronograma",
        lambda pasta: (str(dest), dest.name),
    )

    df, nome = carregar_dados_cronograma()
    assert df is not None and not df.empty
    # basic sanity
    assert "OP" in df.columns
    # the patch should choose the 'Lançamentos' sheet which contains
    # the check-box columns; verify at least one of them is preserved
    assert any(col in df.columns for col in ["RETRABALHO OUTROS DP", "Retrabalho"])
