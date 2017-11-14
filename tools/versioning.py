# -*- coding: utf-8 -*-

import os.path
import subprocess

import baseapp.loader
import tools.data_conversion


__version_config = lambda v: baseapp.loader.Config(baseapp.loader.CONFIG_PATH, v)

def get_ordered_versions():
    return sorted(__version_config('').storage_template)

def get_template(version):
    generate_template = lambda c: c.generate_storage_template(c.default_storage_path[version])
    return generate_template(__version_config(version))

def initialize_template(to_t, path='/tmp'):
    """Create empty directory structure based on version template under $path"""
    for item in to_t:
        os.makedirs(os.path.join(path, to_t[item]))
    with open(os.path.join(path, to_t['ACCOUNT'], 'account.yaml'), 'w') as f:
        f.write('[]')

def pack_template(to_t, with_storage=False, name='data.tar', path='/tmp'):
    """Create tar file based on version template

    If $with_storage, all repo and storage directories will be put in tar file.
    The resulting tar file is stored as $name under $path (default: /tmp/data.tar).
    """
    command = ['tar', 'cvf', os.path.join(path, name)]
    storage_filter = lambda x: x.endswith('_STO') or x.endswith('_REPO')
    command.extend([to_t[option] for option in to_t if not storage_filter(option)])
    if with_storage:
        command.extend([to_t[option] for option in to_t if storage_filter(option)])
    p = subprocess.call(command)
    return p

def remove_template(to_t, path='/tmp'):
    """ Specify $path if you want to do something unsafe."""
    os.chdir(path)
    try:
        os.remove(os.path.join(to_t['ACCOUNT'], 'account.yaml'))
    except OSError:
        pass
    for item in to_t:
        try:
            os.removedirs(to_t[item])
        except OSError:
            continue


def assert_valid_version(version):
    assert version in get_ordered_versions(), ' '.join([version,
        'is not a predefined version'])

def assert_valid_template(version, compatible=True):
    for path in get_template(version).values():
        if compatible:
            assert os.path.isdir(path), ' '.join([path, 'is not directory or compatible'])
        else:
            assert os.path.isdir(path) and not os.path.islink(path), ' '.join([path, 'is not directory'])

def assert_data_version(version, compatible=True):
    """Assert data structure is at the given version"""
    assert_valid_version(version)
    assert_valid_template(version, compatible)


def get_next_version(version):
    """Return the next known version. None otherwise."""
    known_versions = get_ordered_versions()
    try:
        i = known_versions.index(version)
    except ValueError:
        return
    if i == len(known_versions)-1:
        return
    return known_versions[i+1]

def get_data_version():
    """Return the newest version of data matching the templates. None otherwise.

        >>> import os
        >>> import tools.versioning
        >>> os.chdir('/tmp')
        >>> tools.versioning.remove_template(tools.versioning.get_template('1.1'))
        >>> tools.versioning.initialize_template(tools.versioning.get_template('1.1'))
        >>> tools.versioning.get_data_version()
        '1.1'
        >>> tools.versioning.remove_template(tools.versioning.get_template('1.1'))
    """
    version = None
    for v in get_ordered_versions():
        try:
            assert_data_version(v, compatible=False)
            version = v
        except AssertionError:
            if version:
                break
            else:
                continue
    return version


def renames_with_tmp(from_n, to_n):
    """Handle some situations leading to os.renames failure"""
    import time
    if from_n.startswith(to_n+os.sep):
        suffix = time.ctime()
        tmp_from_item = to_n+suffix+from_n.replace(to_n, '')
    else:
        suffix = time.ctime()
        tmp_from_item = from_n+suffix
    try:
        os.renames(from_n, tmp_from_item)
        os.renames(tmp_from_item, to_n)
    except OSError as e:
        e.message = '\''.join(['mv ', tmp_from_item, ' ', to_n])

def update_template(from_t, to_t, backward_compatible=False, restore_backup=True):
    """Update directory structure based on templates"""
    for item in to_t:
        if item in from_t:
            if from_t[item] == to_t[item]:
                continue
            else:
                renames_with_tmp(from_t[item], to_t[item])
            if backward_compatible and not to_t[item].startswith(from_t[item]):
                try:
                    os.symlink(to_t[item], from_t[item])
                except OSError as e:
                    e.message = '\''.join(['ln -sf ', to_t[item], ' ', from_t[item]])
        else:
            if restore_backup and os.path.isdir(to_t[item]+'.bak'):
                renames_with_tmp(to_t[item]+'.bak', to_t[item])
            else:
                try:
                    os.makedirs(to_t[item])
                except OSError:
                    # Already exists
                    pass

def backup_old_template(from_t, to_t):
    """Backup directory structure based on templates

    Use pack_template() instead to backup data in tar file."""
    for item in [_ for _ in from_t if _ not in to_t]:
        if os.path.isdir(from_t[item]):
            renames_with_tmp(from_t[item], from_t[item]+'.bak')
            print(' '.join([from_t[item]+'.bak', 'backup created']))


def update_to_version(version, backward_compatible=True):
    """Make change in directory structure and data to reach a version.

    The given $version is expected to be a future version. Nothing done otherwise.
    If $backward_compatible, symbolic links will match old version template.

        >>> import os
        >>> import tools.versioning
        >>> os.chdir('/tmp')
        >>> tools.versioning.remove_template(tools.versioning.get_template('1.1'))
        >>> tools.versioning.remove_template(tools.versioning.get_template('1.2'))
        >>> tools.versioning.initialize_template(tools.versioning.get_template('1.1'))
        >>> tools.versioning.update_to_version('1.2')
        >>> tools.versioning.get_data_version()
        '1.2'
        >>> tools.versioning.remove_template(tools.versioning.get_template('1.2'))
    """
    known_versions = get_ordered_versions()
    current_version = get_data_version()
    if not current_version:
        return
    assert_valid_version(version)
    assert known_versions.index(current_version) < known_versions.index(version)

    while (not current_version == version):
        next_version = get_next_version(current_version)
        update_template(get_template(current_version), get_template(next_version))
        try:
            data_conversion_rules = tools.data_conversion.conversion_rules[(current_version, next_version)]
            for rule in data_conversion_rules:
                data_conversion_rules[rule](current_template=get_template(current_version),
                                            next_template=get_template(next_version))
        except KeyError:
            pass
        backup_old_template(get_template(current_version), get_template(next_version))
        current_version = next_version
    
