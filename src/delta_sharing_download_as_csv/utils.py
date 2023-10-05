from delta_sharing.delta_sharing import DataSharingRestClient, DeltaSharingReader, Table


def download_table_as_csv(rest_client: DataSharingRestClient, table: Table) -> bytes:
    reader = DeltaSharingReader(
        table=table,
        rest_client=rest_client,
    )
    df = reader.to_pandas()
    csv = df.to_csv().encode("utf-8")
    return csv
