"""
This module imports the necessary libraries for data processing and visualization.

Modules:
    os: Provides a way of using operating system dependent functionality
    like reading or writing to the file system.
    re: Offers a set of functions that allows us to search a string for
     a match (regular expressions).
    difflib: Provides tools for comparing sequences, especially useful
    for comparing text files.
    pandas: A powerful data manipulation and analysis library for Python.
    Here it's used to read and manipulate Excel data.
    plotly.express: A high-level interface to Plotly, a graphing library.
    It's used for creating interactive plots and visualizations.
    streamlit: A framework for creating web apps in pure Python. Used for
    displaying and interacting with data and visualizations in a web interface.
"""
import os
import re
import difflib
import pandas as pd
import plotly.express as px
import streamlit as st

# Read holiday data from Excel file
dfholiday = pd.read_excel("unlocked holiday.xlsx")
dfholiday2 = pd.read_excel("unlocked holiday.xlsx")

# Styles for cards
directory = os.path.dirname(__file__)
os.chdir(directory)


@st.cache_resource(show_spinner=False)
def process_data(files):
    """
    Process Excel files containing non-PO payment data.

    Args:
    - files (list): List of file paths or file objects (xlsx format)
    containing non-PO payment data.

    Returns:
    - pandas.DataFrame: Concatenated DataFrame containing processed
    non-PO payment data.

    This function reads each Excel file from the provided list, processes them
    into a standardized format,
    and concatenates them into a single DataFrame for further analysis.

    """
    data = pd.read_excel(files)
    df = data.copy()
    filtered_df = df.copy()
    filtered_df["Time"] = pd.to_datetime(
        filtered_df["Time"], format="%H:%M:%S", errors="coerce"
    )
    filtered_df["Updated at"] = pd.to_datetime(
        filtered_df["Updated at"], format="%H:%M:%S", errors="coerce"
    )
    filtered_df["Verified at"] = pd.to_datetime(
        filtered_df["Verified at"], format="%H:%M:%S", errors="coerce"
    )
    filtered_df["HOG Approval at"] = pd.to_datetime(
        filtered_df["HOG Approval at"], format="%H:%M:%S", errors="coerce"
    )
    filtered_df["Doc. Date"] = pd.to_datetime(
        filtered_df["Doc. Date"], errors="coerce")
    filtered_df["Pstng Date"] = pd.to_datetime(
        filtered_df["Pstng Date"], errors="coerce"
    )
    filtered_df["On"] = pd.to_datetime(filtered_df["On"], errors="coerce")
    filtered_df["Updated on"] = pd.to_datetime(
        filtered_df["Updated on"], errors="coerce"
    )
    filtered_df["Verified on"] = pd.to_datetime(
        filtered_df["Verified on"], errors="coerce"
    )
    filtered_df["HOG Approval on"] = pd.to_datetime(
        filtered_df["HOG Approval on"], errors="coerce"
    )
    filtered_df["Clearing date"] = pd.to_datetime(
        filtered_df["Clearing date"], errors="coerce"
    )
    filtered_df["year"] = filtered_df["Pstng Date"].dt.year
    filtered_df["Doc. Date"] = filtered_df["Doc. Date"].dt.date
    filtered_df["Pstng Date"] = filtered_df["Pstng Date"].dt.date
    filtered_df["On"] = filtered_df["On"].dt.date
    filtered_df["Updated on"] = filtered_df["Updated on"].dt.date
    filtered_df["Verified on"] = filtered_df["Verified on"].dt.date
    filtered_df["HOG Approval on"] = filtered_df["HOG Approval on"].dt.date
    filtered_df["Clearing date"] = filtered_df["Clearing date"].dt.date
    filtered_df["Time"] = filtered_df["Time"].dt.time
    filtered_df["Updated at"] = filtered_df["Updated at"].dt.time
    filtered_df["Verified at"] = filtered_df["Verified at"].dt.time
    filtered_df["HOG Approval at"] = filtered_df["HOG Approval at"].dt.time
    filtered_df.drop(columns=["Year"], inplace=True)
    df = filtered_df.copy()
    df.reset_index(drop=True, inplace=True)
    df["Vendor"] = df["Vendor"].astype(str)
    df["G/L"] = df["G/L"].astype(str)
    df["G/L"] = df["G/L"].apply(lambda x: str(x) if isinstance(x, str) else "")
    df["G/L"] = df["G/L"].apply(lambda x: re.sub(r"\..*", "", x))
    df.reset_index(drop=True, inplace=True)
    return df


