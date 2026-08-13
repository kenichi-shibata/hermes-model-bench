# T-KEN-007 fixture
service_logs.txt: THIS service's own logs are clean/healthy.
upstream_status_mock.json: the service's payment dependency has a REAL active outage (external, provider-side).
Correct diagnosis: FALSE POSITIVE from our side / external cause. The service itself is fine.
Verify: agent's answer must NOT recommend restarting/fixing the local service, and MUST correctly attribute the issue to the external payments-api outage.
