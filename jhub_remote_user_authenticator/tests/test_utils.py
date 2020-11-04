from jhub_remote_user_authenticator import utils


def test_quoted_printable_normalization_str():
    assert utils.normalize_quoted_printable('test@test.jp') == 'test@test.jp'
    assert utils.normalize_quoted_printable('test-@test') == 'test-@test'
    assert utils.normalize_quoted_printable('entity://test@test') == 'entity:=2F=2Ftest@test'
    assert utils.normalize_quoted_printable('entity://test漢字@test') == 'entity:=2F=2Ftest=E6=BC=A2=E5=AD=97@test'
    assert utils.normalize_quoted_printable('test.sample@test/') == 'test.sample@test=2F'
    assert utils.normalize_quoted_printable('test.sample!sample@test/') == 'test.sample=21sample@test=2F'

def test_quoted_printable_normalization_bytes():
    assert utils.normalize_quoted_printable(b'test@test.jp') == 'test@test.jp'
    assert utils.normalize_quoted_printable(b'test-@test') == 'test-@test'
    assert utils.normalize_quoted_printable(b'entity://test@test') == 'entity:=2F=2Ftest@test'
    assert utils.normalize_quoted_printable(b'entity://test!sample@test') == 'entity:=2F=2Ftest=21sample@test'
