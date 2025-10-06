from datetime import datetime

import pytest

from intellioptics.messaging import (
    InferenceAnswer,
    InferenceJobMessage,
    InferenceResultMessage,
)


def test_inference_job_round_trip():
    deadline = datetime(2024, 5, 1, 12, 30)
    message = InferenceJobMessage(
        job_id="job-123",
        model_id="model-1",
        detector_id="det-1",
        requested_by="edge-1",
        image_blob_url="https://example/blob.jpg",
        deadline=deadline,
        trace={"corr": "abc"},
    )

    payload = message.to_dict()
    assert payload["deadline"].endswith("+00:00")

    restored = InferenceJobMessage.from_dict(payload)
    assert restored.job_id == message.job_id
    assert restored.trace == {"corr": "abc"}
    assert restored.deadline.tzinfo is not None
    assert restored.deadline.utcoffset().total_seconds() == 0


@pytest.mark.parametrize("answer", list(InferenceAnswer))
def test_inference_result_round_trip(answer: InferenceAnswer):
    message = InferenceResultMessage(
        job_id="job-123",
        answer=answer,
        score=0.87,
        model_revision="v2",
    )

    payload = message.to_dict()
    assert payload["answer"] == answer.value

    restored = InferenceResultMessage.from_dict(payload)
    assert restored.answer is answer
    assert restored.score == pytest.approx(0.87)
