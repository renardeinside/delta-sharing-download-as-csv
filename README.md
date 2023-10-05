# Delta Sharing Download as CSV

Sample app to download a Delta Sharing table(s) as a CSV file.


## Prerequisites

- Python 3.10 or above
- [Hatch](https://hatch.pypa.io/latest/)
- Available Delta Sharing profile file (read [here](https://github.com/delta-io/delta-sharing/blob/main/PROTOCOL.md#profile-file-format) for details on file format)

## How to run

1. Clone this repository:

```bash
git clone https://github.com/renardeinside/delta-sharing-download-as-csv.git
```

2. Install the dependencies:

```bash
cd delta-sharing-download-as-csv
hatch env create
```

3. Activate the virtual environment:

```bash
hatch shell
```

4. Run the app:

```bash
streamlit run src/delta_sharing_download_as_csv/app.py
```

5. Open the app in your browser:

```bash
http://localhost:8501
```

6. Upload the Delta Sharing profile file and click the "Download" button for relevant table.


## Technologies used

- Python 3.10
- [Delta Sharing](https://github.com/delta-io/delta-sharing)
- [Streamlit](https://streamlit.io/)
- [Hatch](https://hatch.pypa.io/latest/)