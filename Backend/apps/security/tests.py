import hashlib

from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError
from django.test import SimpleTestCase, TestCase

from apps.common.status import RecordStatus
from apps.security.models import (
    HttpMethod,
    RefreshToken,
    Resource,
    ResourceRole,
    Role,
    RoleUser,
    User,
)
from apps.security.tokens import generate_refresh_value, hash_token
from config.database import database_from_environ


# ----------------- ISS-03: selección del motor -----------------
class DatabaseSelectionTests(SimpleTestCase):
    def _env(self, engine):
        return {
            "DB_ENGINE": engine,
            "POSTGRES_DB": "hornoraiz",
            "POSTGRES_USER": "hornoraiz",
            "POSTGRES_PASSWORD": "hornoraiz",
            "POSTGRES_HOST": "127.0.0.1",
            "POSTGRES_PORT": "5432",
            "MYSQL_DB": "hornoraiz_django",
            "MYSQL_USER": "admin",
            "MYSQL_PASSWORD": "1704",
            "MYSQL_HOST": "127.0.0.1",
            "MYSQL_PORT": "3306",
            "MSSQL_DB": "hornoraiz",
            "MSSQL_USER": "sa",
            "MSSQL_PASSWORD": "hornoraiz",
            "MSSQL_HOST": "127.0.0.1",
            "MSSQL_PORT": "1433",
            "ORACLE_DB": "hornoraiz",
            "ORACLE_USER": "admin",
            "ORACLE_PASSWORD": "hornoraiz",
            "ORACLE_HOST": "127.0.0.1",
            "ORACLE_PORT": "1521",
            "ORACLE_SERVICE_NAME": "FREEPDB1",
        }

    def test_postgresql_engine(self):
        config = database_from_environ(self._env("postgresql"))
        self.assertEqual(config["default"]["ENGINE"], "django.db.backends.postgresql")

    def test_mysql_engine(self):
        config = database_from_environ(self._env("mysql"))
        self.assertEqual(config["default"]["ENGINE"], "django.db.backends.mysql")
        self.assertEqual(config["default"]["OPTIONS"]["charset"], "utf8mb4")

    def test_mssql_engine(self):
        config = database_from_environ(self._env("mssql"))
        self.assertEqual(config["default"]["ENGINE"], "mssql")

    def test_oracle_uses_service_name(self):
        config = database_from_environ(self._env("oracle"))
        self.assertIn("SERVICE_NAME=FREEPDB1", config["default"]["NAME"])
        self.assertEqual(config["default"]["PORT"], "")

    def test_invalid_engine(self):
        with self.assertRaises(ImproperlyConfigured):
            database_from_environ({"DB_ENGINE": "sqlite"})

    def test_missing_variable(self):
        env = self._env("postgresql")
        env["POSTGRES_DB"] = ""
        with self.assertRaises(ImproperlyConfigured):
            database_from_environ(env)


# ----------------- ISS-15: RefreshToken -----------------
class RefreshTokenTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="rt-user",
            email="rt@example.com",
            password="HornoRaiz2026!",
        )

    def test_hash_matches_sha256(self):
        raw = generate_refresh_value()
        expected = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        self.assertEqual(hash_token(raw), expected)
        self.assertEqual(len(hash_token(raw)), 64)

    def test_refresh_row_does_not_store_raw_token(self):
        raw = generate_refresh_value()
        token_hash = hash_token(raw)
        row = RefreshToken.objects.create(
            user=self.user,
            token_hash=token_hash,
            expires_at=RefreshToken.default_expiry(),
        )
        self.assertNotEqual(row.token_hash, raw)
        self.assertEqual(row.token_hash, token_hash)
        self.assertEqual(row.status, RecordStatus.ACTIVE)

    def test_refresh_returns_active_by_default(self):
        raw = generate_refresh_value()
        row = RefreshToken.objects.create(
            user=self.user,
            token_hash=hash_token(raw),
            expires_at=RefreshToken.default_expiry(),
        )
        self.assertTrue(row.is_usable)
        self.assertEqual(row.user, self.user)


# ----------------- ISS-16: matriz RBAC -----------------
class RbacModelsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="rbac-user",
            email="rbac@example.com",
            password="HornoRaiz2026!",
            status=RecordStatus.ACTIVE,
        )

    def test_role_default_status_inactive(self):
        role = Role.objects.create(name="admin")
        self.assertEqual(role.status, RecordStatus.INACTIVE)

    def test_role_user_pair_is_unique(self):
        role = Role.objects.create(name="vendedor")
        RoleUser.objects.create(role=role, user=self.user)
        with self.assertRaises(IntegrityError):
            RoleUser.objects.create(role=role, user=self.user)

    def test_resource_method_route_is_unique(self):
        Resource.objects.create(
            name="Listar ventas",
            method=HttpMethod.GET,
            route="api/sale/sales/",
        )
        with self.assertRaises(IntegrityError):
            Resource.objects.create(
                name="Otra cosa",
                method=HttpMethod.GET,
                route="api/sale/sales/",
            )

    def test_resource_role_pair_is_unique(self):
        role = Role.objects.create(name="cajero")
        resource = Resource.objects.create(
            name="Listar productos",
            method=HttpMethod.GET,
            route="api/catalog/products/",
        )
        ResourceRole.objects.create(resource=resource, role=role)
        with self.assertRaises(IntegrityError):
            ResourceRole.objects.create(resource=resource, role=role)

    def test_full_chain_active(self):
        role = Role.objects.create(name="admin2", status=RecordStatus.ACTIVE)
        resource = Resource.objects.create(
            name="Listar pagos",
            method=HttpMethod.GET,
            route="api/sale/payments/",
            status=RecordStatus.ACTIVE,
        )
        ResourceRole.objects.create(
            resource=resource, role=role, status=RecordStatus.ACTIVE,
        )
        RoleUser.objects.create(
            role=role, user=self.user, status=RecordStatus.ACTIVE,
        )
        self.assertEqual(
            RoleUser.objects.filter(
                user=self.user, status=RecordStatus.ACTIVE
            ).count(),
            1,
        )
