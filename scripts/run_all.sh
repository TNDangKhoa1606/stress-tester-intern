#!/bin/bash

echo "Starting stress test run..."

TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
echo "Timestamp for this run: $TIMESTAMP"

REPORT_DIR="locust/reports"
mkdir -p "$REPORT_DIR"

echo "Running Step-Stress Test..."
STEP_STRESS_REPORT_NAME="${REPORT_DIR}/step_stress_${TIMESTAMP}"
# chọn shape = step
SHAPE=step locust -f locust/locustfile.py --config locust/locust.conf --headless \
  --html "${STEP_STRESS_REPORT_NAME}.html" \
  --csv "${STEP_STRESS_REPORT_NAME}"
echo "Step-Stress Test finished. Reports saved to ${STEP_STRESS_REPORT_NAME}.html/csv"

echo "Running Spike Test..."
SPIKE_TEST_REPORT_NAME="${REPORT_DIR}/spike_test_${TIMESTAMP}"
# chọn shape = spike
SHAPE=spike locust -f locust/locustfile.py --config locust/locust.conf --headless \
  --html "${SPIKE_TEST_REPORT_NAME}.html" \
  --csv "${SPIKE_TEST_REPORT_NAME}"
echo "Spike Test finished. Reports saved to ${SPIKE_TEST_REPORT_NAME}.html/csv"

echo "All tests completed."
