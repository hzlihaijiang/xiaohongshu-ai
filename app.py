import streamlit as st
from openai import OpenAI

# --- 页面配置 ---
st.set_page_config(page_title="🍠 小红书爆款文案生成器", page_icon="🍠")

st.title("🍠 小红书 AI 文案助手")
st.markdown("输入主题，一键生成带 Emoji、标签的爆款笔记！")

# --- 侧边栏：设置 API Key ---
with st.sidebar:
    st.header("⚙️ 设置")
    api_key = st.text_input("请输入 DeepSeek API Key", type="password", placeholder="sk-...")
    st.markdown("[点击获取 API Key](https://platform.deepseek.com/)")
    st.info("提示：Key 仅保存在你的浏览器本地，不会上传到服务器。")

# --- 主界面 ---
topic = st.text_input("📝 笔记主题是什么？", placeholder="例如：周末去上海武康路探店、新手如何学Python、减脂餐推荐")
tone = st.selectbox("🎭 想要什么风格？", ["热情闺蜜风", "专业干货风", "搞笑吐槽风", "温柔治愈风"])

if st.button("✨ 开始生成文案", type="primary"):
    if not api_key:
        st.error("❌ 请先在左侧侧边栏输入 API Key！")
    elif not topic:
        st.warning("⚠️ 请先输入笔记主题！")
    else:
        try:
            # 显示加载动画
            with st.spinner('AI 正在疯狂构思中...'):
                
                # 初始化客户端
                client = OpenAI(
                    api_key=api_key, 
                    base_url="https://api.deepseek.com" # DeepSeek 的地址
                )

                # 构建提示词 (Prompt)
                system_prompt = "你是一位拥有百万粉丝的小红书爆款博主。擅长捕捉热点，语气生动，喜欢使用 Emoji 表情。"
                
                user_prompt = f"""
                请为主题"{topic}"写一篇小红书笔记。
                风格要求：{tone}。
                
                内容结构要求：
                1. 【标题】：生成 3 个吸引人的标题，包含 emoji，利用悬念或痛点。
                2. 【正文】：
                   - 开头：一句话抓住眼球。
                   - 中间：分点叙述（使用 1️⃣2️⃣3️⃣），内容详实，多用 emoji 点缀。
                   - 结尾：引导互动（如“收藏起来慢慢看”、“评论区告诉我”）。
                3. 【标签】：生成 10 个相关的热门标签，用 # 开头。
                
                请直接输出内容，不要解释。
                """

                # 调用大模型
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.8 # 让回答更有创意
                )

                result = response.choices[0].message.content
                
                # 展示结果
                st.success("✅ 生成成功！")
                st.markdown("---")
                st.markdown(result)
                
                # 提供复制按钮
                st.download_button(
                    label="📥 复制文案到剪贴板 (手动复制下方文本)",
                    data=result,
                    file_name="xiaohongshu_copy.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"❌ 出错了：{str(e)}")
            st.info("请检查 API Key 是否正确，或者网络是否通畅。")

# 页脚
st.markdown("---")
st.caption("Powered by Streamlit & DeepSeek | 仅供学习使用")
