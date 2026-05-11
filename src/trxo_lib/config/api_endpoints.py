"""
Centralized API endpoint registry for all TRXO library domains.

Every hardcoded path used in exports/ and imports/ is defined once here.
Domain files call the appropriate static method and pass the result to
_construct_api_url(base_url, endpoint) or, where they already concatenate
directly, to f"{base_url}{endpoint}".

Structure:
  AMEndpoints  – Access Management (OpenAM / PingAM)
  IDMEndpoints – Identity Management (OpenIDM / PingIDM)
  ESVEndpoints – Environment Secrets & Variables (PingOne AIC only)
"""


class AMEndpoints:
    """Access Management (AM) endpoints."""

    class Auth:
        """Token acquisition and on-premise session authentication."""

        TOKEN = "/am/oauth2/access_token"

        @staticmethod
        def on_prem_authenticate(realm: str) -> str:
            """On-premise AM session authenticate endpoint."""
            return f"/am/json/realms/{realm}/authenticate"

    class Agents:
        """Policy Agent endpoints — Gateway, Java, and Web agent types."""

        @staticmethod
        def list_by_type(realm: str, agent_type: str) -> str:
            """List all agents of a specific type in a realm (export, GET)."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                f"/realm-config/agents/{agent_type}?_queryFilter=true"
            )

        @staticmethod
        def item(realm: str, agent_type: str, agent_id: str) -> str:
            """Single agent — GET (fetch), PUT (upsert), DELETE."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                f"/realm-config/agents/{agent_type}/{agent_id}"
            )

    class OAuth:
        """OAuth2 Client and provider configuration endpoints.

        The `client` endpoint is shared by the OAuth exporter, OAuth importer,
        and the Applications exporter — define once, reuse across all three.
        """

        @staticmethod
        def list_clients(realm: str) -> str:
            """List all OAuth2 clients in a realm (export, GET)."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                "/realm-config/agents/OAuth2Client?_queryFilter=true"
            )

        @staticmethod
        def client(realm: str, client_id: str) -> str:
            """Single OAuth2 client — GET (fetch), PUT (upsert), DELETE."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                f"/realm-config/agents/OAuth2Client/{client_id}"
            )

        @staticmethod
        def provider_config(realm: str) -> str:
            """Realm OAuth/OIDC provider configuration — PUT fallback upsert."""
            return f"/am/json/realms/root/realms/{realm}/realm-config/oauth-oidc"

        @staticmethod
        def list_services(realm: str) -> str:
            """List realm services — used to discover OAuth/OIDC service IDs (GET)."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                "/realm-config/services?_queryFilter=true"
            )

        @staticmethod
        def service(realm: str, service_id: str) -> str:
            """Single realm service — GET (fetch), PUT (import discovered provider)."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                f"/realm-config/services/{service_id}"
            )

    class Scripts:
        """Script endpoints — shared by OAuth, SAML, Journeys, and the Scripts domain."""

        @staticmethod
        def list_all(realm: str) -> str:
            """List all scripts in a realm (export, GET)."""
            return f"/am/json/realms/root/realms/{realm}/scripts?_queryFilter=true"

        @staticmethod
        def item(realm: str, script_id: str) -> str:
            """Single script — GET (fetch/export), PUT (upsert), DELETE."""
            return f"/am/json/realms/root/realms/{realm}/scripts/{script_id}"

        @staticmethod
        def create(realm: str) -> str:
            """Script collection create-action — POST when a PUT returns 404."""
            return f"/am/json/realms/root/realms/{realm}/scripts?_action=create"

    class Journeys:
        """Authentication Tree (Journey) endpoints."""

        @staticmethod
        def list_all(realm: str) -> str:
            """List all journey trees in a realm (export, GET)."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                "/realm-config/authentication/authenticationtrees/trees"
                "?_queryFilter=true"
            )

        @staticmethod
        def tree(realm: str, tree_id: str) -> str:
            """Single journey tree — GET (fetch) or PUT (import)."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                f"/realm-config/authentication/authenticationtrees/trees/{tree_id}"
            )

        @staticmethod
        def nodes_next_descendants(realm: str) -> str:
            """All nodes for a realm via nextdescendents action — POST."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                "/realm-config/authentication/authenticationtrees/nodes"
                "?_action=nextdescendents"
            )

        @staticmethod
        def node(realm: str, node_type: str, node_id: str) -> str:
            """Single journey node — PUT (import)."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                "/realm-config/authentication/authenticationtrees"
                f"/nodes/{node_type}/{node_id}"
            )

    class SAML:
        """SAML2 federation endpoints.

        The `export_metadata_jsp` path is shared by the SAML exporter,
        SAML importer, and Journeys exporter — defined once here.
        Callers are responsible for URL-encoding entity_id and realm as needed.
        """

        @staticmethod
        def list_providers(realm: str) -> str:
            """Shallow list of all SAML2 providers (hosted + remote) in a realm (GET)."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                "/realm-config/saml2?_queryFilter=true"
            )

        @staticmethod
        def provider(realm: str, location: str, provider_id: str) -> str:
            """Full provider detail — GET (export), PUT (upsert). location: 'hosted'/'remote'."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                f"/realm-config/saml2/{location}/{provider_id}"
            )

        @staticmethod
        def import_remote_metadata(realm: str) -> str:
            """Import remote entity metadata — POST ?_action=importEntity."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                "/realm-config/saml2/remote/?_action=importEntity"
            )

        @staticmethod
        def create_hosted_provider(realm: str) -> str:
            """Create a new hosted SAML entity — POST ?_action=create."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                "/realm-config/saml2/hosted?_action=create"
            )

        @staticmethod
        def export_metadata_jsp(entity_id: str, realm: str) -> str:
            """JSP endpoint returning XML SAML metadata for an entity (GET).
            Pass pre-encoded values when URL encoding is required by the caller."""
            return f"/am/saml2/jsp/exportmetadata.jsp?entityid={entity_id}&realm={realm}"

        @staticmethod
        def list_circles_of_trust(realm: str) -> str:
            """List all SAML2 Circles of Trust in a realm (GET)."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                "/realm-config/federation/circlesoftrust?_queryFilter=true"
            )

        @staticmethod
        def circle_of_trust(realm: str, cot_id: str) -> str:
            """Single Circle of Trust — PUT (import)."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                f"/realm-config/federation/circlesoftrust/{cot_id}"
            )

    class Services:
        """AM Services endpoints — global and realm scope."""

        LIST_GLOBAL = "/am/json/global-config/services?_queryFilter=true"

        @staticmethod
        def list_realm(realm: str) -> str:
            """List all services in a realm (GET)."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                "/realm-config/services?_queryFilter=true"
            )

        @staticmethod
        def global_item(service_id: str) -> str:
            """Single global service — GET (fetch detail), PUT (import)."""
            return f"/am/json/global-config/services/{service_id}"

        @staticmethod
        def realm_item(realm: str, service_id: str) -> str:
            """Single realm-scoped service — GET (fetch detail), PUT (import)."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                f"/realm-config/services/{service_id}"
            )

        @staticmethod
        def realm_item_next_descendants(realm: str, service_id: str) -> str:
            """Realm service next-descendants action — POST (fetch sub-configs)."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                f"/realm-config/services/{service_id}?_action=nextdescendents"
            )

    class Authn:
        """Authentication settings endpoints."""

        @staticmethod
        def realm_settings(realm: str) -> str:
            """Realm authentication settings — GET (export), PUT (import)."""
            return f"/am/json/realms/root/realms/{realm}/realm-config/authentication"

    class Policies:
        """AM Policy and Policy Set (application) endpoints."""

        @staticmethod
        def list_all(realm: str) -> str:
            """List all policies in a realm (export, GET)."""
            return f"/am/json/realms/root/realms/{realm}/policies?_queryFilter=true"

        @staticmethod
        def item(realm: str, policy_id: str) -> str:
            """Single policy — PUT (import)."""
            return f"/am/json/realms/root/realms/{realm}/policies/{policy_id}"

        @staticmethod
        def list_policy_sets(realm: str) -> str:
            """List all policy sets (applications) in a realm — export and import."""
            return f"/am/json/realms/root/realms/{realm}/applications?_queryFilter=true"

        @staticmethod
        def policy_set(realm: str, policy_set_id: str) -> str:
            """Single policy set (application) — PUT (import)."""
            return f"/am/json/realms/root/realms/{realm}/applications/{policy_set_id}"

    class Realms:
        """Global realm configuration endpoints."""

        LIST_ALL = "/am/json/global-config/realms?_queryFilter=true"

    class Webhooks:
        """AM Webhook endpoints."""

        @staticmethod
        def list_all(realm: str) -> str:
            """List all webhooks in a realm (export, GET)."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                "/realm-config/webhooks?_queryFilter=true"
            )

        @staticmethod
        def item(realm: str, webhook_id: str) -> str:
            """Single webhook — GET, PUT (upsert), DELETE."""
            return (
                f"/am/json/realms/root/realms/{realm}"
                f"/realm-config/webhooks/{webhook_id}"
            )


