#!/bin/bash

# 指定された日時文字列をJSTの文字列に変換する
# 使い方の例：
# convert_to_jst.sh "Tue, 28 Jan 2025 09:46:23 +0000 (UTC)"　→　2025-01-28 18:46:23
# convert_to_jst.sh "Tue, 28 Jan 2025 09:46:23 +0000"　      →　2025-01-28 18:46:23
# convert_to_jst.sh "Tue, 28 Jan 2025 09:46:23 +0900 (JST)"　→　2025-01-28 09:46:23
# convert_to_jst.sh "Tue, 28 Jan 2025 09:46:23 +0900"　      →　2025-01-28 09:46:23

convert_to_jst() {
  local date_str="$1"
  
  if [[ $date_str == *"+0000 (UTC)"* ]]; then
    date_str=${date_str// +0000 (UTC)/}
    date -d "$date_str UTC" "+%Y-%m-%d %H:%M:%S"
  elif [[ $date_str == *"+0000"* ]]; then
    date_str=${date_str// +0000/}
    date -d "$date_str UTC" "+%Y-%m-%d %H:%M:%S"
  elif [[ $date_str == *"+0900 (JST)"* ]]; then
    date_str=${date_str// +0900 (JST)/}
    date -d "$date_str JST" "+%Y-%m-%d %H:%M:%S"
  elif [[ $date_str == *"+0900"* ]]; then
    date_str=${date_str// +0900/}
    date -d "$date_str JST" "+%Y-%m-%d %H:%M:%S"
  else
    echo "Unsupported date format: $date_str"
  fi
}

# コマンドライン引数として与えられた日時文字列を処理
if [ -z "$1" ]; then
  echo "Usage: $0 '<datetime_string>'"
  exit 1
fi

convert_to_jst "$1"
