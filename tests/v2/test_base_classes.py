from mindee.parsing.v2.base_inference import BaseInference
from mindee.parsing.v2.base_response import BaseResponse
from mindee.parsing.v2.inference_file import InferenceFile
from mindee.parsing.v2.inference_job import InferenceJob
from mindee.parsing.v2.inference_model import InferenceModel


def test_inference_job():
    job = InferenceJob({"id": "job-id"})

    assert job.id == "job-id"
    assert str(job) == "Job\n===\n:ID: job-id"


def test_base_inference():
    inference = BaseInference(
        {
            "id": "inference-id",
            "job": {"id": "job-id"},
            "model": {"id": "model-id"},
            "file": {
                "name": "document.pdf",
                "alias": "alias",
                "page_count": 2,
                "mime_type": "application/pdf",
            },
        }
    )

    assert inference.id == "inference-id"
    assert isinstance(inference.job, InferenceJob)
    assert inference.job.id == "job-id"
    assert isinstance(inference.model, InferenceModel)
    assert inference.model.id == "model-id"
    assert isinstance(inference.file, InferenceFile)
    assert inference.file.name == "document.pdf"


def test_base_response():
    class DummyResponse(BaseResponse):
        _slug = "dummy/results"

        def __init__(self):
            self.inference = "dummy inference"

    response = DummyResponse()

    assert str(response) == "dummy inference"
    assert response.get_result_slug() == "dummy/results"
