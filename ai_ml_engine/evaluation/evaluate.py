from pathlib import Path

import pandas as pd


DATA_PATH = Path(
    "ai_ml_engine/data/processed/training_dataset.csv"
)


def generate_report():

    df = pd.read_csv(
        DATA_PATH
    )

    print("=" * 60)
    print("FORGE_X AI — ML DATASET REPORT")
    print("=" * 60)

    print(
        "\nDataset shape:",
        df.shape
    )

    print(
        "\nTarget distribution:"
    )

    print(
        df["target"]
        .value_counts()
    )

    print(
        "\nTarget percentage:"
    )

    print(
        (
            df["target"]
            .value_counts(
                normalize=True
            )
            * 100
        ).round(2)
    )

    print(
        "\nMissing values:"
    )

    missing = (
        df.isnull()
        .sum()
        .sort_values(
            ascending=False
        )
    )

    print(
        missing[
            missing > 0
        ]
    )

    numeric = df.select_dtypes(
        include="number"
    )

    print(
        "\nCorrelation with target:"
    )

    print(
        numeric.corr()["target"]
        .sort_values(
            ascending=False
        )
    )

    print(
        "\nDataset quality check:"
    )

    print(
        "Duplicate rows:",
        df.duplicated().sum()
    )

    print(
        "Rows:",
        len(df)
    )

    print(
        "\nREPORT COMPLETE"
    )


if __name__ == "__main__":
    generate_report()