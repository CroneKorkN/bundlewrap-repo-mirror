assert node.has_bundle('postfix')
assert node.has_bundle('dovecot')
assert node.has_bundle('letsencrypt')
assert node.has_bundle('roundcube')

from shlex import quote

setup = '''
    CREATE TABLE domains (
        "id" BIGSERIAL PRIMARY KEY,
        "name" varchar(255) UNIQUE NOT NULL
    );
    CREATE INDEX ON domains ("name");

    CREATE TABLE users (
        "id" BIGSERIAL PRIMARY KEY,
        "name" varchar(255) NOT NULL,
        "domain_id" BIGSERIAL NOT NULL,
        CONSTRAINT "fk_domain"
            FOREIGN KEY("domain_id") 
                REFERENCES domains("id"),
        "password" varchar(255) NULL,
        "redirect" varchar(255) DEFAULT NULL
    );
    CREATE UNIQUE INDEX ON users ("name", "domain_id") WHERE "redirect" IS NULL;
'''

actions['initialize_mailserver_db'] = {
    'command': f'psql -d mailserver -c {quote(setup)}',
    'unless': f'psql -At -d mailserver -c "SELECT to_regclass(\'public.users\')" | grep -q \'^users$\'',
    'needs': [
        'postgres_db:mailserver',
    ],
}


# TEST
'''
DROP TABLE users; DROP TABLE domains;

INSERT INTO domains (id, name)
VALUES (1, 'mails2.sublimity.de');
INSERT INTO users (id, name, domain_id, password)
VALUES (1, 'ckn', 1, MD5('test123'));
INSERT INTO users (id, name, domain_id, redirect)
VALUES (1, 'weg', 1, 'irgendweo@gmail.com');
'''
