if __name__ == '__main__':
    from math import ceil
    from os.path import normpath, splitext
    from sys import exit

    from Crypto.Cipher import AES
    from PIL import Image, UnidentifiedImageError
    from progressbar import Bar, Percentage, ProgressBar, SimpleProgress

    from modules.AES import decrypt
    from modules.image_cryptor import XOR_image, generate_decrypted_image, get_mapping_lists
    from modules.loader import get_instances, create_process_pool
    from modules.utils import pause
    from modules.version_adapter import load_encryption_attributes

    program = get_instances()

    if 'path' not in program.parameter:
        program.logger.error('没有输入文件')
        pause()
        exit()

    program.parameter['path'] = normpath(program.parameter['path'])

    try:
        img = Image.open(program.parameter['path']).convert('RGBA')
    except FileNotFoundError:
        program.logger.error('文件不存在')
        pause()
        exit()
    except UnidentifiedImageError:
        program.logger.error('无法打开或识别图像格式，或输入了不受支持的格式')
        pause()
        exit()

    size = img.size
    program.logger.info(f'导入大小：{size[0]}x{size[1]}')

    image_data = load_encryption_attributes()
    pw = 100

    if image_data['has_password']:
        input_pw = ''
        while True:
            input_pw = input('需要解密的图片被密码保护，请输入密码：')
            if input_pw == '':
                continue
            try:
                if decrypt(AES.MODE_CFB, input_pw, image_data['password_base64'], str(image_data['width']) + str(image_data['height']), True) == 'PASS':
                    break
                else:
                    program.logger.warning('密码错误！')
            except UnicodeDecodeError:
                program.logger.warning('密码错误！')
        pw = input_pw
    program.logger.info(f"原始图片信息：大小：{image_data['width']}x{image_data['height']}; 分块数量：{image_data['col']}x{image_data['row']}")

    block_width = ceil(size[0] / image_data['col'])
    block_height = ceil(size[1] / image_data['row'])
    program.logger.info(f'分块大小：{block_width}x{block_height}')
    widgets = [Percentage(), ' ', SimpleProgress(), ' ', Bar('█'), ' ']
    program.logger.info('正在处理')
    program.logger.info('正在生成映射列表')

    bar = ProgressBar(max_value=image_data['col'] * image_data['row'], widgets=widgets)
    regions, pos_list, flip_list = get_mapping_lists(img, pw, image_data['row'], image_data['col'], block_width, block_height, bar)

    program.logger.info('正在重组')

    bar = ProgressBar(max_value=image_data['col'] * image_data['row'], widgets=widgets)
    new_image = generate_decrypted_image(regions, pos_list, flip_list, image_data['row'], image_data['col'], block_width, block_height, image_data['rgb_mapping'], bar)

    if image_data['xor_rgb']:
        create_process_pool()
        program.logger.info('正在异或解密，性能较低，请耐心等待')
        size = new_image.size
        new_image = XOR_image(new_image, pw, image_data['xor_alpha'], program.process_pool, program.parameter['process_count'])

    program.logger.info('正在保存文件')
    original_image = new_image.crop((0, 0, int(image_data['width']), int(image_data['height'])))

    name, suffix = splitext(program.parameter['path'])
    suffix = program.parameter['format'] if program.parameter['format'] != 'normal' else suffix
    suffix = suffix.strip('.')
    if suffix.lower() in ['jpg', 'jpeg']:
        original_image = original_image.convert('RGB')
    name = name.replace('-encrypted', '')

    original_image.save(name + '-decrypted.' + suffix, quality=100)
