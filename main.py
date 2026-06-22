import os
from datetime import datetime
from dotenv import load_dotenv
from notionCli import NotionFetcher
from parser import BlockParser
from builder import PptxBuilder

load_dotenv()
NotionAPIKey = os.getenv("NotionAPIKey")

def main():
    # ご自身のページIDを設定してください
    PAGE_ID = "380e3a3403dd809fa664fa68db8d9a8b"

    now = datetime.now()
    timeStamp = now.strftime("%Y%m%d")

    # 出力先のフォルダ、ファイルの決定
    OUTPUT_DIR = "output"
    OUTPUT_FILENAME = f"VSeminer{timeStamp}.pptx"

    OUTPUT_FILE = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)

    try:
        # 1. Fetch層：データの取得
        print("Notionからデータを取得しています...")
        fetcher = NotionFetcher(NotionAPIKey)
        raw_blocks = fetcher.getBlocks(PAGE_ID)

        # 2. Transform層：データの解析と変換
        print("データを解析しています...")
        parser = BlockParser()
        parsedBlocks = parser.parseBlocks(raw_blocks)

        # 3. Generate層：PowerPointの生成
        print("PowerPointスライドを作成しています...")
        builder = PptxBuilder() # 今回はデフォルトの白紙テンプレートを使用
        builder.build(parsedBlocks, OUTPUT_FILE)

        print(f"\n成功! {OUTPUT_FILE} が作成されました！")

    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    main()