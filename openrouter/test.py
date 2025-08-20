import requests
import json
import os
from typing import Dict, List, Optional

def call_openrouter(
    prompt: str,
    model: str = "deepseek/deepseek-r1:free",
    temperature: float = 0.7,
    top_p: float = 0.95,
    max_tokens: int = 1024,
    api_key: Optional[str] = None
) -> Dict:
    """
    调用OpenRouter API
    
    Args:
        prompt: 用户输入的提示词
        model: 模型名称
        temperature: 温度参数
        top_p: top_p参数
        max_tokens: 最大token数
        api_key: API密钥,如果为None则从环境变量获取
    
    Returns:
        API响应结果
    """
    # 获取API密钥
    api_key = api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OpenRouter API key not found. Please set OPENROUTER_API_KEY environment variable.")

    # 准备请求数据
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
        # "HTTP-Referer": "https://github.com/your-repo",  # 替换为你的项目URL
        # "X-Title": "Verilog Code Generator",  # 替换为你的项目名称
    }
    
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens
    }

    try:
        # 打印请求信息
        print("Request URL:", url)
        print("Request Headers:", json.dumps(headers, indent=2))
        print("Request Data:", json.dumps(data, indent=2))

        # 发送请求
        response = requests.post(url, headers=headers, json=data)
        
        # 打印响应状态
        print("\nResponse Status:", response.status_code)
        print("Response Headers:", dict(response.headers))
        
        # 解析响应
        result = response.json()
        print("\nFull Response:", json.dumps(result, indent=2))
        
        # 检查响应格式
        if "choices" in result and len(result["choices"]) > 0:
            if "message" in result["choices"][0]:
                generated_text = result["choices"][0]["message"]["content"]
                print("\nGenerated text:", generated_text)
                
                # 打印token使用情况
                if "usage" in result:
                    usage = result["usage"]
                    print(f"\nToken usage:")
                    print(f"Prompt tokens: {usage.get('prompt_tokens', 'N/A')}")
                    print(f"Completion tokens: {usage.get('completion_tokens', 'N/A')}")
                    print(f"Total tokens: {usage.get('total_tokens', 'N/A')}")
                
                return result
            else:
                print("No 'message' field in choices[0]")
                print("Choices structure:", json.dumps(result["choices"][0], indent=2))
        else:
            print("No 'choices' field in response or empty choices")
        
        return result
            
    except requests.exceptions.RequestException as e:
        print(f"Error calling OpenRouter API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response text: {e.response.text}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error parsing API response: {e}")
        print(f"Response text: {response.text}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    # 测试调用
    try:
        result = call_openrouter(
            prompt="What is the meaning of life?",
            model="deepseek/deepseek-r1:free",
            temperature=0.7,
            top_p=0.95,
            max_tokens=1024
        )
    except Exception as e:
        print(f"Test failed: {e}")