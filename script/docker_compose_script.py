import subprocess
import logging

logging.basicConfig(
    filename='./log/access.log.text',
    format='%(asctime)s - %(name)s - %(levelname)s -%(module)s : %(message)s',
    level=10
)


def run_docker_info():
    try:
        result = subprocess.run(['docker-compose', 'ps', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, encoding='utf-8')
        # 检查命令是否成功执行
        if result.returncode == 0:
            # 清理镜像
            clear_image_result = subprocess.run(['docker', 'rmi', 'it21/rs:latest'], stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                text=True, encoding='utf-8')
            if clear_image_result.returncode == 0:
                logging.info("删除成功：%s", clear_image_result.returncode)
            else:
                logging.info("删除失败：%s", clear_image_result.stderr)
            # 打印标准输出
            update_result = subprocess.run(['docker-compose', 'up', '-d'], stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           text=True, encoding='utf-8')
            if update_result.returncode == 0:
                logging.info("镜像更新成功：%s", update_result.stderr)
            else:
                logging.info("镜像更新失败：%s", update_result.stderr)
        else:
            # 打印错误信息
            logging.info("命令操作失败", result.stderr)
    except Exception as e:
        logging.info(f"An error occurred: {e}")


# 调用函数
run_docker_info()
