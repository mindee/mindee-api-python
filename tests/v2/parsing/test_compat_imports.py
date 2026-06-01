from mindee.parsing.v2.base_inference import BaseInference
from mindee.parsing.v2.base_response import BaseResponse
from mindee.parsing.v2.inference_job import InferenceJob
from mindee.v2.parsing import BaseInference as V2BaseInference
from mindee.v2.parsing import BaseResponse as V2BaseResponse
from mindee.v2.parsing.inference import BaseInference as V2InferenceBaseInference
from mindee.v2.parsing.inference import BaseResponse as V2InferenceBaseResponse
from mindee.v2.parsing.inference.base_inference import (
    BaseInference as V2BaseInferenceModule,
)
from mindee.v2.parsing.inference.base_response import (
    BaseResponse as V2BaseResponseModule,
)
from mindee.v2.parsing.inference.inference_job import InferenceJob as V2InferenceJob


def test_v2_parsing_compatibility_imports():
    assert V2BaseInference is BaseInference
    assert V2BaseResponse is BaseResponse
    assert V2InferenceBaseInference is BaseInference
    assert V2InferenceBaseResponse is BaseResponse
    assert V2BaseInferenceModule is BaseInference
    assert V2BaseResponseModule is BaseResponse
    assert V2InferenceJob is InferenceJob
