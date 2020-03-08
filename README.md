# KudoLog

## Overview

KudoLogは登録ユーザーが記事投稿、コメントができる掲示板アプリです。

## 使用した技術

### backend

- Django (web framework)
- Docker (環境構築)
- Heroku (インフラ)
- Postgresql (開発・運用用DB)
- AWS S3 (メディアストレージ)

### frontend

- bootstrap
- google font
- font awesome

## Function

### ユーザー管理

- 管理ユーザー登録機能(username, email, password)
- ログイン/ログアウト機能
- プロフィール作成機能
- 画像アップロード機能(アイコン)

### 記事(登録ユーザーのみ)

- 記事投稿機能(ドラック&ドロップで画像投稿可)
- 下書作成機能
- 記事編集・削除機能
- 記事検索機能
- 記事ごとのコメント機能
- ページネーション機能
