import pandas as pd
from scripts.transform.map_overarch import (
    map_overarching_workflow,
    build_canonical_to_overarching,
    add_overarching,
)

def test_map_overarching_workflow(tmp_path):
    # Create minimal dummy audit files for younger and older
    audit_younger = tmp_path / "audit_younger.csv"
    audit_older = tmp_path / "audit_older.csv"
    pd.DataFrame({
        "Raw Question": [
            "How safe do you feel? [Safety]",
            "Is there an adult you trust? [Trusted Adult]"
        ]
    }).to_csv(audit_younger, index=False)
    pd.DataFrame({
        "Raw Question": [
            "I feel connected [Connection]",
            "Adults talk about race [Race]"
        ]
    }).to_csv(audit_older, index=False)

    # Create minimal dummy summary files for younger and older
    summary_younger = tmp_path / "summary_younger.csv"
    summary_older = tmp_path / "summary_older.csv"
    pd.DataFrame({
        "Canonical Question": ["safety", "trusted adult"],
        "SomeCol": [1, 2]
    }).to_csv(summary_younger, index=False)
    pd.DataFrame({
        "Canonical Question": ["connection", "race"],
        "SomeCol": [3, 4]
    }).to_csv(summary_older, index=False)

    output_file = tmp_path / "canon_to_over.csv"

    # Call workflow
    out_df = map_overarching_workflow(
        summary_younger=str(summary_younger),
        summary_older=str(summary_older),
        audit_younger=str(audit_younger),
        audit_older=str(audit_older),
        output_file=str(output_file)
    )

    # Check output file exists and correct columns
    assert output_file.exists()
    df_out = pd.read_csv(output_file)
    assert "Canonical Question" in df_out.columns
    assert "Overarching" in df_out.columns
    # Check expected mappings are present
    expected = {
        "safety": "how safe do you feel?",
        "trusted adult": "is there an adult you trust?",
        "connection": "i feel connected",
        "race": "adults talk about race"
    }
    out_map = dict(zip(df_out["Canonical Question"], df_out["Overarching"]))
    for k, v in expected.items():
        assert out_map.get(k) == v
