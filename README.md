# ADKを使ってLINE botを動かす

## Overview

Agent Development Kit（ADK）を使ったLINE botを開発する。

考えていることは以下のとおりです。

- adkのターミナル機能でデバッグができる
- adkによるエージェントの作り方がわかる
- 実際に動く最小限のものがすぐに確認できる

作成するエージェントは誰でも手軽に実行できるものがいい。
RAGを使うとかそういう大掛かりなものではなくもっとシンプルなものが良い。

シンプルなものの第一条件として`エージェントが動作するためのコンポーネントが必要最小限であること`と
必要とあれば、コンポーネントをはずすことができる。（オプションとして実装されていてなくても動く）みたいなものが良い。

## Setup

```bash
curl -sSL https://sdk.cloud.google.com | bash && exec -l $SHELL && gcloud init
```

setup gcloud.

```bash
gcloud auth login
gcloud auth application-default login
```

Setup environment variables.

```bash
export GOOGLE_CLOUD_PROJECT=`gcloud config list --format 'value(core.project)'`
export GOOGLE_CLOUD_LOCATION=us-central1
```

Setup `.env` file.

```bash
echo "GOOGLE_GENAI_USE_VERTEXAI=TRUE" > ./multi_tool_agent/.env
echo "GOOGLE_CLOUD_LOCATION=us-central1" >> ./multi_tool_agent/.env
echo "GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT" >> ./multi_tool_agent/.env
```

```bash
pip install google-adk
```

## Run

Run the agent.

```bash
cd src/agents
adk web
```
