<?php

/**
 * Rehashes the mail password on login when its hash does not match password_algorithm_options.
 * Dovecot reads the argon2 parameters from the stored hash and verifies it on every imap login,
 * which roundcube does on every request.
 */
class argon2_rehash extends rcube_plugin
{
    public $task = 'login';

    #[\Override]
    public function init()
    {
        $this->require_plugin('password');
        $this->add_hook('login_after', [$this, 'login_after']);
    }

    public function login_after($args)
    {
        $rcmail = rcmail::get_instance();
        $db = rcube_db::factory($rcmail->config->get('password_db_dsn'), '', false);
        $result = $db->query(
            'SELECT users.password FROM users JOIN domains ON domains.id = users.domain_id WHERE domains.name = ? AND users.name = ?',
            $rcmail->user->get_username('domain'),
            $rcmail->user->get_username('local'),
        );
        $row = $db->fetch_array($result);

        if ($row) {
            $hash = preg_replace('/^\{[^}]+\}/', '', $row[0]);
            $options = (array) $rcmail->config->get('password_algorithm_options', []);

            if (password_needs_rehash($hash, \PASSWORD_ARGON2ID, $options)) {
                require_once INSTALL_PATH . 'plugins/password/drivers/sql.php';
                $password = $rcmail->get_user_password();
                $driver = new rcube_sql_password();

                if ($driver->save($password, $password, $rcmail->get_user_name()) === PASSWORD_SUCCESS) {
                    rcube::write_log('password', 'Rehashed password for ' . $rcmail->get_user_name());
                }
            }
        }

        return $args;
    }
}
