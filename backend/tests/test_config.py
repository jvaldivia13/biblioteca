from app.config import Settings


def test_allowed_origins_accepts_comma_separated_string():
    settings = Settings(
        jwt_secret_key="test-secret",
        allowed_origins_value="http://localhost:3000,http://localhost:8080",
    )

    assert settings.allowed_origins == [
        "http://localhost:3000",
        "http://localhost:8080",
    ]


def test_allowed_origins_accepts_json_list_string():
    settings = Settings(
        jwt_secret_key="test-secret",
        allowed_origins_value='["http://localhost:3000", "http://localhost:8080"]',
    )

    assert settings.allowed_origins == [
        "http://localhost:3000",
        "http://localhost:8080",
    ]


def test_debug_accepts_release_as_false():
    settings = Settings(jwt_secret_key="test-secret", debug="release")

    assert settings.debug is False


def test_settings_ignores_extra_seed_values():
    settings = Settings(
        jwt_secret_key="test-secret",
        admin_email="admin@biblioapp.pe",
        admin_password="Admin123!",
    )

    assert settings.jwt_secret_key == "test-secret"
