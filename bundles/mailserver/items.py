assert node.has_bundle('postfix')
assert node.has_bundle('dovecot')
assert node.has_bundle('letsencrypt')
assert node.has_bundle('roundcube')

from hashlib import md5
from shlex import quote

db_data = node.metadata.get('mailserver/database')
test_password = str(node.metadata.get('mailserver/test_password'))
setup = f"""
    CREATE TABLE domains (
        "id" BIGSERIAL PRIMARY KEY,
        "name" varchar(255) UNIQUE NOT NULL
    );
    CREATE INDEX ON domains ("name");

    CREATE TABLE users (
        "id" BIGSERIAL PRIMARY KEY,
        "name" varchar(255) NOT NULL,
        "domain_id" BIGSERIAL REFERENCES domains(id),
        "password" varchar(255) NULL,
        "redirect" varchar(255) DEFAULT NULL
    );
    CREATE UNIQUE INDEX ON users ("name", "domain_id") WHERE "redirect" IS NULL;

    -- OWNERSHIPS
    
    ALTER TABLE domains OWNER TO {db_data['user']};
    ALTER TABLE users OWNER TO {db_data['user']};

    -- TEST DATA
    
    INSERT INTO domains (name) VALUES ('example.com');
    
    INSERT INTO users (name, domain_id, password)
    SELECT 'bw_test_user', domains.id, MD5('{test_password}')
    FROM domains
    WHERE domains.name = 'example.com';

    INSERT INTO users (name, domain_id, redirect)
    SELECT 'bw_test_alias', domains.id, 'somewhere@example.com'
    FROM domains
    WHERE domains.name = 'example.com';
"""

actions['initialize_mailserver_db'] = {
    'command': f"psql -d {db_data['name']} -c {quote(setup)}",
    'unless': f"psql -At -d {db_data['name']} -c \"SELECT to_regclass(\'public.users\')\" | grep -q '^users$'",
    'needs': [
        'postgres_db:mailserver',
    ],
}

# testuser

test_password_md5 = md5(str(test_password).encode()).hexdigest()
check_query = """
    SELECT password
    FROM users
    WHERE name = 'bw_test_user'
    AND domain_id = (SELECT id FROM domains WHERE name = 'example.com')
"""
update_query = f"""
    UPDATE users
    SET password = MD5('{test_password}')
    WHERE name = 'bw_test_user'
    AND domain_id = (SELECT id FROM domains WHERE name = 'example.com')
"""
actions['mailserver_update_test_pw'] = {
    'command': f"psql -d {db_data['name']} -c {quote(update_query)}",
    'unless': f"psql -At -d {db_data['name']} -c {quote(check_query)} | grep -q '^{test_password_md5}$\'",
    'needs': [
        'action:initialize_mailserver_db',
    ],
}
