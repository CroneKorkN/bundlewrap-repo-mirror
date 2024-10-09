from bundlewrap.items import Item, ItemStatus
from bundlewrap.exceptions import BundleError
from bundlewrap.utils.text import force_text, mark_for_translation as _
from bundlewrap.utils.remote import PathInfo
import types
from shlex import quote

# Downloaded from https://github.com/bundlewrap/plugins/blob/master/item_download/items/download.py
# No, we can't use plugins here, because bw4 won't support them anymore.

class Download(Item):
    """
    Download a file and verify its Hash.
    """
    BUNDLE_ATTRIBUTE_NAME = "downloads"
    NEEDS_STATIC = [
        "pkg_apt:",
        "pkg_pacman:",
        "pkg_yum:",
        "pkg_zypper:",
    ]
    ITEM_ATTRIBUTES = {
        'url': None,
        'sha256': None,
        'sha256_url': None,
        'gpg_signature_url': None,
        'gpg_pubkey_url': None,
        'verifySSL': True,
        'decompress': None,
    }
    ITEM_TYPE_NAME = "download"
    REQUIRED_ATTRIBUTES = ['url']

    def __repr__(self):
        return "<Download name:{}>".format(self.name)

    def __hash_remote_file(self, filename):
        path_info = PathInfo(self.node, filename)
        if not path_info.is_file:
            return None

        if hasattr(path_info, 'sha256'):
            return path_info.sha256
        else:
            """"pending pr so do it manualy"""
            if self.node.os == 'macos':
                result = self.node.run("shasum -a 256 -- {}".format(quote(filename)))
            elif self.node.os in self.node.OS_FAMILY_BSD:
                result = self.node.run("sha256 -q -- {}".format(quote(filename)))
            else:
                result = self.node.run("sha256sum -- {}".format(quote(filename)))
            return force_text(result.stdout).strip().split()[0]

    def fix(self, status):
        if status.must_be_deleted:
            # Not possible
            pass
        else:
            decompress = self.attributes.get('decompress')
            # download file
            self.node.run("curl -L {verify}-s -- {url}{pipe} > {file}".format(
                pipe = ' | ' + decompress if decompress else '',
                verify="" if self.attributes.get('verifySSL', True) else "-k ",
                file=quote(self.name),
                url=quote(self.attributes['url'])
            ))

    def cdict(self):
        """This is how the world should be"""
        cdict = {
            'type': 'download',
        }

        if self.attributes.get('sha256'):
            cdict['sha256'] = self.attributes['sha256']
        elif self.attributes.get('gpg_signature_url'):
            cdict['verified'] = True
        elif self.attributes.get('sha256_url'):
            full_sha256_url = self.attributes['sha256_url'].format(url=self.attributes['url'])
            cdict['sha256'] = force_text(
                self.node.run(f"curl -sL -- {quote(full_sha256_url)}").stdout
            ).strip().split()[0]
        else:
            raise

        return cdict

    def sdict(self):
        """This is how the world is right now"""
        path_info = PathInfo(self.node, self.name)
        if not path_info.exists:
            return None
        else:
            sdict = {
                'type': 'download',
            }
            if self.attributes.get('sha256'):
                sdict['sha256'] = self.__hash_remote_file(self.name)
            elif self.attributes.get('sha256_url'):
                sdict['sha256'] = self.__hash_remote_file(self.name)
            elif self.attributes.get('gpg_signature_url'):
                full_signature_url = self.attributes['gpg_signature_url'].format(url=self.attributes['url'])
                signature_path = f'{self.name}.signature'

                self.node.run(f"curl -sSL {self.attributes['gpg_pubkey_url']} | gpg --import -")
                self.node.run(f"curl -L {full_signature_url} -o {quote(signature_path)}")
                gpg_output = self.node.run(f"gpg --verify {quote(signature_path)} {quote(self.name)}").stderr

                if b'Good signature' in gpg_output:
                    sdict['verified'] = True
                else:
                    sdict['verified'] = False

        return sdict

    @classmethod
    def validate_attributes(cls, bundle, item_id, attributes):
        if (
            'sha256' not in attributes and
            'sha256_url' not in attributes and
            'gpg_signature_url'not in attributes
        ):
            raise BundleError(_(
                "at least one hash must be set on {item} in bundle '{bundle}'"
            ).format(
                bundle=bundle.name,
                item=item_id,
            ))

        if 'url' not in attributes:
            raise BundleError(_(
                "you need to specify the url on {item} in bundle '{bundle}'"
            ).format(
                bundle=bundle.name,
                item=item_id,
            ))

    def get_auto_deps(self, items):
        deps = []
        for item in items:
            # debian TODO: add other package manager
            if item.ITEM_TYPE_NAME == 'pkg_apt' and item.name == 'curl':
                deps.append(item.id)
        return deps
