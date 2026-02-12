# Paissa 开发指南

## 项目结构

```
Paissa/
├── Data/                 # 数据文件目录
│   ├── item.Pdt         # 物品数据文件
│   ├── marketable.py    # 可交易物品列表
│   └── logger.py        # 日志模块
├── UI/                  # 界面文件目录
│   ├── *.ui             # Qt Designer界面文件
│   └── *.py             # 转换后的Python界面文件
├── cache/               # 缓存模块
│   └── manager.py       # 缓存管理器
├── network/             # 网络模块
│   └── client.py        # HTTP客户端
├── tests/               # 测试文件
│   └── test_core.py     # 核心功能测试
├── config.py            # 配置管理
├── main.py              # 新的主程序入口
├── Paissa.py            # 原始主程序（保留兼容性）
├── Queryer.py           # 数据查询核心模块
├── Window.py            # 主窗口逻辑
├── requirements.txt     # 依赖列表
└── setup.py            # 安装配置
```

## 开发环境搭建

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试文件
python -m pytest tests/test_core.py -v

# 生成覆盖率报告
pip install pytest-cov
python -m pytest tests/ --cov=. --cov-report=html
```

### 3. 代码格式化

```bash
# 使用black格式化代码
black .

# 使用flake8检查代码质量
flake8 .
```

## 核心模块说明

### Config 配置管理
统一管理项目的所有配置项，包括路径、超时设置等。

### HttpClient 网络客户端
- 基于requests.Session的封装
- 支持连接池和自动重试
- 统一的异常处理

### CacheManager 缓存管理器
- 基于内存的LRU缓存
- 支持过期时间设置
- 提供缓存统计功能

### Logger 增强日志
- 支持控制台和文件双重输出
- 包含性能监控功能
- 自动创建日志目录

## 主要优化点

### 1. 异常处理改进
```python
# 旧代码 - 不推荐
except:
    logger.warn("出错了")

# 新代码 - 推荐
except requests.RequestException as e:
    logger.warning(f"网络请求失败: {e}")
except json.JSONDecodeError as e:
    logger.warning(f"JSON解析失败: {e}")
```

### 2. 类型提示
```python
from typing import Optional, Dict, List

def query_item(self, item_name: str) -> Optional[List[Dict]]:
    """查询物品信息"""
    pass
```

### 3. 性能监控
```python
from Data.logger import log_performance

@log_performance
def expensive_function():
    # 函数执行会被自动计时并记录
    pass
```

## 开发规范

### 代码风格
- 遵循PEP 8规范
- 使用类型提示
- 添加docstring文档
- 保持函数单一职责

### Git提交规范
```
feat: 新功能
fix: 修复bug
refactor: 代码重构
docs: 文档更新
test: 测试相关
chore: 构建过程或辅助工具的变动
```

### 测试要求
- 新功能必须包含单元测试
- 修改现有功能需确保测试通过
- 测试覆盖率应达到80%以上

## 部署流程

### 1. 本地测试
```bash
python -m pytest tests/ -v
python Paissa.py  # 测试新入口
python Paissa.py  # 确保旧入口仍可用
```

### 2. 打包发布
```bash
# 安装打包工具
pip install pyinstaller

# 打包为exe
pyinstaller --onefile --windowed Paissa.py
```

### 3. 版本发布
1. 更新版本号
2. 更新CHANGELOG.md
3. 创建Git标签
4. 上传到GitHub Releases

## 常见问题

### Q: 如何添加新的API接口？
A: 在network/client.py中扩展HttpClient类，添加相应的方法。

### Q: 缓存如何工作？
A: 使用装饰器`@cache_manager.cache_with_expire(expire_time)`包装需要缓存的函数。

### Q: 日志文件在哪里？
A: 默认在Data/Paissa.log，性能日志在Data/Paissa_perf.log。

## 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

---
如需帮助，请联系：夕山菀 @ 紫水栈桥