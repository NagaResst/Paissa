#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络连接测试脚本 - 严格超时测试
达到超时设定立即判定为超时，不等待真实响应
"""

import sys
import time
import threading
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class TimeoutTestRunner:
    """超时测试运行器 - 达到时限立即判定超时"""
    
    def __init__(self, timeout):
        self.timeout = timeout
        self.result = None
        self.finished = False
        self.timed_out = False
        
    def _run_request(self, func, *args, **kwargs):
        """在独立线程中运行请求"""
        try:
            self.result = func(*args, **kwargs)
            if not self.timed_out:  # 只有在未超时的情况下才标记完成
                self.finished = True
        except Exception as e:
            self.result = e
            if not self.timed_out:
                self.finished = True
    
    def run_with_timeout(self, func, *args, **kwargs):
        """运行带超时控制的请求"""
        # 启动请求线程
        thread = threading.Thread(target=self._run_request, args=(func,) + args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        
        # 等待超时或完成
        thread.join(timeout=self.timeout)
        
        # 检查是否超时
        if not self.finished:
            self.timed_out = True
            return None, True  # 返回None表示超时
        else:
            return self.result, False  # 返回结果表示成功

def test_single_interface_enforced(name: str, url: str, timeout: int, test_count: int = 3):
    """强制超时测试单个接口"""
    print(f"\n📍 {name}")
    print(f"   URL: {url}")
    print(f"   强制超时: {timeout}秒")
    print(f"   测试次数: {test_count}次")
    print("-" * 50)
    
    results = {
        'success_count': 0,
        'timeout_count': 0,
        'error_count': 0,
        'times': []
    }
    
    # 导入HTTP客户端
    from network.client import http_client
    
    for i in range(test_count):
        print(f"   🎯 第{i+1}次测试...", end=" ")
        
        start_time = time.time()
        
        # 创建超时测试运行器
        runner = TimeoutTestRunner(timeout)
        
        try:
            # 根据URL类型选择合适的请求方法
            if url.endswith('.json') or 'version' in url:
                result, timed_out = runner.run_with_timeout(http_client.get_json, url, timeout)
            else:
                result, timed_out = runner.run_with_timeout(http_client.get_text, url, timeout)
            
            request_time = time.time() - start_time
            
            if timed_out:
                results['timeout_count'] += 1
                print(f"⏰ 超时 ({timeout}秒)")
            elif isinstance(result, Exception):
                results['error_count'] += 1
                print(f"❌ 错误: {type(result).__name__}")
            elif result:
                results['success_count'] += 1
                results['times'].append(request_time)
                print(f"✅ 成功 ({request_time:.2f}秒)")
            else:
                results['error_count'] += 1
                print(f"❌ 无数据")
                
        except Exception as e:
            results['error_count'] += 1
            print(f"❌ 异常: {type(e).__name__}")
        
        # 测试间隔
        if i < test_count - 1:
            time.sleep(0.5)
    
    # 统计结果
    total_tests = results['success_count'] + results['timeout_count'] + results['error_count']
    success_rate = (results['success_count'] / total_tests * 100) if total_tests > 0 else 0
    timeout_rate = (results['timeout_count'] / total_tests * 100) if total_tests > 0 else 0
    
    avg_time = sum(results['times']) / len(results['times']) if results['times'] else 0
    min_time = min(results['times']) if results['times'] else 0
    max_time = max(results['times']) if results['times'] else 0
    
    print(f"   📊 成功率: {success_rate:.1f}% ({results['success_count']}/{total_tests})")
    print(f"   ⏰ 超时率: {timeout_rate:.1f}% ({results['timeout_count']}/{total_tests})")
    if results['times']:
        print(f"   ⏱️  耗时: 平均{avg_time:.2f}秒 (最快{min_time:.2f}s, 最慢{max_time:.2f}s)")
    
    return {
        'name': name,
        'success_rate': success_rate,
        'timeout_rate': timeout_rate,
        'avg_time': avg_time,
        'min_time': min_time,
        'max_time': max_time,
        'total_tests': total_tests,
        'times': results['times']
    }

def test_network_enforced():
    print("⚡ 强制超时网络测试")
    print("=" * 60)
    
    # 导入配置
    import config
    from Data.logger import logger
    
    print(f"🔧 配置参数:")
    print(f"   超时设置: {config.Config.TIMEOUT_SETTINGS}")
    print(f"   最大重试: {config.Config.MAX_RETRY_ATTEMPTS}次")
    print()
    
    # 定义要测试的接口（强制超时）
    test_interfaces = [
        {
            'name': '版本检查接口',
            'url': 'https://paissa-data.oss-cn-hongkong.aliyuncs.com/version',
            'timeout': 3,  # 强制3秒超时
            'test_count': 9
        },
        {
            'name': '市场可交易物品',
            'url': 'https://universalis.app/api/marketable',
            'timeout': 3,  # 强制2秒超时
            'test_count': 3
        },
        {
            'name': '世界服务器列表',
            'url': 'https://universalis.app/api/v2/worlds',
            'timeout': 2,  # 强制2秒超时
            'test_count': 3
        }
    ]
    
    # 执行测试
    all_results = []
    successful_interfaces = 0
    
    print(f"🚀 开始强制超时测试 {len(test_interfaces)} 个接口")
    print("=" * 60)
    
    for interface in test_interfaces:
        result = test_single_interface_enforced(
            interface['name'],
            interface['url'],
            interface['timeout'],
            interface['test_count']
        )
        all_results.append(result)
        
        if result['success_rate'] > 0:
            successful_interfaces += 1
    
    # 生成汇总报告
    print("\n" + "=" * 60)
    print("📊 强制超时测试报告")
    print("=" * 60)
    
    total_tests = sum(r['total_tests'] for r in all_results)
    total_successful = sum(1 for r in all_results if r['success_rate'] > 0)
    total_timeouts = sum(r['timeout_rate'] for r in all_results) / len(all_results)
    
    print(f"🌐 接口总数: {len(test_interfaces)}")
    print(f"✅ 成功接口: {total_successful}")
    print(f"⏰ 超时接口: {len(test_interfaces) - total_successful}")
    print(f"📈 平均超时率: {total_timeouts:.1f}%")
    
    if total_tests > 0:
        overall_success_rate = sum(r['success_rate'] for r in all_results) / len(all_results)
        print(f"📈 平均成功率: {overall_success_rate:.1f}%")
        
        # 评级
        if overall_success_rate >= 90:
            rating = "🌟 优秀"
        elif overall_success_rate >= 70:
            rating = "👍 良好"
        elif overall_success_rate >= 50:
            rating = "⚠️  一般"
        else:
            rating = "❌ 较差"
        print(f"🏆 网络质量评级: {rating}")
    
    print("\n📋 详细结果:")
    print("-" * 60)
    for result in all_results:
        status = "✅" if result['success_rate'] > 0 else "⏰"
        print(f"{status} {result['name']}: {result['success_rate']:.1f}%成功率, {result['timeout_rate']:.1f}%超时")
        if 'times' in result and result['times']:
            print(f"   平均响应: {result['avg_time']:.2f}秒")
        elif result['success_rate'] == 0:
            print(f"   无成功请求")
    
    # 关闭连接
    from network.client import http_client
    http_client.close()
    
    print("\n⚡ 测试特点:")
    print("   • 达到超时设定立即判定超时")
    print("   • 不等待请求真实完成")
    print("   • 强制时间限制")
    print("   • 快速获得测试结果")

# 添加必要的导入
import requests

if __name__ == "__main__":
    test_network_enforced()