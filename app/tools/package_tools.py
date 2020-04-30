import os


def install_package(package_name, version):
    """
        安装需要的包
    :param package_name: 包名
    :param version: 版本（空, None, release 则安装最新版本）
    :return:
    """

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
        获取已安装的包版本
    :param package_name: 包名称
    :return: 包版本号
    """
    return os.popen('pip3 show --files %s' % package_name).read().split('\n')[1].split(' ')[1]
