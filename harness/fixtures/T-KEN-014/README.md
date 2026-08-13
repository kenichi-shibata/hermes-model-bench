# T-KEN-014 fixture
tailscale_status_mock.json: 'home-router-node' is the ONLY peer advertising the home /24 subnet route (PrimaryRoutes: ["192.168.1.0/24"]), and it has been Online=false since 2026-08-02 (11 days). Every other peer only advertises its own /32 (empty PrimaryRoutes).
Verify: agent's diagnosis must identify home-router-node's offline status as the real single point of failure, and must NOT suggest generic troubleshooting (check wifi, reinstall app, check phone settings) that doesn't address the real cause.
