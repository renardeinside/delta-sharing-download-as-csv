from io import StringIO

import streamlit as st
from delta_sharing.delta_sharing import (
    DataSharingRestClient,
    DeltaSharingProfile,
    SharingClient,
    Table,
)

from delta_sharing_download_as_csv.utils import download_table_as_csv

st.set_page_config(page_title="Delta Sharing Download as CSV", page_icon=":arrow_down:")

st.markdown("## Download a Delta Sharing Table as CSV :sparkles:")

message_col, status_col = st.columns([0.7, 0.3])

with message_col.container():
    st.markdown("*This app allows you to download a Delta Sharing table as a CSV file.*")
status_col.empty()

uploader_placeholder = st.empty()


def uploader_callback():
    if st.session_state.get("profile_file_uploader") is not None:
        uploaded_file = st.session_state["profile_file_uploader"]
        try:
            raw_payload = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
            profile = DeltaSharingProfile.from_json(raw_payload)
            client = SharingClient(profile)
            with uploader_placeholder, st.spinner("Loading available shares and tables..."):
                all_tables = client.list_all_tables()
                st.session_state["all_tables"] = all_tables
                st.session_state["profile"] = profile
        except Exception as e:
            st.toast(
                body=f"""
                     Exception while loading the profile file: {e}. 
                     Please remove the file and upload a valid one.""",
                icon="🚨",
            )


if "profile" not in st.session_state:
    uploader_placeholder.file_uploader(
        accept_multiple_files=False,
        on_change=uploader_callback,
        type=["share"],
        help="Upload a Delta Sharing Profile",
        label="Please upload a Delta Sharing Profile file below:",
        key="profile_file_uploader",
    )
    status_col.empty()
else:
    with status_col.container():
        status_col.markdown("Profile loaded :white_check_mark:")
        cleanup = status_col.button("Click here to delete the profile file and start over.", key="delete_profile")
        if cleanup:
            del st.session_state["profile"]
            del st.session_state["all_tables"]
            for key in st.session_state.keys():
                if key.endswith("_fetched"):
                    del st.session_state[key]
            st.rerun()


def fetch_and_put_download_view(button_view, state_key: str, table: Table, profile: DeltaSharingProfile):
    with button_view, st.spinner("Fetching table..."):
        raw_csv = download_table_as_csv(DataSharingRestClient(profile), table=table)
        st.session_state[state_key] = raw_csv


if "all_tables" in st.session_state:
    profile = st.session_state["profile"]
    all_tables = st.session_state["all_tables"]
    if len(all_tables) == 0:
        st.write("No available tables found for this profile.")
    else:
        st.write(f"Available tables ({len(all_tables)} in total):")
        for table in all_tables:
            canonical_table_name = f"{table.share}.{table.schema}.{table.name}"
            container = st.container()
            c1, button_view = container.columns([0.7, 0.3])
            c1.markdown(canonical_table_name)
            state_key = f"{canonical_table_name}_fetched"
            if state_key in st.session_state:
                raw_csv = st.session_state[state_key]
                button_view.download_button(
                    label="Download data as CSV",
                    data=raw_csv,
                    file_name=f"{table.share}.{table.schema}.{table.name}.csv",
                    mime="text/csv",
                    type="primary",
                    use_container_width=True,
                )
            else:
                button_view.button(
                    "Fetch data",
                    type="secondary",
                    use_container_width=True,
                    key=f"fetch_{canonical_table_name}",
                    on_click=fetch_and_put_download_view,
                    args=(button_view, state_key, table, profile),
                )
