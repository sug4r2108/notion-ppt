class BlockParser:
    def __init__(self):
        pass

    def parse_blocks(self, rawBlocks: list) -> list:
        """
        Notionの生のブロックデータから、
        パワポ生成に必要な情報（タイプとテキスト）だけを抽出
        """
        parsed_data = []

        for block in rawBlocks:
            # ブロックの種類を取得
            block_type = block.get("type")
            if not block_type:
                continue

            # ブロックの種類に応じた中身のデータを取得
            block_contents = block.get(block_type, {})

            # 画像ブロックの特別処理
            if block_type == "image":
                image_type = block_contents.get("type") 
                if image_type:
                    imageURL = block_contents.get(image_type, {}).get("url")
                    if imageURL:
                        parsed_data.append({
                            "type": "image",
                            "url": imageURL
                        })
                continue

            # テキストを抽出
            text_array = block_contents.get("rich_text", [])
            text = self._extract_text(text_array)

            # テキストが空っぽのブロックはスキップ
            if not text.strip():
                continue

            # 辞書型にしてリストに追加
            parsed_data.append({
                "type": block_type,
                "text": text
            })

        return parsed_data

    def _extract_text(self, text_array: list) -> str:
        """
        text配列の中から、装飾などを無視して純粋なテキストだけを繋ぎ合わせる
        """
        text = ""
        for rt in text_array:
            text += rt.get("plain_text", "")
        return text