# the mail server's own postfix delivers itself, see bundle postfix
if node.has_bundle('postfix'):
    defaults = {}
else:
    defaults = {
        'apt': {
            'packages': {
                'postfix': {},
                # mail(1), for icinga notifications and tests
                'bsd-mailx': {},
            },
        },
    }

    @metadata_reactor.provides(
        'postfix-relay/relayhost',
    )
    def relayhost(metadata):
        mail_node, = (other for other in repo.nodes if other.has_bundle('mailserver'))

        return {
            'postfix-relay': {
                'relayhost': repo.libs.ip.internal_ip(mail_node.metadata),
            },
        }
