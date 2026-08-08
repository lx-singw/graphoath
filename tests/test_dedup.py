import pytest
import time
from graphoath.ops.dedup import IncidentDeduplicator

def test_dedup_rapid_events_suppression():
    IncidentDeduplicator.clear_cache()
    dedup = IncidentDeduplicator(ttl_seconds=900)
    source_urn = "urn:li:dataset:(snowflake,prod.orders)"
    failure_type = "ROW_COUNT_ZERO"

    # 1. First event
    res1 = dedup.check_and_deduplicate(source_urn, failure_type)
    assert res1.is_duplicate is False
    assert res1.duplicate_event_count == 1

    # 2. Simulate 49 rapid duplicate events
    for _ in range(49):
        res_dup = dedup.check_and_deduplicate(source_urn, failure_type)
        assert res_dup.is_duplicate is True
        assert res_dup.incident_urn == res1.incident_urn

    assert res_dup.duplicate_event_count == 50

def test_dedup_post_ttl_window():
    IncidentDeduplicator.clear_cache()
    dedup = IncidentDeduplicator(ttl_seconds=1)  # 1s TTL for testing
    source_urn = "urn:li:dataset:(snowflake,prod.orders)"
    failure_type = "SCHEMA_BREAK"

    res1 = dedup.check_and_deduplicate(source_urn, failure_type)
    assert res1.is_duplicate is False

    time.sleep(1.1)  # Exceed TTL

    res2 = dedup.check_and_deduplicate(source_urn, failure_type)
    assert res2.is_duplicate is False
    assert res2.duplicate_event_count == 1
