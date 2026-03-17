# 🏛️ AI Court Debate Agent - 线上法庭智能答辩 AI Agent 系统

[English](#english) | [中文](#chinese)

---

<a name="chinese"></a>

## 📖 项目简介

**AI Court Debate Agent** 是一个基于 TEN Framework 构建的智能法庭辩论助手系统。该系统集成了语音识别、大语言模型、法律知识库和案情分析功能，能够实时进行法庭辩论和答辩。

### 🎯 核心功能

1. **实时语音交互**
   - 🎤 语音识别（ASR）：实时识别法官/对方律师的问题
   - 🔊 语音合成（TTS）：将答辩意见转换为自然语音输出

2. **法律知识库**
   - 📚 内置中国刑法、民法典等法律条文
   - 🔍 智能检索相关法律规定
   - 📑 支持按类别和关键词搜索

3. **案情分析引擎**
   - 📊 分析案件事实和证据
   - 🎯 生成辩论策略和要点
   - 🛡️ 基于无罪推定、疑罪从无等法律原则

4. **智能答辩生成**
   - 🤖 基于 OpenAI GPT 模型生成专业答辩意见
   - 📝 自动引用相关法律条文
   - 💡 提供有理有据的法律观点

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                  AI Court Debate Agent                   │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    ┌───▼───┐         ┌─────▼─────┐      ┌─────▼─────┐
    │  ASR  │         │    LLM    │      │    TTS    │
    │ 语音识别│         │ 大语言模型  │      │  语音合成  │
    └───┬───┘         └─────┬─────┘      └─────▲─────┘
        │                   │                   │
        │         ┌─────────▼─────────┐        │
        │         │  Court Debate     │        │
        └────────►│  Control          ├────────┘
                  │  主控制器           │
                  └─────────┬─────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
        ┌───────▼────────┐      ┌──────▼───────┐
        │ Legal Knowledge│      │ Case Analyzer│
        │   法律知识库     │      │   案情分析    │
        └────────────────┘      └──────────────┘
```

### 核心组件

| 组件 | 说明 | 技术栈 |
|------|------|--------|
| **Agora RTC** | 实时音视频通信 | Agora SDK |
| **ASR (Deepgram)** | 语音转文本 | Deepgram API |
| **LLM (OpenAI)** | 智能对话生成 | OpenAI GPT-4 |
| **TTS (ElevenLabs)** | 文本转语音 | ElevenLabs API |
| **Legal Knowledge** | 法律知识库 | Python Extension |
| **Case Analyzer** | 案情分析器 | Python Extension |
| **Court Debate Control** | 主控制逻辑 | Python Extension |

## 🤖 支持的国产大模型

系统提供 5 个预定义图，对应 5 种主流国产大模型（通过 OpenAI 兼容 API 接入）：

| 图名称 | 模型 | 提供商 | API Base URL |
|--------|------|--------|--------------|
| `ai_court_debate_deepseek` ⭐（默认） | deepseek-chat / deepseek-reasoner | [DeepSeek](https://platform.deepseek.com/) | `https://api.deepseek.com/v1` |
| `ai_court_debate_qwen` | qwen-max / qwen-plus | [通义千问(阿里云)](https://dashscope.aliyun.com/) | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `ai_court_debate_kimi` | moonshot-v1-32k | [Kimi(月之暗面)](https://platform.moonshot.cn/) | `https://api.moonshot.cn/v1` |
| `ai_court_debate_glm` | glm-4 / glm-4-flash | [智谱AI(GLM)](https://open.bigmodel.cn/) | `https://open.bigmodel.cn/api/paas/v4` |
| `ai_court_debate_doubao` | doubao-pro-32k | [豆包(字节跳动)](https://www.volcengine.com/product/ark) | `https://ark.cn-beijing.volces.com/api/v3` |

> **推荐**：优先使用 **DeepSeek**（默认），中文理解能力强，推理模型（R1）擅长逻辑分析，非常适合法律场景。

## 🚀 快速开始

### 前置要求

1. **系统要求**
   - Linux / macOS / Windows
   - Go 1.22+
   - Python 3.10+

2. **API Keys**（至少需要以下服务的 API 密钥）
   - [Agora](https://www.agora.io/) - 实时音视频
   - [Deepgram](https://deepgram.com/) - 语音识别（支持中文）
   - **国产大模型之一**（见上表，推荐 DeepSeek）
   - [ElevenLabs](https://elevenlabs.io/) - 语音合成

### 安装步骤

1. **克隆仓库**
   ```bash
   cd ten-framework/ai_agents/agents/examples/ai-court-debate
   ```

2. **配置环境变量**
   复制 `.env.example` 为 `.env` 并填入 API 密钥：
   ```bash
   cp .env.example .env
   ```

   根据想用的国产大模型，至少填写对应的 API Key：
   ```bash
   # Agora 配置（必填）
   AGORA_APP_ID=your_agora_app_id
   AGORA_APP_CERTIFICATE=your_agora_certificate

   # Deepgram ASR（必填，支持中文）
   DEEPGRAM_API_KEY=your_deepgram_api_key

   # 选一个国产大模型（必填其一）
   DEEPSEEK_API_KEY=sk-xxxx          # DeepSeek（推荐）
   # DASHSCOPE_API_KEY=sk-xxxx       # 通义千问
   # MOONSHOT_API_KEY=sk-xxxx        # Kimi
   # ZHIPU_API_KEY=xxxx.xxxx         # 智谱GLM
   # DOUBAO_API_KEY=xxxx             # 字节豆包

   # ElevenLabs TTS（必填）
   ELEVENLABS_TTS_KEY=your_elevenlabs_api_key
   ```

3. **安装依赖**
   ```bash
   cd tenapp

   # 安装 TEN 依赖
   tman install
   ```

4. **构建项目**
   ```bash
   # 使用 Task 构建
   task build

   # 或手动构建
   go build -o bin/app main.go
   ```

5. **启动服务**（选择国产大模型）
   ```bash
   # 使用 DeepSeek（默认，推荐）
   ./bin/app
   # 等价于加载 ai_court_debate_deepseek 图

   # 使用通义千问
   ./bin/app -graph ai_court_debate_qwen

   # 使用 Kimi
   ./bin/app -graph ai_court_debate_kimi

   # 使用智谱 GLM
   ./bin/app -graph ai_court_debate_glm

   # 使用字节豆包
   ./bin/app -graph ai_court_debate_doubao
   ```

## 💼 使用指南

### 基础使用

1. **启动服务后**，系统会输出：
   ```
   AI Court Debate Agent Starting...
   法庭AI辩护助手已就绪（DeepSeek驱动）
   ```

2. **连接到频道**
   - 使用 Agora SDK 客户端连接到频道 `court_debate_channel`
   - 系统会播放欢迎语（含当前使用的模型名）

3. **开始对话**
   - 通过麦克风说话，系统会实时识别（中文优先）
   - AI 会基于法律知识和案情分析生成答辩意见
   - 答辩意见会通过语音输出

### 高级配置

#### 1. 自定义案件信息

编辑 `tenapp/property.json` 中的 `case_analyzer` 配置：

```json
{
  "type": "extension",
  "name": "case_analyzer",
  "property": {
    "case_info": {
      "case_number": "（2024）京0105刑初123号",
      "case_type": "criminal",
      "role": "defendant",
      "description": "盗窃案辩护",
      "facts": [
        "被告人于2024年1月在某商场涉嫌盗窃",
        "涉案金额约5000元人民币"
      ],
      "evidence": [
        "监控录像",
        "被害人陈述",
        "物证清单"
      ],
      "defendant_statement": "当事人否认盗窃行为，称是误拿",
      "prosecution_claims": [
        "指控被告人构成盗窃罪",
        "建议判处有期徒刑三年"
      ]
    }
  }
}
```

#### 2. 扩展法律知识库

编辑 `tenapp/ten_packages/extension/legal_knowledge_python/property.json`：

```json
{
  "legal_database": {
    "criminal_law": {
      "robbery": {
        "article": "第263条",
        "content": "以暴力、胁迫或者其他方法抢劫公私财物的，处三年以上十年以下有期徒刑，并处罚金。",
        "keywords": ["抢劫", "暴力", "胁迫", "财物"]
      }
    }
  }
}
```

#### 3. 调整 LLM 提示词

修改 `tenapp/property.json` 中的 `llm.property.prompt` 来自定义 AI 的行为方式。

### 工具调用示例

AI 助手可以调用以下工具：

1. **search_legal_knowledge** - 搜索法律条文
   ```json
   {
     "query": "盗窃",
     "category": "criminal_law"
   }
   ```

2. **analyze_case** - 分析案情
   ```json
   {
     "aspect": "strategy"  // overview | evidence | strategy | counterarguments
   }
   ```

## 📝 使用场景

### 场景 1：刑事案件辩护

**案例**：盗窃案辩护

**对话示例**：
```
法官：被告人，你对公诉机关指控你犯盗窃罪有何辩解？

AI助手：尊敬的审判长，针对公诉机关的指控，辩护人认为：

第一，关于犯罪主观方面。根据刑法第264条，盗窃罪的成立需要具备非法占有的主观故意。
本案中，当事人始终坚称是误拿商品，并无盗窃的主观故意。

第二，关于证据的充分性。根据刑事诉讼法的规定，定罪需要达到"证据确实、充分"的证明标准。
现有证据尚不能排除合理怀疑，根据疑罪从无原则，应当作出有利于被告人的认定。

第三，即使认定构成盗窃，本案涉案金额仅5000元，属于"数额较大"的情形，
依据刑法第264条，应处三年以下有期徒刑、拘役或者管制，建议从轻处罚。

综上，请求法庭依法作出公正判决。
```

### 场景 2：民事纠纷答辩

**案例**：合同纠纷

**对话示例**：
```
法官：被告对原告的诉讼请求有何答辩意见？

AI助手：尊敬的审判长，针对原告的诉讼请求，被告答辩如下：

第一，关于合同效力。根据民法典第509条，当事人应当按照约定全面履行自己的义务。
本案中，被告已按照合同约定履行了主要义务，原告主张被告违约缺乏事实依据。

第二，关于违约责任。即使存在部分履行瑕疵，也应根据民法典相关规定，
按照实际损失确定赔偿金额，原告主张的赔偿数额明显过高，缺乏合理依据。

第三，关于诉讼时效。本案争议发生于2年前，根据民法典第188条的规定，
部分诉讼请求可能已超过诉讼时效，依法不应得到支持。

综上，请求法庭驳回原告的诉讼请求。
```

## 🛠️ 开发指南

### 目录结构

```
ai-court-debate/
├── tenapp/                          # TEN 应用主目录
│   ├── main.go                      # Go 启动入口
│   ├── manifest.json                # 应用清单
│   ├── property.json                # 应用配置（图结构）
│   ├── scripts/
│   │   └── start.sh                 # 启动脚本
│   └── ten_packages/
│       └── extension/               # 扩展目录
│           ├── court_debate_control_python/  # 主控制扩展
│           │   ├── manifest.json
│           │   ├── property.json
│           │   ├── addon.py
│           │   ├── extension.py
│           │   ├── config.py
│           │   └── helper.py
│           ├── legal_knowledge_python/       # 法律知识库扩展
│           │   ├── manifest.json
│           │   ├── property.json
│           │   ├── addon.py
│           │   └── extension.py
│           └── case_analyzer_python/         # 案情分析扩展
│               ├── manifest.json
│               ├── property.json
│               ├── addon.py
│               └── extension.py
├── README.md                        # 本文档
└── Dockerfile                       # Docker 部署文件
```

### 添加新的法律知识

1. 编辑 `legal_knowledge_python/property.json`
2. 在 `legal_database` 中添加新的法律类别或条文
3. 重启服务使配置生效

### 自定义扩展

参考 `court_debate_control_python` 创建新的扩展：

```python
from ten_runtime import AsyncExtension, AsyncTenEnv

class MyExtension(AsyncExtension):
    async def on_init(self, ten_env: AsyncTenEnv):
        # 初始化逻辑
        pass

    async def on_cmd(self, ten_env: AsyncTenEnv, cmd: Cmd):
        # 处理命令
        pass
```

## 🔧 故障排除

### 常见问题

1. **服务启动失败**
   - 检查所有 API Keys 是否正确配置
   - 确认网络连接正常
   - 查看日志文件排查错误

2. **语音识别不准确**
   - 检查麦克风权限
   - 调整 Deepgram 的 `language` 参数（zh-CN / en-US）
   - 确保网络延迟较低

3. **AI 回答不专业**
   - 完善 `case_info` 中的案件信息
   - 扩充法律知识库内容
   - 优化 LLM 的 system prompt

### 日志查看

```bash
# 查看运行日志
tail -f logs/app.log

# 调试模式启动
LOG_LEVEL=debug ./bin/app
```

## 📄 许可证

本项目基于 TEN Framework 构建，遵循 Apache License 2.0。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，请通过以下方式联系：
- GitHub Issues
- TEN Framework 社区

---

<a name="english"></a>

## 📖 Introduction (English)

**AI Court Debate Agent** is an intelligent legal defense assistant system built on the TEN Framework. It integrates speech recognition, large language models, legal knowledge base, and case analysis capabilities for real-time court debate and defense.

### 🎯 Key Features

1. **Real-time Voice Interaction**
   - 🎤 ASR: Real-time recognition of judge/opposing counsel questions
   - 🔊 TTS: Convert defense arguments to natural speech output

2. **Legal Knowledge Base**
   - 📚 Built-in Chinese Criminal Law, Civil Code provisions
   - 🔍 Intelligent retrieval of relevant legal regulations
   - 📑 Search by category and keywords

3. **Case Analysis Engine**
   - 📊 Analyze case facts and evidence
   - 🎯 Generate debate strategies and key points
   - 🛡️ Based on legal principles like presumption of innocence

4. **Intelligent Defense Generation**
   - 🤖 Generate professional defense opinions using OpenAI GPT
   - 📝 Automatically cite relevant legal provisions
   - 💡 Provide well-reasoned legal viewpoints

### Quick Start

Please refer to the Chinese documentation above for detailed setup and usage instructions.

---

## 🌟 特性亮点

- ✅ **实时交互**：毫秒级语音识别和响应
- ✅ **专业性强**：基于真实法律条文和原则
- ✅ **可扩展**：模块化设计，易于添加新功能
- ✅ **多场景**：支持刑事、民事等多种案件类型
- ✅ **开源免费**：基于 Apache 2.0 协议

## 🎓 技术特点

- 采用 TEN Framework 的图结构设计
- 多语言支持（Go + Python）
- 异步处理提升性能
- 工具调用机制（Function Calling）
- 流式语音输出

---

**Built with ❤️ using TEN Framework**
