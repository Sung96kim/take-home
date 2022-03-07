from indico import IndicoClient, IndicoConfig
from indico.queries import (
    RetrieveStorageObject,
    SubmissionResult,
    UpdateSubmission,
    WorkflowSubmission,
)

# Create an Indico API client
my_config = IndicoConfig(
    host="app.indico.io", api_token_path="./indico_api_token.txt"
)
client = IndicoClient(config=my_config)

workflow_id = 933

submission_ids = client.call(
    WorkflowSubmission(workflow_id=workflow_id, files=["./assets/ERSInvoice01.02.18_2.pdf"])
)
submission_id = submission_ids[0]

result_url = client.call(SubmissionResult(submission_id, wait=True))
result = client.call(RetrieveStorageObject(result_url.result))
#Returns a truckload of data, need to implement specific extraction from returned data pool, get "final"
print(result['results'])

client.call(UpdateSubmission(submission_id, retrieved=True))