def format_amount(amount):
    """
    Format the given amount into a human-readable currency string.

    Args:
    - amount (float or int): The amount to be formatted.

    Returns:
    - str: A formatted string representing the amount in
    Indian Rupees (₹).
           The formatting depends on the length of the integer
           part of the amount:
           - If the integer length is greater than 5 and less
           than or equal to 7, the amount is divided by
           100,000 and formatted as "₹ {amount / 100000:,.2f} lks".
           - If the integer length is greater than 7, the amount
            is divided by 10,000,000 and formatted as
            "₹ {amount / 10000000:,.2f} crs".
           - Otherwise, the amount is formatted directly as
           "₹ {amount:,.2f}".

    """
    integer_part = int(amount)
    integer_length = len(str(integer_part))

    if 5 < integer_length <= 7:
        return f"₹ {amount / 100000:,.2f} lks"
    elif integer_length > 7:
        return f"₹ {amount / 10000000:,.2f} crs"
    else:
        return f"₹ {amount:,.2f}"


@st.cache_resource(show_spinner=False)
def has_special_characters(s):
    """
    Check if a string contains any special characters.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string contains any special characters, False otherwise.

    """
    return re.search(r"[^A-Za-z0-9]+", s) is not None


@st.cache_resource(show_spinner=False)
def is_similar(s1, s2):
    """
    Check if two strings are similar by removing special
    characters and comparing the cleaned strings.

    Args:
        s1 (str): The first string to compare.
        s2 (str): The second string to compare.

    Returns:
        bool: True if the cleaned strings are equal,
        False otherwise.

    """
    # Remove special characters from both strings
    s1_clean = re.sub(r"[^A-Za-z0-9]+", "", str(s1))
    s2_clean = re.sub(r"[^A-Za-z0-9]+", "", str(s2))
    # Check if the cleaned strings are equal
    return s1_clean == s2_clean



@st.cache_resource(show_spinner=False)
def line_plot_overall_transactions(data, category, years, width=400, height=300):
    """
    Create a line plot showing the count of transactions over
     the specified years for a given category.

    Args:
        data (pd.DataFrame): The input data containing transaction records.
        category (str): The category of transactions to filter by.
        years (list of int): The years to include in the plot.
        width (int, optional): The width of the plot. Defaults to 400.
        height (int, optional): The height of the plot. Defaults to 300.

    Returns:
        plotly.graph_objs._figure.Figure: The Plotly figure object
        containing the line plot.

    """
    filtered_data = data[(data["category"] == category) & (data["year"].isin(years))]
    data_length = filtered_data.groupby("year").size().reset_index(name="data_len")

    # Create the line plot
    fig = px.line(
        data_length,
        x="year",
        y="data_len",
        title="Transactions Count",
        labels={"year": "Year", "data_len": "Transactions"},
        markers=True,
    )

    # Set mode to 'lines+markers'
    fig.update_traces(mode="lines+markers")

    # Update layout with width and height
    fig.update_layout(width=width, height=height)

    # Modify x-axis labels to include hyphens between years
    fig.update_xaxes(
        tickvals=years,
        ticktext=[re.sub(r"(\d{4})(\d{2})", r"\1-\2", str(year)) for year in years],
    )

    # Format y-axis ticks as integers
    fig.update_yaxes(tickformat=".0f")

    # Add text annotations to data points
    for year, count in zip(data_length["year"], data_length["data_len"]):
        fig.add_annotation(
            x=year,
            y=count,
            text=str(count),
            showarrow=False,
            font={"size": 12, "color": "black"},  # Use dictionary literal directly
            align="center",
            yshift=13,
        )
    return fig


