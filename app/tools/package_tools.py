import os


def install_package(package_name, version):
    """
        using pip to install python package
    :param package_name: str package name
    :param version: version
    :return:
    """
    if not package_name:
        return
    try:
        os_result = os.popen('pip3 show --files %s' % package_name).read()
        if not os_result.find('Version') > -1:
            print('正在安装 %s ...' % package_name)
            if version and version != '' and version != 'release':
                os_result = os.popen('pip3 install %s==%s' % (package_name, version)).read()
            else:
                os_result = os.popen('pip3 install %s' % package_name).read()

            os_result = os.popen('pip3 show --files %s' % package_name).read()
            if len(os_result.split('\n')[1].split(': ')[1]) > -1:
                print('%s Version: %s 安装完成' % (package_name, os_result.split('\n')[1].split(': ')[1]))
        else:
            os_result = os.popen('pip3 show --files %s' % package_name).read()
            if len(os_result.split('\n')[1].split(': ')[1]) > -1:
                print('%s Version: %s' % (package_name, os_result.split('\n')[1].split(': ')[1]))

    except Exception as ex:
        print(ex)


def get_package_info(package_name):
    """
        get installed package information
    :param package_name: str package name
    :return: version
    """
    return os.popen('pip3 show --files %s' % package_name).read().split('\n')[1].split(' ')[1]
