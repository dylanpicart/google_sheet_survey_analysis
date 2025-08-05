import pandas as pd
from data.configs import complicated_path

# Load the summary file
df = pd.read_csv(complicated_path)

ignore_columns = [
    "All the time", "A lot of the time", "Sometimes", "Not at all",
    "Very Frequently (every day or almost every day)", "Frequently (several times a week)", "A lot",
    " Rarely (less than once a week) ", "Occasionally (around once a week)", "A little", "Not at All",
    "Agree", "Strongly Agree", "Neither Agree Nor Disagree", "Neither", "Disagree", "Strongly Disagree",
    "Yes", "Maybe", "No", "Raw Question", "Canonical Question", "Column", "Question"
]

row_name = "Adults from Partnership with Children have provided or helped me this year with:"
row = df[df["Question"] == row_name]

if row.empty:
    print(f"No row found for: {row_name}")
else:
    option_counts = {}
    for col in row.columns:
        if col in ignore_columns:
            continue
        val = row.iloc[0][col]
        try:
            v = float(val)
            # Split the column header on commas
            for opt in col.split(","):
                opt_clean = opt.strip()
                if not opt_clean:
                    continue
                option_counts[opt_clean] = option_counts.get(opt_clean, 0) + int(v)
        except (ValueError, TypeError):
            continue

    result = pd.DataFrame({
        "Option": list(option_counts.keys()),
        "Count": list(option_counts.values())
    }).sort_values("Option").reset_index(drop=True)
    result.to_csv("data/processed/partnership_multiselect_option_counts.csv", index=False)
    print("Saved tally to: data/processed/partnership_multiselect_option_counts.csv")
    print(result)
