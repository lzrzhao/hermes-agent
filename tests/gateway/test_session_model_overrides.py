import unittest


class TestSessionModelOverrides(unittest.TestCase):
    def test_provider_switch_clears_stale_runtime_fields(self):
        from gateway.run import GatewayRunner

        runner = GatewayRunner.__new__(GatewayRunner)
        runner._session_model_overrides = {
            "session-1": {
                "model": "openrouter/model-x",
                "provider": "openrouter",
                "api_key": None,
                "base_url": None,
                "api_mode": None,
            }
        }

        model, runtime = GatewayRunner._apply_session_model_override(
            runner,
            "session-1",
            "anthropic/claude-sonnet-4",
            {
                "provider": "anthropic",
                "api_key": "old-key",
                "base_url": "https://anthropic.example",
                "api_mode": "responses",
                "other": "keep-me",
            },
        )

        self.assertEqual(model, "openrouter/model-x")
        self.assertEqual(runtime["provider"], "openrouter")
        self.assertNotIn("api_key", runtime)
        self.assertNotIn("base_url", runtime)
        self.assertNotIn("api_mode", runtime)
        self.assertEqual(runtime["other"], "keep-me")

    def test_same_provider_keeps_existing_runtime_fields_when_override_blank(self):
        from gateway.run import GatewayRunner

        runner = GatewayRunner.__new__(GatewayRunner)
        runner._session_model_overrides = {
            "session-1": {
                "model": "anthropic/claude-opus-4-1",
                "provider": "anthropic",
                "api_key": None,
                "base_url": None,
                "api_mode": None,
            }
        }

        model, runtime = GatewayRunner._apply_session_model_override(
            runner,
            "session-1",
            "anthropic/claude-sonnet-4",
            {
                "provider": "anthropic",
                "api_key": "existing-key",
                "base_url": "https://anthropic.example",
                "api_mode": "responses",
            },
        )

        self.assertEqual(model, "anthropic/claude-opus-4-1")
        self.assertEqual(runtime["provider"], "anthropic")
        self.assertEqual(runtime["api_key"], "existing-key")
        self.assertEqual(runtime["base_url"], "https://anthropic.example")
        self.assertEqual(runtime["api_mode"], "responses")


if __name__ == "__main__":
    unittest.main()