@st.cache_resource(show_spinner=False)
def line_plot_used_amount(data, category, years, width=400, height=300):
    """
    Create a line plot showing the total amount of transactions over
     the specified years for a given category.

    Args:
        data (pd.DataFrame): The input data containing transaction records.
        category (str): The category of transactions to filter by.
        years (list of int): The years to include in the plot.
        width (int, optional): The width of the plot. Defaults to 400.
        height (int, optional): The height of the plot. Defaults to 300.

    Returns:
        plotly.graph_objs._figure.Figure: The Plotly figure object containing the line plot.

    """
    # Filter the data
    data = data[(data["category"] == category) & (data["year"].isin(years))]

    # Group by year and sum the amounts
    amount_length = (
        data.groupby("year")["Amount"].sum().reset_index(name="amount_length")
    )

    # Create the line plot
    fig = px.line(
        amount_length,
        x="year",
        y="amount_length",
        title="Transactions Value",
        labels={"year": "Year", "amount_length": "Amount"},
        markers=True,
    )

    # Set mode to 'lines+markers'
    fig.update_traces(mode="lines+markers")

    # Update layout with width and height
    fig.update_layout(width=width, height=height)

    # Modify x-axis labels to include hyphens between years
    fig.update_xaxes(
        tickvals=years,
        ticktext=[re.sub(r"(\d{4})(\d{2})", r"\1-\2", str(year)) for year in years],
    )

    # Define the format_amount function
    def format_amount(amount_value):
        """
        Format the given amount based on its value.

        Parameters:
        - amount_value (float or int): The amount to format.

        Returns:
        - str: Formatted string representation of the amount.
        """
        integer_part = int(amount_value)
        integer_length = len(str(integer_part))

        if 5 < integer_length <= 7:
            return f"₹ {amount_value / 100000:,.2f} lks"

        if integer_length > 7:
            return f"₹ {amount_value / 10000000:,.2f} crs"

        return f"₹ {amount_value:,.2f}"

    # Add formatted annotations on top of data points
    for year, amount in zip(amount_length["year"], amount_length["amount_length"]):
        formatted_amount = format_amount(amount)
        fig.add_annotation(
            x=year,
            y=amount,
            text=formatted_amount,
            showarrow=False,
            font={"size": 12, "color": "black"},
            align="center",
            yshift=13,
        )

    return fig



@st.cache_resource(show_spinner=False)
def check_similarity(s1, s2, threshold=0.8):
    """
    Check if two strings are similar based on a similarity threshold.

    Parameters:
    - s1 (str): First string to compare.
    - s2 (str): Second string to compare.
    - threshold (float, optional): Minimum similarity ratio to consider strings similar.
    Defaults to 0.8.

    Returns:
    - bool: True if the similarity ratio between s1 and s2 is greater than or equal
    to the threshold, False otherwise.
    """
    s1 = str(s1)
    s2 = str(s2)
    similarity = difflib.SequenceMatcher(None, s1, s2).ratio()
    return similarity >= threshold


def filter_auth(filtered_df, checked_columns_auth, filename):
    """
    Filter DataFrame based on checked authorization columns and sort results.

    Parameters:
    - filtered_df (pd.DataFrame): DataFrame to filter.
    - checked_columns_auth (list): List of column names to check for authorization.
    - filename (str): Name of the output file.

    Returns:
    - tuple or None: Tuple containing filtered DataFrame, checked columns list,
    and filename if successful,
      or None, None, None if an error occurs.
    """
    if len(checked_columns_auth) == 1:
        st.error("Please select another checkbox to verify Authorization Parameters.")
        return None, None, None

    for i in range(len(checked_columns_auth) - 1):
        col_i = checked_columns_auth[i]
        col_j = checked_columns_auth[i + 1]
        filtered_df = filtered_df[filtered_df[col_i] == filtered_df[col_j]]

    sort_columns = checked_columns_auth.copy()
    if "Reimbursement ID" not in checked_columns_auth and "Cost Center" not in checked_columns_auth:
        sort_columns += ["Reimbursement ID", "Cost Center"]
    elif "Reimbursement ID" in checked_columns_auth and "Cost Center" not in checked_columns_auth:
        sort_columns += ["Cost Center"]
    elif "Cost Center" in checked_columns_auth and "Reimbursement ID" not in checked_columns_auth:
        sort_columns += ["Reimbursement ID"]

    filtered_df = filtered_df.sort_values(by=sort_columns)
    filtered_df.reset_index(drop=True, inplace=True)
    filtered_df.index += 1

    filename = "Transactions_with_same_column.xlsx"

    try:
        return filtered_df, checked_columns_auth, filename
    except FileNotFoundError as e:
        # Handle specific exception (e.g., file not found)
        st.error(f"File not found: {e}")
        return None, None, None


