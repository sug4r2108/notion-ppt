from notion_client import Client
from notion_client.errors import APIResponseError

class NotionFetcher:
    def __init__(self, apiKey: str):
        """
        Notion APIクライアントの初期化
        """
        self.client = Client(auth = apiKey)

    def get_blocks(self, blockId: str) -> list:
        """
        指定されたブロックの子ブロックの全取得
        """
        try:
            blocks = []
            cursor = None

            while True:
                # APIによりブロックを取得
                response = self.client.blocks.children.list(
                    block_id = blockId,
                    start_cursor = cursor
                )

                # 取得したブロックのリストを配列に追加
                blocks.extend(response.get("results", []))

                # 続きがある場合は続けて取得
                if response.get("has_more"):
                    cursor = response.get("next_cursor")
                else:
                    break

            return blocks
        except APIResponseError as e:
            raise APIResponseError(f"ブロック取得失敗（ID: {blockId}）: {e}")