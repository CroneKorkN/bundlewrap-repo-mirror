# uv is not in Debian Trixie's apt archive (only experimental/sid), so a
# pinned release from astral-sh/uv, checked against its SHA256 sibling
version = node.metadata.get('uv/version')

actions['install_uv'] = {
    'command': f"""set -e
tmpdir=$(mktemp -d); trap "rm -rf $tmpdir" EXIT
base=https://github.com/astral-sh/uv/releases/download/{version}
tar=uv-x86_64-unknown-linux-gnu.tar.gz
curl -fsSL -o $tmpdir/$tar        $base/$tar
curl -fsSL -o $tmpdir/$tar.sha256 $base/$tar.sha256
(cd $tmpdir && sha256sum -c $tar.sha256)
tar -xzf $tmpdir/$tar -C $tmpdir --strip-components=1
install -m 0755 $tmpdir/uv  /usr/local/bin/uv
install -m 0755 $tmpdir/uvx /usr/local/bin/uvx
""",
    # prints "uv 0.11.8 (x86_64-unknown-linux-gnu)"
    'unless': f'/usr/local/bin/uv --version 2>/dev/null | grep -q "^uv {version} "',
    'cascade_skip': False,
    'needs': [
        'pkg_apt:curl',
    ],
}
