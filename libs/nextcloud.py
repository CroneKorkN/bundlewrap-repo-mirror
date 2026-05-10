"""nextcloud: build `sudo -u www-data php occ ...` shell strings for use in actions."""


def occ(command, *args, **kwargs):
    return f"""sudo -u www-data php /opt/nextcloud/occ {command} {' '.join(args)} {' '.join(f'--{name.replace("_", "-")}' + (f'={value}' if value else '') for name, value in kwargs.items())}"""
