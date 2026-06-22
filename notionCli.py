from notion_client import Client
from notion_client.errors import APIResponseError

class NotionFetcher:
    def __init__(self, api_key: str):
        """
        Notion APIクライアントの初期化
        """
        if not api_key:
            raise ValueError("NotionAPIKeyが設定されていません\n.envファイルを確認してください")

        self.client = Client(auth = api_key)

    def get_blocks(self, blockId: str) -> list:
        """
        指定されたブロックの子ブロックの全取得
        """
        try:
            blocks = self._fetch_blocks(blockId)
            return blocks
        except APIResponseError as e:
            raise APIResponseError(f"ブロック取得失敗（ID: {blockId}）: {e}")
    
    def _fetch_blocks(self, blockId: str) -> list:
        """
        ページネーションを考慮しながらブロックを取得し、
        子ブロックがあれば再帰的に取得する
        """
        blocks = []
        cursor = None

        while True:
            response = self.client.blocks.children.list(
                block_id = blockId,
                start_cursor = cursor
            )

            for block in response.get("results", []):
                if block.get("has_children"):
                    block["_children"] = self._fetch_blocks(block["id"])
                blocks.append(block)
            
            if response.get("has_more"):
                cursor = response.get("next_cursor")
            else:
                break
        
        return blocks