
# Please install OpenAI SDK first: `pip3 install openai`
from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from openai import OpenAI
import json

router = APIRouter()

@router.post("/chat",summary="非流式接口测试")
def chat(userinput: str = Body(embed=True)): 
    client = OpenAI(api_key="sk-ce44bf08c9964ea182e64daf50d082e9", base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": userinput},
        ],      
        stream=False,
        temperature=1.2  # 设置temperature参数为1.2，增加响应的创造性和多样性
    )
    print(response.choices[0].message.content)
    ai_response = response.choices[0].message.content
    return ai_response

@router.post("/chat_stream",summary="流式接口测试")
def chat_stream(userinput: str = Body(embed=True)):
    """
    流式返回聊天接口，实时返回AI生成的内容
    """
    def generate():
        try:
            client = OpenAI(api_key="sk-ce44bf08c9964ea182e64daf50d082e9", base_url="https://api.deepseek.com")
            stream = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": userinput},
                ],
                stream=True
            )
            
            # 初始化完整响应文本
            full_response = ""
            
            for chunk in stream:
                # 打印每个接收到的chunk
                print("Received chunk:", chunk)
                
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    # 返回当前chunk和累积的完整响应
                    yield f"data: {json.dumps({'delta': content, 'content': full_response}, ensure_ascii=False)}\n\n"
            
            # 发送完成信号
            yield f"data: {json.dumps({'finish': True}, ensure_ascii=False)}\n\n"
            
        except Exception as e:
            error_message = f"处理请求时发生错误: {str(e)}"
            print(error_message)
            yield f"data: {json.dumps({'error': error_message}, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@router.post("/chat_divination",summary="易经大师接口测试")
async def chat_divination(question: str = Body(), current: str = Body(), future: str = Body()):
    """
    流式返回聊天接口，实时返回AI生成的内容
    """
    # 定义易经大师的提示模板
    prompt: str = f"""
    <prompt>
        <identity>你是一位中国易经大师，精通《易经》六十四卦、阴阳五行、八卦风水、命理预测、起名择日等传统文化知识。</identity>
        <expertise>
            <skill>能够深入浅出地解读卦象含义，结合现代语境进行分析与建议</skill>
            <skill>熟悉汉语表达，语言庄重、简练、富有文化底蕴</skill>
            <skill>能指导用户选择吉日良辰，进行起名、搬迁、婚嫁等事项</skill>
            <skill>擅长根据生辰八字进行命理推算，提供个性化运势解读</skill>
        </expertise>
        <divination>
            <method>三钱法</method>
            <question>{question}</question>
            <hexagrams>
                <current>{current}</current>
                <future>{future}</future>
            </hexagrams>
        </divination>
        <task>
            对用户的问题结合这两个卦象进行分析：
            1、分析当前卦象({current}）所反映的问题现状和处境
            2、分析未来卦象({future}）所反映的发展趋势和前景
            3、结合卦象分析的结果，再输出分析过程和最终结论，必要时给出实际建议
            4、输出的内容应符合以下要求：
                a) 尊重传统文化语境，语言庄重、简练、富有文化底蕴、措辞典雅，逻辑清晰
        </task>
    </prompt>
    """    

    def generate():
        try:
            # 创建API客户端
            client = OpenAI(
                api_key="sk-ce44bf08c9964ea182e64daf50d082e9", 
                base_url="https://api.deepseek.com"
            )
            
            # 创建流式对话
            stream = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": "开始吧"},
                ],
                stream=True
            )
            
            full_response = ""
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    # 构建响应数据
                    response_data = {
                        'delta': content,
                        'content': full_response
                    }
                    yield f"data: {json.dumps(response_data, ensure_ascii=False)}\n\n"
            
            # 发送完成信号
            yield f"data: {json.dumps({'finish': True}, ensure_ascii=False)}\n\n"
        except Exception as e:
            error_message = f"处理请求时发生错误: {str(e)}"
            print(error_message)
            yield f"data: {json.dumps({'error': error_message}, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
