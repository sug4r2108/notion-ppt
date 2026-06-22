class BlockParser:
    def __init__(self):
        pass

    def parseBlocks(self, rawBlocks: list) -> list:
        """
        Notionの生のブロックデータから、
        パワポ生成に必要な情報（タイプとテキスト）だけを抽出
        """
        parsedData = []

        for block in rawBlocks:
            # ブロックの種類を取得
            blockType = block.get("type")
            if not blockType:
                continue

            # ブロックの種類に応じた中身のデータを取得
            blockContents = block.get(blockType, {})

            # 画像ブロックの特別処理
            if blockType == "image":
                imageType = blockContents.get("type") 
                if imageType:
                    imageURL = blockContents.get(imageType, {}).get("url")
                    if imageURL:
                        parsedData.append({
                            "type": "image",
                            "url": imageURL
                        })
                continue

            # テキストを抽出
            textArray = blockContents.get("rich_text", [])
            text = self._extractText(textArray)

            # テキストが空っぽのブロックはスキップ
            if not text.strip():
                continue

            # 辞書型にしてリストに追加
            parsedData.append({
                "type": blockType,
                "text": text
            })

        return parsedData

    def _extractText(self, textArray: list) -> str:
        """
        text配列の中から、装飾などを無視して純粋なテキストだけを繋ぎ合わせる
        """
        text = ""
        for rt in textArray:
            text += rt.get("plain_text", "")
        return text