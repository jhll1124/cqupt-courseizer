import yaml
import os
import sys
import logging


class ConfigLoader:
    """配置文件加载器"""
    
    def __init__(self, config_path="config.yml"):
        self.config_path = config_path
        self.config = None
        
    def load(self):
        """加载配置文件"""
        if not os.path.exists(self.config_path):
            logging.error(f"配置文件不存在: {self.config_path}")
            logging.info("请复制 config.yml 并填写你的配置")
            sys.exit(1)
            
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logging.error(f"配置文件格式错误: {e}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"读取配置文件失败: {e}")
            sys.exit(1)
            
        # 验证配置
        self._validate()
        return self.config
    
    def _validate(self):
        """验证配置文件的必填项"""
        if not self.config:
            logging.error("配置文件为空")
            sys.exit(1)
            
        # 检查 cookie
        if 'cookie' not in self.config or not self.config['cookie']:
            logging.error("配置文件中缺少 cookie")
            sys.exit(1)
            
        if self.config['cookie'] == "PHPSESSID=your_cookie_here":
            logging.error("请在配置文件中填写真实的 cookie，不要使用默认值")
            sys.exit(1)
            
        # 检查课程列表
        if 'courses' not in self.config or not self.config['courses']:
            logging.error("配置文件中缺少 courses（课程列表）")
            sys.exit(1)
            
        if not isinstance(self.config['courses'], list):
            logging.error("courses 必须是列表格式")
            sys.exit(1)
            
        if len(self.config['courses']) == 0:
            logging.error("courses 列表不能为空，请至少添加一门课程")
            sys.exit(1)
            
        # 设置默认值
        if 'mode' not in self.config:
            self.config['mode'] = 1
            
        if 'log_level' not in self.config:
            self.config['log_level'] = 'INFO'
            
        logging.info("配置文件验证通过")
    
    def get_cookie(self):
        """获取 cookie"""
        return self.config.get('cookie', '')
    
    def get_mode(self):
        """获取抢课模式"""
        return self.config.get('mode', 1)
    
    def get_courses(self):
        """获取课程列表"""
        return self.config.get('courses', [])
    
    def get_log_level(self):
        """获取日志级别"""
        level_str = self.config.get('log_level', 'INFO').upper()
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return level_map.get(level_str, logging.INFO)
