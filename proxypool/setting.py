
#数据库
REDIS_HOST = 'localhost'  # Redis数据库地址
REDIS_PORT = 6379          # Redis端口
REDIS_PASSWORD = 'foobared'  # Redis密码，如无填None   foobared
REDIS_KEY = 'proxies'   #有序集合的键名

# 代理分数
MAX_SCORE = 100  #最大分数
MIN_SCORE = 0    #最小分数
INITIAL_SCORE = 10 #初始分数

#实测的正常返回码
VALID_STATUS_CODES = [200]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 10000


TESTER_CYCLE = 20# 检查周期

GETTER_CYCLE = 20# 获取周期

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'http://www.baidu.com'

# API配置
API_HOST = '127.0.0.1'
API_PORT = 5555

# 各模块开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 100
