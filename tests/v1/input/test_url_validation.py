import pytest

from mindee.error.mindee_error import MindeeSourceError
from mindee.mindee_http.response_validation import validate_url_for_source


@pytest.mark.v1
class TestValidateUrlScheme:
    def test_rejects_http(self):
        with pytest.raises(MindeeSourceError, match="HTTPS"):
            validate_url_for_source("http://example.com/file.pdf")

    def test_rejects_ftp(self):
        with pytest.raises(MindeeSourceError, match="HTTPS"):
            validate_url_for_source("ftp://example.com/file.pdf")

    def test_accepts_https(self):
        validate_url_for_source("https://example.com/file.pdf")


@pytest.mark.v1
class TestValidateUrlUserinfo:
    def test_rejects_username_and_password(self):
        with pytest.raises(MindeeSourceError, match="credentials"):
            validate_url_for_source("https://user:pass@example.com/file.pdf")

    def test_rejects_username_only(self):
        with pytest.raises(MindeeSourceError, match="credentials"):
            validate_url_for_source("https://user@example.com/file.pdf")


@pytest.mark.v1
class TestValidateUrlLoopbackHostnames:
    def test_rejects_localhost(self):
        with pytest.raises(MindeeSourceError, match="Loopback"):
            validate_url_for_source("https://localhost/file.pdf")

    def test_rejects_localhost_subdomain(self):
        with pytest.raises(MindeeSourceError, match="Loopback"):
            validate_url_for_source("https://myapp.localhost/file.pdf")

    def test_rejects_ip6_localhost(self):
        with pytest.raises(MindeeSourceError, match="Loopback"):
            validate_url_for_source("https://ip6-localhost/file.pdf")

    def test_rejects_ip6_loopback(self):
        with pytest.raises(MindeeSourceError, match="Loopback"):
            validate_url_for_source("https://ip6-loopback/file.pdf")


@pytest.mark.v1
class TestValidateUrlLoopbackIPs:
    def test_rejects_ipv4_loopback(self):
        with pytest.raises(MindeeSourceError, match="disallowed"):
            validate_url_for_source("https://127.0.0.1/file.pdf")

    def test_rejects_ipv4_loopback_other(self):
        with pytest.raises(MindeeSourceError, match="disallowed"):
            validate_url_for_source("https://127.0.0.2/file.pdf")

    def test_rejects_ipv6_loopback(self):
        with pytest.raises(MindeeSourceError, match="disallowed"):
            validate_url_for_source("https://[::1]/file.pdf")


@pytest.mark.v1
class TestValidateUrlPrivateIPs:
    def test_rejects_rfc1918_10_block(self):
        with pytest.raises(MindeeSourceError, match="disallowed"):
            validate_url_for_source("https://10.0.0.1/file.pdf")

    def test_rejects_rfc1918_172_block(self):
        with pytest.raises(MindeeSourceError, match="disallowed"):
            validate_url_for_source("https://172.16.0.1/file.pdf")

    def test_rejects_rfc1918_192_block(self):
        with pytest.raises(MindeeSourceError, match="disallowed"):
            validate_url_for_source("https://192.168.1.1/file.pdf")

    def test_rejects_link_local(self):
        with pytest.raises(MindeeSourceError, match="disallowed"):
            validate_url_for_source("https://169.254.0.1/file.pdf")

    def test_rejects_unspecified(self):
        with pytest.raises(MindeeSourceError, match="disallowed"):
            validate_url_for_source("https://0.0.0.0/file.pdf")

    def test_rejects_multicast(self):
        with pytest.raises(MindeeSourceError, match="disallowed"):
            validate_url_for_source("https://224.0.0.1/file.pdf")


@pytest.mark.v1
class TestValidateUrlCgnat:
    def test_rejects_cgnat_start(self):
        with pytest.raises(MindeeSourceError, match="disallowed"):
            validate_url_for_source("https://100.64.0.1/file.pdf")

    def test_rejects_cgnat_end(self):
        with pytest.raises(MindeeSourceError, match="disallowed"):
            validate_url_for_source("https://100.127.255.255/file.pdf")

    def test_accepts_just_outside_cgnat(self):
        # 100.128.0.1 is outside 100.64.0.0/10
        validate_url_for_source("https://100.128.0.1/file.pdf")


@pytest.mark.v1
class TestValidateUrlIpv6UniqueLocal:
    def test_rejects_ipv6_ula_fc(self):
        with pytest.raises(MindeeSourceError, match="disallowed"):
            validate_url_for_source("https://[fc00::1]/file.pdf")

    def test_rejects_ipv6_ula_fd(self):
        with pytest.raises(MindeeSourceError, match="disallowed"):
            validate_url_for_source("https://[fd00::1]/file.pdf")
