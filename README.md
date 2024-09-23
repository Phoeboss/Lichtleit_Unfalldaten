# Project README

## Setup Instructions

### 1. Create a Virtual Environment

To create a virtual environment named `venv`, run the following command:

```bash
python -m venv venv
```

### 2. Activate the Virtual Environment

- On Windows:

```bash
.\venv\Scripts\activate
```

### 3. Install Requirements

To install the required packages, run:

```bash
pip install -r requirements.txt
```

### 4. Run the Script

To run the `export_coord_data.py` script, use the following command:

```bash
python .\export_coord_data.py '.\ADAC Verkehrsdaten_formatiert_LichtLeit.csv'
```

## Adding Filters

The `filter_data` function is located in the `export_coord_data.py` file. To add filters, follow these steps:

1. Open `export_coord_data.py` in your preferred text editor.
2. Locate the `filter_data` function. It should look something like this:

```python
def filter_data(data, filters):
    # Existing filter logic
    pass
```

3. Add your custom filter logic within the `filter_data` function. For example:

```python
def filter_data(data, filters):
    # Existing filter logic

    # Custom filter example
    if 'custom_filter' in filters:
        data = [item for item in data if item['key'] == filters['custom_filter']]

    return data
```

4. Save the file and re-run the script to apply the new filters.






































































