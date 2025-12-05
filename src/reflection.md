# Reflection: Data Cleaning & GitHub Copilot

## What Copilot Generated

For this project, I used GitHub Copilot to help with a few of the functions in `src/data_cleaning.py`. In particular, Copilot generated the initial versions of:

- `load_data(file_path: str) -> pd.DataFrame`
- `handle_missing_values(df: pd.DataFrame) -> pd.DataFrame`

To trigger Copilot, I first wrote descriptive comments above each function explaining what it should do. For example, I wrote a comment about loading a CSV file into a pandas DataFrame and then typed the function signature. After I pressed Enter, Copilot suggested the body of the function, including `pd.read_csv(file_path)` and returning the DataFrame. I did something similar for the function that handles missing values: I described “handling missing price and quantity values in a consistent way,” wrote the function header, and Copilot suggested using `dropna` on those columns.

## What I Modified

I did not accept Copilot’s suggestions exactly as they were. I made several changes to better fit the assignment and make the code more robust and readable:

- I added docstrings that describe the purpose, parameters, and return values for each function, so someone else can quickly understand what the code does.
- I added checks in both functions to make sure the expected columns (`"price"` and `"quantity"`) exist before trying to clean them. If they are missing, the function raises a clear `KeyError` instead of failing silently.
- I added a `copy()` call in the cleaning functions to avoid modifying the original DataFrame in place, which makes the behavior more predictable.
- I added comments explaining *why* we drop rows with missing values (because we can’t compute sales correctly without both price and quantity) and why negative values are treated as invalid.

These changes were needed so the code aligned with the project’s goals: readable, professional, and safe to show to someone like a recruiter or classmate.

## What I Learned

From the data cleaning side, I learned how much value you can get just from simple, consistent steps: standardizing column names, stripping whitespace from product names and categories, dropping rows with missing prices or quantities, and removing negative values. Even basic rules like “no negative quantity” and “no missing price” dramatically improve data quality and make later analysis more trustworthy.

From the Copilot side, I learned that it is very good at generating boilerplate code and common patterns, especially when I give it clear comments or function signatures. However, it’s not something I can blindly trust. I still had to review the suggestions, decide whether dropping or filling missing values made sense for this context, and add error handling and documentation on top. Copilot got me 60–70% of the way there quickly, but the last part—making decisions and polishing the code—was still my responsibility.

Overall, this assignment helped me practice using AI coding tools responsibly. I saw how Copilot can speed up my workflow while still requiring me to understand the logic, make design choices, and ensure that the final result meets both the technical requirements and the expectations of a professional project.
