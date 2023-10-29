# ChatGPT Discord Bot
# RESister

Team Name: Japan Vietnam friends - JVf

Name of the product/ application/ POC /demo: RESister (Residency Sister)

Short description of the product/ application/ POC /demo (maximum: 400-500 words):
Our intelligent chatbot delivers next-gen support for residency administration offices by automating responses to common questions from residents and staff.

Powered by a cutting-edge large language model, this virtual assistant understands free-form questions in natural language when asked via chat or voice interface. It then provides accurate answers instantly on topics like scheduling, evaluations, paperwork, policies and more.

For example, residents can ask:

When is my next rotation schedule?
Have my vacation days for this month been approved?
What forms do I need to submit for an upcoming conference?
The chatbot scans the question, extracts key details, and leverages its advanced reasoning capabilities to formulate a helpful response on the fly.

If it lacks the confidence to answer a question fully, it will suggest helpful resources and seamlessly escalate the inquiry to a human agent.

Key benefits:

24/7 automated assistance - Quick answers for residents anytime
Increased admin productivity - Bot handles common inquiries
Reduced admin workload - Staff freed from repetitive questions
Intuitive conversational interface - Easy question and answer interactions
Seamless human escalation - Complex questions efficiently handed over

With the ability to understand free-form language, access key residency information, and learn from human agents, our AI chatbot streamlines support services for program administrators.

By providing fast, accurate self-service options to residents for program questions, it acts as a virtual resident services coordinator 24/7. This enables human staff to focus their time on higher-value tasks.

The bot delivers the right answers to the right user at the right time - transforming how residency offices provide scalable, hassle-free support.



# Setup

## Critical prerequisites to install

* run ```pip3 install -r requirements.txt```

* **Rename the file `.env.example` to `.env`**

* Recommended python version `3.9` +
---
## Create a Discord bot

1. Go to https://discord.com/developers/applications create an application
2. Build a Discord bot under the application
3. Get the token from bot setting

4. Store the token to `.env` under the `DISCORD_BOT_TOKEN`





---
> **Note**
>
> In Step 2, you only need to complete the authentication process for the model you want to use (it's not necessary to complete all Step 2)
>
> Remember to modify `CHAT_MODEL` to the default model you want to use in `.env` file

## Official API authentication

### Geanerate an OpenAI API key
1. Go to https://beta.openai.com/account/api-keys

2. Click Create new secret key


3. Store the SECRET KEY to `.env` under the `OPENAI_API_KEY`

---
## Website ChatGPT authentication

> **Only Support ChatGPT Plus Account**

1. Open https://chat.openai.com/api/auth/session

2. Open console with `F12`



3. Copy the value for `_puid` from cookies and paste it into `.env` under `PUID`

4. Copy the value for `accessToken` from cookies and paste it into `.env` under `ACCESS_TOKEN`



---

---
## Run the bot on the desktop

1. Open a terminal or command prompt

2. Navigate to the directory where you installed the ChatGPT Discord bot

3. Run `python3 main.py` or `python main.py` to start the bot
---
## Run the bot with Docker

1. Build the Docker image & Run the Docker container `docker compose up -d`

2. Inspect whether the bot works well `docker logs -t chatgpt-discord-bot`

   ### Stop the bot:

   * `docker ps` to see the list of running services
   * `docker stop <BOT CONTAINER ID>` to stop the running bot


## Commands

* `/chat [message]` Chat with ChatGPT!