class IDMEndpoints:
    """Identity Management (IDM) / OpenIDM endpoints."""

    class Config:
        """Generic /openidm/config document endpoints."""

        LIST = "/openidm/config"
        MANAGED = "/openidm/config/managed"
        THEME_REALM = "/openidm/config/ui/themerealm"
        SYNC = "/openidm/config/sync"

        # Pre-built filtered list endpoints (query strings are exact and must not be changed)
        LIST_CONNECTORS = '/openidm/config?_queryFilter=_id+sw+"provisioner.openicf/"'
        LIST_EMAIL_TEMPLATES = '/openidm/config?_queryFilter=_id sw "emailTemplate"'
        LIST_ENDPOINT_CONFIGS = '/openidm/config?_queryFilter=_id sw "endpoint"'
        LIST_PRIVILEGES = '/openidm/config?_queryFilter=_id co "privilege"'
        LIST_IDENTITY_PROVIDERS = (
            "/openidm/config?_queryFilter=_id+sw+%22identityProvider%22&_fields=_id"
        )

        @staticmethod
        def item(config_id: str) -> str:
            """Single config document — GET (fetch), PUT (upsert)."""
            return f"/openidm/config/{config_id}"

        @staticmethod
        def email_template(name: str) -> str:
            """Single email template config — GET (fetch), PUT (import)."""
            return f"/openidm/config/emailTemplate/{name}"

        @staticmethod
        def theme_realm_for_realm(realm: str) -> str:
            """Themerealm config scoped to a specific realm's themes (GET)."""
            return f"/openidm/config/ui/themerealm?_fields=realm/{realm}"

    class Managed:
        """Managed object endpoints under /openidm/managed/."""

        @staticmethod
        def list_applications(realm: str) -> str:
            """List all managed applications for a realm (export, GET)."""
            return f"/openidm/managed/{realm}_application?_queryFilter=true"

        @staticmethod
        def application(realm: str, app_id: str) -> str:
            """Single managed application — PUT (upsert), DELETE."""
            return f"/openidm/managed/{realm}_application/{app_id}"

    class Schema:
        """Managed object schema endpoints under /openidm/schema/."""

        @staticmethod
        def managed_object(object_name: str) -> str:
            """Schema root for a managed object — GET (fetch current schema)."""
            return f"/openidm/schema/managed/{object_name}"

        @staticmethod
        def managed_object_property(object_name: str, prop_name: str) -> str:
            """Single property schema — PUT (add/update property), DELETE (remove property)."""
            return f"/openidm/schema/managed/{object_name}/properties/{prop_name}"


class ESVEndpoints:
    """Environment Secrets & Variables (ESV) endpoints (PingOne AIC)."""

    class Variables:
        """ESV variable endpoints."""

        LIST = "/environment/variables"

        @staticmethod
        def item(variable_id: str) -> str:
            """Single variable — PUT (create/update)."""
            return f"/environment/variables/{variable_id}"

    class Secrets:
        """ESV secret endpoints."""

        LIST = "/environment/secrets"

        @staticmethod
        def item(secret_id: str) -> str:
            """Single secret — GET (existence check), PUT (create/update metadata)."""
            return f"/environment/secrets/{secret_id}"

        @staticmethod
        def create_version(secret_id: str) -> str:
            """Create a new secret version — POST ?_action=create."""
            return f"/environment/secrets/{secret_id}/versions?_action=create"

        @staticmethod
        def set_description(secret_id: str) -> str:
            """Update secret description — POST ?_action=setDescription."""
            return f"/environment/secrets/{secret_id}?_action=setDescription"
