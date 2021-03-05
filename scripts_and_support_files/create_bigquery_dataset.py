from google.cloud import bigquery

client = bigquery.Client()
dataset_id = "{}.industrial_machine_product_data".format(client.project)

dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"

dataset = client.create_dataset(dataset, timeout=30)
print("Created dataset {}.{}".format(client.project, dataset.dataset_id))