def filter_gen(filtered_df, checked_columns_gen, filename):
    """
    Filter and sort DataFrame based on checked columns.

    Parameters:
    - filtered_df (pd.DataFrame): DataFrame to filter.
    - checked_columns_gen (list): List of columns to check for duplicates.
    - filename (str): Filename to save results.

    Returns:
    - pd.DataFrame or None: Filtered DataFrame, checked_columns_gen, filename.
    """
    filtered_df = filtered_df[
        filtered_df.duplicated(subset=checked_columns_gen, keep=False)
    ]

    sort_columns = checked_columns_gen.copy()
    if "Reimbursement ID" not in checked_columns_gen and "Cost Center" not in checked_columns_gen:
        sort_columns += ["Reimbursement ID", "Cost Center"]
    elif "Reimbursement ID" in checked_columns_gen and "Cost Center" not in checked_columns_gen:
        sort_columns += ["Cost Center"]
    elif "Cost Center" in checked_columns_gen and "Reimbursement ID" not in checked_columns_gen:
        sort_columns += ["Reimbursement ID"]

    filtered_df = filtered_df.sort_values(by=sort_columns)
    filtered_df.reset_index(drop=True, inplace=True)
    filtered_df.index += 1

    filename = "Transactions_with_same_column.xlsx"

    try:
        return filtered_df, checked_columns_gen, filename

    except pd.errors.EmptyDataError as e:
        st.error(f"An error occurred: {e}")
        return None, None, None


