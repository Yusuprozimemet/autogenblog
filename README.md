# AutoGenBlog - AI Chat Assistant 🤖

A sophisticated AI-powered chat application built with Streamlit that features multi-agent workflows, financial analysis capabilities, and intelligent conversation management.

## 🌟 Features

- **Multi-Chat Interface**: Manage multiple conversation threads with history
- **AI-Powered Responses**: Uses OpenAI's GPT-4o-mini for intelligent conversations
- **User Profiles**: Customizable user preferences and chat styles
- **Financial Analysis**: Stock analysis and reporting with AutoGen agents
- **Real-time Visualization**: Interactive charts and financial metrics
- **Responsive Design**: Modern UI with custom styling

## 🏗️ Architecture

- **Frontend**: Streamlit web framework
- **AI Engine**: OpenAI API with AutoGen multi-agent system
 **AI Engine**: OpenAI API with AutoGen multi-agent system (using `autogen-agentchat` and `autogen-ext[openai,azure]`)
- **Data Sources**: Yahoo Finance for stock data
- **Visualization**: Matplotlib for charts and graphs

## 🚀 Railway Deployment

### Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com)
3. **Git Repository**: Your code in a Git repository

### Deployment Steps

#### Option 1: Deploy from GitHub

1. **Connect Repository**:
   - Go to Railway dashboard
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Set Environment Variables**:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Deploy**:
   - Railway will automatically detect the Dockerfile
   - Build and deploy process starts automatically
   - Your app will be live at the provided Railway URL

#### Option 2: Deploy via Railway CLI

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Deploy**:
   ```bash
   railway login
   railway link
   railway up
   ```

3. **Set Environment Variables**:
   ```bash
   railway variables set OPENAI_API_KEY=your_openai_api_key_here
   ```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | ✅ Yes |
| `PORT` | Port number (automatically set by Railway) | ✅ Auto |

## 🛠️ Local Development

### Setup

1. **Clone Repository**:
   ```bash
   git clone <your-repo-url>
   cd autogenblog
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   # For agent functionality, also install:
   pip install autogen-agentchat autogen-ext[openai,azure]
   ```

4. **Set Environment Variables**:
   Create a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run Application**:
   ```bash
   streamlit run Homepage.py
   ```

### Development with Docker

1. **Build Image**:
   ```bash
   docker build -t autogenblog .
   ```

2. **Run Container**:
   ```bash
   docker run -p 8080:8080 -e OPENAI_API_KEY=your_key_here autogenblog
   ```

## 📁 Project Structure

```
autogenblog/
├── Homepage.py              # Main Streamlit app
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── railway.json            # Railway deployment config
├── .dockerignore           # Docker ignore file
├── pages/
│   └── 01_User_Profile.py  # User profile page
├── functions/
│   └── utils.py            # Utility functions
├── styles/
│   └── main.py             # CSS styling
├── coding/
│   ├── stock_analysis.py   # Stock analysis logic
│   └── scrape_news_headlines.py
└── financial_report.py     # AutoGen financial reports
├── rna_research_report.py  # RNA research report (requires agent packages)
```

## 🔧 Configuration

### Streamlit Configuration

The app is configured to run on Railway with:
- Port: 8080 (Railway standard)
- Headless mode enabled
- File watcher disabled for production
- Health check endpoint at `/_stcore/health`

### Docker Optimization

- Multi-stage build for smaller images
- Non-root user for security
- Layer caching for faster builds
- Health checks for reliability

## 🚨 Security Notes

- ✅ API keys are stored as environment variables
- ✅ Non-root Docker user
- ✅ No sensitive data in version control
- ⚠️ Ensure your OpenAI API key has appropriate usage limits

## 🐛 Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check Dockerfile syntax
   - Verify all dependencies in requirements.txt

2. **Runtime Errors**:
   - Ensure OPENAI_API_KEY is set correctly
   - Check Railway logs for detailed error messages
   - If you see `ModuleNotFoundError: No module named 'autogen'`, make sure you installed `autogen-agentchat` and `autogen-ext[openai,azure]`.

3. **Performance Issues**:
   - Monitor Railway resource usage
   - Consider upgrading Railway plan for better performance

### Getting Help

- Check Railway deployment logs
- Verify environment variables are set
- Ensure your OpenAI API key is valid and has credits

## 📄 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines here]