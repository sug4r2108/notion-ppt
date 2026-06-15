import os
import argparse
from dotenv import load_dotenv
from notionCli import NotionFetcher
from trans import Parser
from builder import Builder

# .envファイルからAPIキーを読み込み
load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")

def main():
    parser = argparse.ArgumentParser(description="NotionからPowerPointを生成します")
    parser.add_argument("page_id", help="スライド化したいNotionページのID")
    args = parser.parse_args()

    # データの取得
    fetcher = NotionFetcher(NOTION_API_KEY)
    raw_blocks = fetcher.get_blocks(args.page_id)

    # データの解析と変換
    parser = Parser()
    slide_data = parser.parse_blocks(raw_blocks)

    # パワポの生成
    builder = Builder("assets/template.pptx")
    output_path = f"output_{args.page_id}.pptx"
    builder.create_presentation(slide_data, output_path)

    print(f"生成完了: {output_path}")

if __name__ == "__main__":
    main()