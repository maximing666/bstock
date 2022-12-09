import logging

# 创建日志对象(不设置时默认名称为root)
log = logging.getLogger('test_http')
# 设置日志级别(默认为WARNING)
log.setLevel('INFO')
# 设置输出渠道(以文件方式输出需设置文件路径)
file_handler = logging.FileHandler('./logs/test.log', encoding='utf-8')
file_handler.setLevel('INFO')
# 设置输出格式(实例化渠道)
fmt_str = '%(asctime)s %(thread)d %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
formatter = logging.Formatter(fmt_str)
# 绑定渠道的输出格式
file_handler.setFormatter(formatter)
# 绑定渠道到日志收集器
log.addHandler(file_handler)

log.info("123")