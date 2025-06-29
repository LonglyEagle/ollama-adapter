#!/usr/bin/env python3
"""
简单的API测试脚本
"""

import requests
import json

BASE_URL = "http://localhost:11434"

def test_health():
    """测试健康检查"""
    print("=== 测试健康检查 ===")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_tags():
    """测试本地模型列表"""
    print("\n=== 测试本地模型列表接口 /api/tags ===")
    try:
        response = requests.get(f"{BASE_URL}/api/tags")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"本地模型数量: {len(models)}")
            if models:
                first_model = models[0]
                print(f"第一个模型: {first_model['name']}")
                print(f"模型大小: {first_model['size']} bytes")
                print(f"修改时间: {first_model['modified_at']}")
            return True
        else:
            print(f"请求失败: {response.text}")
            return False
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_generate():
    """测试文本生成"""
    print("\n=== 测试阿里百炼文本生成 ===")
    payload = {
        "model": "dashscope/qwen-turbo",
        "prompt": "你好，请简单介绍一下你自己",
        "stream": False
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/generate", json=payload, timeout=30)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"模型: {data.get('model')}")
            print(f"响应: {data.get('response', '')[:200]}...")
            print(f"完成: {data.get('done')}")
        else:
            print(f"错误响应: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_stream_generate():
    """测试流式文本生成"""
    print("\n=== 测试流式文本生成 ===")
    payload = {
        "model": "dashscope/qwen-turbo",
        "prompt": "请用一句话介绍人工智能",
        "stream": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/generate", json=payload, timeout=30, stream=True)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("流式响应:")
            full_response = ""
            chunk_count = 0
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    # 处理Server-Sent Events格式
                    if line_str.startswith('data: '):
                        json_str = line_str[6:]  # 移除"data: "前缀
                        try:
                            data = json.loads(json_str)
                            if 'response' in data:
                                chunk_text = data.get('response', '')
                                full_response += chunk_text
                                print(chunk_text, end='', flush=True)
                                chunk_count += 1
                            if data.get('done', False):
                                print(f"\n流式传输完成，共接收 {chunk_count} 个数据块")
                                print(f"完整响应长度: {len(full_response)} 字符")
                                break
                        except json.JSONDecodeError:
                            continue
        else:
            print(f"错误响应: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_embeddings():
    """测试向量接口（旧版）"""
    print("\n=== 测试向量接口（旧版） ===")
    payload = {
        "model": "dashscope/text-embedding-v4",
        "prompt": "人工智能是一门研究如何让机器模拟人类智能的科学",
        "dimensions": 1024,
        "encoding_format": "float"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/embeddings", json=payload, timeout=30)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"模型: {data.get('model')}")
            embeddings = data.get('embedding', [])
            if embeddings:
                print(f"向量维度: {len(embeddings)}")
                print(f"向量前5个值: {embeddings[:5]}")
                print(f"向量后5个值: {embeddings[-5:]}")
            else:
                print("未获取到向量数据")
        else:
            print(f"错误响应: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_chat():
    """测试聊天接口"""
    print("\n=== 测试聊天接口 ===")
    payload = {
        "model": "dashscope/qwen-turbo",
        "messages": [
            {"role": "system", "content": "你是一个有用的AI助手。"},
            {"role": "user", "content": "请简单介绍一下人工智能的发展历史"}
        ],
        "stream": False
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=30)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"模型: {data.get('model')}")
            message = data.get('message', {})
            print(f"角色: {message.get('role')}")
            print(f"内容: {message.get('content', '')[:200]}...")
            print(f"完成: {data.get('done')}")
        else:
            print(f"错误响应: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_embed():
    """测试新版嵌入接口"""
    print("\n=== 测试新版嵌入接口 ===")
    payload = {
        "model": "dashscope/text-embedding-v4",
        "input": [
            "人工智能是一门研究如何让机器模拟人类智能的科学",
            "机器学习是人工智能的一个重要分支"
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/embed", json=payload, timeout=30)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"模型: {data.get('model')}")
            embeddings = data.get('embeddings', [])
            if embeddings:
                print(f"嵌入向量数量: {len(embeddings)}")
                for i, embedding in enumerate(embeddings):
                    print(f"向量{i+1}维度: {len(embedding)}")
                    print(f"向量{i+1}前5个值: {embedding[:5]}")
            else:
                print("未获取到嵌入向量数据")
        else:
            print(f"错误响应: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_ps_api():
    """测试运行中模型列表接口 /api/ps"""
    print("\n=== 测试运行中模型列表接口 /api/ps ===")
    
    try:
        response = requests.get(f"{BASE_URL}/api/ps")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"运行中模型数量: {len(data.get('models', []))}")
            if data.get('models'):
                first_model = data['models'][0]
                print(f"第一个模型: {first_model.get('name')}")
                print(f"模型大小: {first_model.get('size')} bytes")
                print(f"过期时间: {first_model.get('expires_at')}")
            print("✅ 运行中模型列表接口测试通过")
            return True
        else:
            print(f"❌ 运行中模型列表接口测试失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 运行中模型列表接口测试出错: {e}")
        return False

def main():
    print("Ollama Adapter 简单测试")
    print("=" * 40)
    
    tests = [
        ("健康检查", test_health),
        ("本地模型列表", test_tags),
        ("文本生成", test_generate),
        ("流式文本生成", test_stream_generate),
        ("聊天接口", test_chat),
        ("向量接口（旧版）", test_embeddings),
        ("嵌入接口（新版）", test_embed),
        ("运行中模型列表", test_ps_api),
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
        print(f"{name}: {'✅ 通过' if result else '❌ 失败'}")
    
    print("\n" + "=" * 40)
    passed = sum(1 for _, result in results if result)
    print(f"测试结果: {passed}/{len(results)} 通过")

if __name__ == "__main__":
    main()