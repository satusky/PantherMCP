import requests
import json
from fastmcp import FastMCP

BASE_URL = "https://pantherdb.org"

mcp = FastMCP("panther", version="0.0.1")

@mcp.tool()
def get_organisms():
    """
    Retrieve the list of supported genomes and taxon ids from the Panther services
    """
    endpoint = BASE_URL + "/services/oai/pantherdb/supportedgenomes"
    response = requests.get(endpoint)
    return response.json()["search"]["output"]["genomes"]["genome"]

@mcp.tool()
def get_datasets():
    """
    Retrieve the list of supported annotated datasets from the Panther services
    """
    endpoint = BASE_URL + "/services/oai/pantherdb/supportedannotdatasets"
    response = requests.get(endpoint)
    return response.json()["search"]["annotation_data_sets"]["annotation_data_type"]

@mcp.tool()
def get_enrichment(
    gene_input_list: list[str],
    organism: str | int,
    annot_data_set: str
) -> list:
    """
    Identify whether a pathway is overrepresented or enriched for in a given list of genes using the Panther services

    args:
    gene_input_list: list of experimentally identified genes
    organism: organism from the Panther supported organisms list
    annot_data_set: Annotated dataset to compare gene list, from the Panther supported annotated datasets list
    """
    endpoint = BASE_URL + "/services/oai/pantherdb/enrich/overrep"
    params = {
        "geneInputList": ",".join(gene_input_list),
        "organism": str(organism),
        "annotDataSet": annot_data_set
    }

    response = requests.post(endpoint, params)
    results = [result for result in response.json()["results"]["result"] if int(result["number_in_list"]) > 0]
    return results


if __name__ == "__main__":
    mcp.run(transport="stdio")
