'''
Author       : noeru_desu
Date         : 2021-10-10 10:48:27
LastEditors  : noeru_desu
LastEditTime : 2021-10-31 09:08:21
Description  : 粗略包装的密码验证器
'''
from image_encryptor.common.modules.password_verifier import PasswordDict
from image_encryptor.common.modules.version_adapter import load_encryption_attributes


def get_image_data(file, extra_info='', password_dict: PasswordDict = None):
    '''
    :description: 获取文件尾部的json信息，并自动处理设置的密码
    :param file: 要读取的文件
    :param extra_info: 在输出提示信息时额外显示的内容
    :param password_dict: 提供的密码字典
    :return: (json信息, 出现的错误提示)元组
    '''
    image_data, error = load_encryption_attributes(file)
    if error is not None:
        return None, error
    check_password = True
    password = 100
    password_base64 = 0

    if image_data['has_password']:
        if password_dict is not None:
            password = password_dict.get(image_data['password_base64'], None)
            if password is not None:
                check_password = False

        if check_password:
            while True:
                password = input(f'{extra_info}需要解密的图片被密码保护，请输入密码：\n')
                if password == '':
                    continue

                password_base64 = PasswordDict.get_validation_field_base64(password)
                if password_base64 is not None and password_base64 == image_data['password_base64']:
                    password_dict[password_base64] = password
                    break
                else:
                    print('密码错误！', end='')

    image_data['password'] = password
    return image_data, None
