import os
import pandas as pd

# Load consolidated files with Overarching already present
df_younger = pd.read_csv("data/processed/consolidated_questions_younger.csv")
df_older = pd.read_csv("data/processed/consolidated_questions_older.csv")

# Combine both
df_all = pd.concat([df_younger, df_older], ignore_index=True)

fixed_cols = ['School Year', 'Canonical Question', 'Overarching']
response_cols = [col for col in df_all.columns if col not in fixed_cols]

# Group by canonical question, sum all response columns
totals = df_all.groupby('Canonical Question', as_index=False)[response_cols].sum(numeric_only=True)
totals = totals.sort_values("Canonical Question").reset_index(drop=True)

# --- Merge back Overarching column ---
# Use the unique mapping from original dataframe
canon_to_over_df = df_all[['Canonical Question', 'Overarching']].drop_duplicates('Canonical Question')
totals = totals.merge(canon_to_over_df, on='Canonical Question', how='left')

# Optional: Move Overarching to the end
cols = [col for col in totals.columns if col != "Overarching"] + ["Overarching"]
totals = totals[cols]

for col in response_cols:
    if col in totals.columns:
        totals[col] = totals[col].astype(int)

# Save result
output_path = os.path.abspath("data/processed/canonical_question_totals.csv")
totals.to_csv(output_path, index=False)
print(f"Saved totals to: {output_path}")
