import logging
import logging.handlers

# 로그 생성
root_logger = logging.getLogger('root')

# 로그의 출력 기준 설정
root_logger.setLevel(logging.DEBUG)

# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
root_logger.addHandler(stream_handler)

# log를 파일에 출력
file_handler = logging.handlers.RotatingFileHandler('/log/elastic.log',
                                                    maxBytes=1024 * 1024,
                                                    backupCount=5)

file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)
