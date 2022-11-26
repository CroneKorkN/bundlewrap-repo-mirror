directories['/Users/mwiegand/.config/bundlewrap/lock'] = {}

files['/Users/mwiegand/.bin/macbook-update'] = {
    'mode': '755',
}

for element in [*files.values(), *directories.values()]:
    element.update({
        'owner': 'mwiegand',
        'group': 'staff',
        **element,
    })
