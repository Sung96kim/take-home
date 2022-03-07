from indico import IndicoClient, IndicoConfig
from indico.queries import (
    RetrieveStorageObject,
    SubmissionResult,
    UpdateSubmission,
    WorkflowSubmission,
)
import ipdb

# Create an Indico API client
my_config = IndicoConfig(host="app.indico.io", api_token_path="./indico_api_token.txt")
client = IndicoClient(config=my_config)

workflow_id = 933

submission_ids = client.call(
    WorkflowSubmission(
        workflow_id=workflow_id, files=["./assets/AriatInvoice03.28.19.pdf"]
    )
)
submission_id = submission_ids[0]

result_url = client.call(SubmissionResult(submission_id, wait=True))
result = client.call(RetrieveStorageObject(result_url.result))

print(result["results"]["document"]["Invoice Fields q2026 model"]["final"])

# Get 'final'

client.call(UpdateSubmission(submission_id, retrieved=True))

ipdb.set_trace()
