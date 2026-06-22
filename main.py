import os
from datetime import datetime
from dotenv import load_dotenv
import argparse
from notionCli import NotionFetcher
from notion_client.errors import APIResponseError
from parser import BlockParser
from builder import PptxBuilder

# 環境情報の取得
load_dotenv()
NotionAPIKey = os.getenv("NotionAPIKey")

# CLI引数化
def setup_args():
    parser = argparse.ArgumentParser(
        description = "NotionページからPowerPointを生成するCLIツール"
    )

    parser.add_argument(
        "page_id",
        help = "変換したいNotionページ"
    )

    parser.add_argument(
        "-o", "--output",
        default = None,
        help = "出力ファイルパス（省略時は output/slide_YYYYMMDD.pptx）"
    )

    return parser.parse_args()

def main():
    args = setup_args()

    # 出力先の決定
    OUTPUT_DIR = "output"
    if args.output:
        OUTPUT_FILE = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d")
        OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"slide_{timestamp}.pptx")
    
    # output/ ディレクトリの自動生成
    os.makedirs(os.path.dirname(OUTPUT_FILE) or OUTPUT_DIR, exist_ok = True)

    
    # 1. Fetch層：データの取得
    print("Notionからデータを取得しています...")
    try:
        fetcher = NotionFetcher(NotionAPIKey)
        raw_blocks = fetcher.get_blocks(args.page_id)
    except APIResponseError as e:
        print(f"Notion APIエラー: {e}")
        print("ページIDやAPIキーを確認してください")
        return
    except Exception as e:
        print(f"データ取得中に予期せぬエラー: {e}")
        return

    # 2. Transform層：データの解析と変換
    print("データを解析しています...")
    try:
        parser = BlockParser()
        parsed_blocks = parser.parse_blocks(raw_blocks)
    except Exception as e:
        print(f"データ解析中に予期せぬエラー: {e}")

    # 3. Generate層：PowerPointの生成
    print("PowerPointスライドを作成しています...")
    builder = PptxBuilder() # 今回はデフォルトの白紙テンプレートを使用
    builder.build(parsed_blocks, OUTPUT_FILE)

    print(f"\n成功! {OUTPUT_FILE} が作成されました！")


if __name__ == "__main__":
    main()