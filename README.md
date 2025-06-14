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
gcloud config set project PROJECT_ID
gcloud auth application-default login
```

Setup environment variables.

```bash
export GOOGLE_CLOUD_PROJECT=`gcloud config list --format 'value(core.project)'`
export GOOGLE_CLOUD_LOCATION=us-central1
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
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

## Google Cloud

```bash
export GOOGLE_CLOUD_PROJECT=`gcloud config list --format 'value(core.project)'` && echo $GOOGLE_CLOUD_PROJECT
export image_name=adk-linebot

gcloud auth configure-docker asia-northeast1-docker.pkg.dev
gcloud artifacts repositories create $image_name --location=asia-northeast1 --repository-format=docker --project=$GOOGLE_CLOUD_PROJECT

docker rmi asia-northeast1-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/$image_name/$image_name && docker rmi $image_name
cd src
docker build . -t $image_name --platform linux/amd64
docker tag $image_name asia-northeast1-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/$image_name/$image_name && docker push asia-northeast1-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/$image_name/$image_name:latest
```

```bash
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

CHANNEL_SECRETとCHANNEL_ACCESS_TOKENの環境変数をSecret Managerに登録する。

```bash
gcloud secrets create LINE_CHANNEL_SECRET \
    --replication-policy="automatic"
```

```bash
echo -n "" | gcloud secrets versions add LINE_CHANNEL_SECRET --data-file=-
```

```bash
gcloud secrets create LINE_CHANNEL_ACCESS_TOKEN \
    --replication-policy="automatic"
```

```bash
echo -n "" | gcloud secrets versions add LINE_CHANNEL_ACCESS_TOKEN --data-file=-
```

## Cloud Runのデプロイ

todo: サービスアカウントの作成を書く。[参考](https://zenn.dev/ymd65536/articles/recently_read_books_bot_gemini15#cloudrun%E3%81%A7docker%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%82%92%E3%83%87%E3%83%97%E3%83%AD%E3%82%A4)