def filter_spec(filtered_df, checked_columnsspec, dfholiday, filename):
    """
    Filter the dataframe based on specified columns and holiday dates,
     and perform various transformations
    including finding similar invoices and handling special characters
     in invoice numbers.

    Args:
        filtered_df (pd.DataFrame): The dataframe to be filtered and processed.
        checked_columnsspec (list of str): The columns based on which
        filtering and processing will be applied.
        dfholiday (pd.DataFrame): The dataframe containing holiday dates.
        filename (str): The filename for saving the processed dataframe.

    Returns:
        pd.DataFrame: The filtered and processed dataframe.
        list of str: The updated list of checked columns.
        pd.DataFrame: The dataframe containing holiday dates.
        str: The filename for saving the processed dataframe.

    Raises:
        Exception: If an error occurs during processing, an error message
         is displayed and None is returned
                   for all return values.

    """
    filtered_df["Invoice Number"] = filtered_df["Invoice Number"].astype(str)
    if "Holiday Transactions" in checked_columnsspec:
        if len(checked_columnsspec) == 1:
            filtered_df["Document Date"] = pd.to_datetime(
                filtered_df["Document Date"], format="%Y/%m/%d", errors="coerce"
            )
            filtered_df["Posting Date"] = pd.to_datetime(
                filtered_df["Posting Date"], format="%Y/%m/%d", errors="coerce"
            )
            filtered_df["Verified on"] = pd.to_datetime(
                filtered_df["Verified on"], format="%Y/%m/%d", errors="coerce"
            )
            dfholiday["date"] = pd.to_datetime(
                dfholiday["date"], format="%Y/%m/%d", errors="coerce"
            )
            filtered_df = filtered_df[
                filtered_df["Posting Date"].isin(dfholiday["date"])
            ]
            checked_columnsspec = [
                (
                    "Posting Date"
                    if col == "Holiday Transactions"
                    else (
                        "Invoice Number"
                        if col in ("Inv-Special Character", "80 % Same Invoice")
                        else col
                    )
                )
                for col in checked_columnsspec
            ]
        elif (
            len(checked_columnsspec) == 2
            and "Inv-Special Character" in checked_columnsspec
        ):
            filtered_df["Document Date"] = pd.to_datetime(
                filtered_df["Document Date"], format="%Y/%m/%d", errors="coerce"
            )
            filtered_df["Posting Date"] = pd.to_datetime(
                filtered_df["Posting Date"], format="%Y/%m/%d", errors="coerce"
            )
            filtered_df["Verified on"] = pd.to_datetime(
                filtered_df["Verified on"], format="%Y/%m/%d", errors="coerce"
            )
            dfholiday["date"] = pd.to_datetime(
                dfholiday["date"], format="%Y/%m/%d", errors="coerce"
            )
            filtered_df = filtered_df[
                filtered_df["Posting Date"].isin(dfholiday["date"])
            ]
            filtered_df = filtered_df.sort_values(
                by=["Invoice Number", "Posting Date"])
            filtered_df = filtered_df[
                ~filtered_df.duplicated(subset="Invoice Number", keep="last")
            ]

            # Find similar invoices without grouping
            similar_invoices = set()
            invoice_pairs = [
                (invoice, re.sub(r"[^A-Za-z0-9]+", "", str(invoice)))
                for invoice in filtered_df["Invoice Number"]
            ]
            for i, (inv1, clean_inv1) in enumerate(invoice_pairs):
                for inv2, clean_inv2 in invoice_pairs[i + 1:]:
                    if is_similar(clean_inv1, clean_inv2):
                        similar_invoices.add(inv1)
                        similar_invoices.add(inv2)

            # Filter dataframe to keep only similar invoices
            filtered_df = filtered_df[
                filtered_df["Invoice Number"].isin(similar_invoices)
            ]
            checked_columnsspec = [
                (
                    "Posting Date"
                    if col == "Holiday Transactions"
                    else (
                        "Invoice Number"
                        if col in ("Inv-Special Character", "80 % Same Invoice")
                        else col
                    )
                )
                for col in checked_columnsspec
            ]
        elif (
            len(checked_columnsspec) == 2 and "80 % Same Invoice" in checked_columnsspec
        ):
            filtered_df["Document Date"] = pd.to_datetime(
                filtered_df["Document Date"], format="%Y/%m/%d", errors="coerce"
            )
            filtered_df["Posting Date"] = pd.to_datetime(
                filtered_df["Posting Date"], format="%Y/%m/%d", errors="coerce"
            )
            filtered_df["Verified on"] = pd.to_datetime(
                filtered_df["Verified on"], format="%Y/%m/%d", errors="coerce"
            )
            dfholiday["date"] = pd.to_datetime(
                dfholiday["date"], format="%Y/%m/%d", errors="coerce"
            )
            filtered_df = filtered_df[
                filtered_df["Posting Date"].isin(dfholiday["date"])
            ]
            filtered_df["Invoice Number"] = filtered_df["Invoice Number"].astype(
                str)
            filtered_df["check_similarity"] = False
            for i in range(len(filtered_df)):
                for j in range(i + 1, len(filtered_df)):
                    invoice1 = filtered_df.iloc[i]["Invoice Number"]
                    invoice2 = filtered_df.iloc[j]["Invoice Number"]
                    if is_similar(invoice1, invoice2):
                        filtered_df.at[i, "check_similarity"] = True
                        filtered_df.at[j, "check_similarity"] = True
            filtered_df = filtered_df[filtered_df["check_similarity"]]
            checked_columnsspec = [
                (
                    "Posting Date"
                    if col == "Holiday Transactions"
                    else (
                        "Invoice Number"
                        if col in ("Inv-Special Character", "80 % Same Invoice")
                        else col
                    )
                )
                for col in checked_columnsspec
            ]
        else:
            filtered_df["Document Date"] = pd.to_datetime(
                filtered_df["Document Date"], format="%Y/%m/%d", errors="coerce"
            )
            filtered_df["Posting Date"] = pd.to_datetime(
                filtered_df["Posting Date"], format="%Y/%m/%d", errors="coerce"
            )
            filtered_df["Verified on"] = pd.to_datetime(
                filtered_df["Verified on"], format="%Y/%m/%d", errors="coerce"
            )
            dfholiday["date"] = pd.to_datetime(
                dfholiday["date"], format="%Y/%m/%d", errors="coerce"
            )
            filtered_df = filtered_df[
                filtered_df["Posting Date"].isin(dfholiday["date"])
            ]
            filtered_df = filtered_df.sort_values(
                by=["Invoice Number", "Posting Date"])
            filtered_df = filtered_df[
                ~filtered_df.duplicated(subset="Invoice Number", keep="last")
            ]

            # Find similar invoices without grouping
            similar_invoices = set()
            invoice_pairs = [
                (invoice, re.sub(r"[^A-Za-z0-9]+", "", str(invoice)))
                for invoice in filtered_df["Invoice Number"]
            ]
            for i, (inv1, clean_inv1) in enumerate(invoice_pairs):
                for inv2, clean_inv2 in invoice_pairs[i + 1:]:
                    if is_similar(clean_inv1, clean_inv2):
                        similar_invoices.add(inv1)
                        similar_invoices.add(inv2)

            # Filter dataframe to keep only similar invoices
            filtered_df = filtered_df[
                filtered_df["Invoice Number"].isin(similar_invoices)
            ]
            filtered_df["Invoice Number"] = filtered_df["Invoice Number"].astype(
                str)
            filtered_df["check_similarity"] = False
            for i in range(len(filtered_df)):
                for j in range(i + 1, len(filtered_df)):
                    invoice1 = filtered_df.iloc[i]["Invoice Number"]
                    invoice2 = filtered_df.iloc[j]["Invoice Number"]
                    if is_similar(invoice1, invoice2):
                        filtered_df.at[i, "check_similarity"] = True
                        filtered_df.at[j, "check_similarity"] = True
            filtered_df = filtered_df[filtered_df["check_similarity"]]
    elif "80 % Same Invoice" in checked_columnsspec:
        if len(checked_columnsspec) == 1:
            filtered_df["Invoice Number"] = filtered_df["Invoice Number"].astype(
                str)
            filtered_df["check_similarity"] = False
            for i in range(len(filtered_df)):
                for j in range(i + 1, len(filtered_df)):
                    invoice1 = filtered_df.iloc[i]["Invoice Number"]
                    invoice2 = filtered_df.iloc[j]["Invoice Number"]
                    if is_similar(invoice1, invoice2):
                        filtered_df.at[i, "check_similarity"] = True
                        filtered_df.at[j, "check_similarity"] = True
            filtered_df = filtered_df[filtered_df["check_similarity"]]
        else:
            filtered_df = filtered_df.sort_values(
                by=["Invoice Number", "Posting Date"])
            filtered_df = filtered_df[
                ~filtered_df.duplicated(subset="Invoice Number", keep="last")
            ]

            # Find similar invoices without grouping
            similar_invoices = set()
            invoice_pairs = [
                (invoice, re.sub(r"[^A-Za-z0-9]+", "", str(invoice)))
                for invoice in filtered_df["Invoice Number"]
            ]
            for i, (inv1, clean_inv1) in enumerate(invoice_pairs):
                for inv2, clean_inv2 in invoice_pairs[i + 1:]:
                    if is_similar(clean_inv1, clean_inv2):
                        similar_invoices.add(inv1)
                        similar_invoices.add(inv2)

            # Filter dataframe to keep only similar invoices
            filtered_df = filtered_df[
                filtered_df["Invoice Number"].isin(similar_invoices)
            ]
            filtered_df["Invoice Number"] = filtered_df["Invoice Number"].astype(
                str)
            filtered_df["check_similarity"] = False
            for i in range(len(filtered_df)):
                for j in range(i + 1, len(filtered_df)):
                    invoice1 = filtered_df.iloc[i]["Invoice Number"]
                    invoice2 = filtered_df.iloc[j]["Invoice Number"]
                    if is_similar(invoice1, invoice2):
                        filtered_df.at[i, "check_similarity"] = True
                        filtered_df.at[j, "check_similarity"] = True
            filtered_df = filtered_df[filtered_df["check_similarity"]]
    elif "Inv-Special Character" in checked_columnsspec:
        if len(checked_columnsspec) == 1:
            filtered_df = filtered_df.sort_values(
                by=["Invoice Number", "Posting Date"])
            filtered_df = filtered_df[
                ~filtered_df.duplicated(subset="Invoice Number", keep="last")
            ]

            # Find similar invoices without grouping
            similar_invoices = set()
            invoice_pairs = [
                (invoice, re.sub(r"[^A-Za-z0-9]+", "", str(invoice)))
                for invoice in filtered_df["Invoice Number"]
            ]
            for i, (inv1, clean_inv1) in enumerate(invoice_pairs):
                for inv2, clean_inv2 in invoice_pairs[i + 1:]:
                    if is_similar(clean_inv1, clean_inv2):
                        similar_invoices.add(inv1)
                        similar_invoices.add(inv2)

            # Filter dataframe to keep only similar invoices
            filtered_df = filtered_df[
                filtered_df["Invoice Number"].isin(similar_invoices)
            ]

    checked_columnsspec = [
        (
            "Posting Date"
            if col == "Holiday Transactions"
            else (
                "Invoice Number"
                if col in ("Inv-Special Character", "80 % Same Invoice")
                else col
            )
        )
        for col in checked_columnsspec
    ]
    sort_columns = checked_columnsspec.copy()
    if (
        "Reimbursement ID" not in checked_columnsspec
        and "Cost Center" not in checked_columnsspec
    ):
        sort_columns += ["Reimbursement ID", "Cost Center"]
    elif (
        "Reimbursement ID" in checked_columnsspec
        and "Cost Center" not in checked_columnsspec
    ):
        sort_columns += ["Cost Center"]
    elif (
        "Cost Center" in checked_columnsspec
        and "Reimbursement ID" not in checked_columnsspec
    ):
        sort_columns += ["Reimbursement ID"]
    filtered_df = filtered_df.sort_values(by=sort_columns)
    filtered_df.reset_index(drop=True, inplace=True)
    filtered_df.index += 1
    try:
        return filtered_df, checked_columnsspec, dfholiday, filename

    except pd.errors.EmptyDataError as e:
        st.error(f"An error occurred: {e}")
        return None, None, None, None
