import pytest
from graphoath.modules.deposition.trigger import AssertionTriggerListener, AssertionRunEvent

def test_assertion_trigger_listener_raises_incident():
    listener = AssertionTriggerListener()
    event_payload = {
        "event_type": "AssertionRunEvent_v1",
        "assertion_urn": "urn:li:assertion:4f8e910a-2b3c-4d5e",
        "dataset_urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
        "status": "FAILURE",
        "failure_type": "ROW_COUNT_ZERO"
    }

    res = listener.process_assertion_event(event_payload)
    assert res["status"] == "INCIDENT_RAISED"
    assert res["dataset_urn"] == "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)"
    assert res["assertion_urn"] == "urn:li:assertion:4f8e910a-2b3c-4d5e"
    assert "incident_urn" in res

def test_assertion_trigger_listener_ignores_success_event():
    listener = AssertionTriggerListener()
    event_payload = {
        "event_type": "AssertionRunEvent_v1",
        "assertion_urn": "urn:li:assertion:valid_1",
        "dataset_urn": "urn:li:dataset:table_1",
        "status": "SUCCESS",
        "failure_type": "NONE"
    }

    res = listener.process_assertion_event(event_payload)
    assert res["status"] == "IGNORED"
