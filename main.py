import os
from dotenv import load_dotenv
from notionCli import NotionFetcher
from trans import Parser

# .envファイルからAPIキーを読み込む
load_dotenv()
NotionAPIKey = os.getenv("NotionAPIKey")

def main():
    # ここにNotionページのIDを貼り付け
    PAGE_ID = "380e3a3403dd809fa664fa68db8d9a8b" 

    # 1. Fetch層：データの取得
    print("Notionからデータを取得しています...")
    fetcher = NotionFetcher(NotionAPIKey)
    rawBlocks = fetcher.getBlocks(PAGE_ID)

    # 2. Transform層：データの解析と変換
    print("データを解析しています...")
    parser = Parser()
    parsedBlocks = parser.parseBlocks(rawBlocks)

    # 結果を表示
    print("\n解析完了！抽出されたデータは以下の通りです：\n")
    for item in parsedBlocks:
        if item["type"] == "image":
            # 画像ブロックの場合は url を表示
            print(f"[{item['type']}]\n{item['url']}")
        else:
            # それ以外のテキストブロックの場合は text を表示
            print(f"[{item['type']}]\n{item['text']}")

if __name__ == "__main__":
    main()