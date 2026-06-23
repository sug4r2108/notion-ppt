"""
parser.py
Notionの生のブロックデータを、builder.pyが扱いやすい階層構造に変換。

出力データ構造:
{
    "title": "ページタイトル（仮: page_id）",
    "sections": [
        {
            "heading1": "大題目",
            "subsections": [
                {
                    "heading2": "小題目",
                    "content": [
                        {
                            "heading3": "小セクション",
                            "body": ["文章1", "文章2"]
                        },
                    ]
                },
            ]
        },
    ]
}
"""


class BlockParser:
    def __init__(self):
        pass

    def parse_blocks(self, page_id: str, raw_blocks: list) -> dict:
        """
        Notionの生ブロックリストを階層構造の辞書に変換
        """
        result = {
            "title": page_id,  # 仮実装：page_idをタイトルとして使用
            "sections": []
        }

        current_section    = None  # 現在の大題目（heading1）
        current_subsection = None  # 現在の小題目（heading2）
        current_content    = None  # 現在の小セクション（heading3）

        for block in raw_blocks:
            block_type = block.get("type")
            if not block_type:
                continue

            text = self._extract_text(block)

            # heading1 → 新しい大題目を開始
            if block_type == "heading_1":
                if not text:
                    continue
                current_section = {
                    "heading1": text,
                    "subsections": []
                }
                current_subsection = None
                current_content    = None
                result["sections"].append(current_section)

            # heading2 → 新しい小題目を開始
            elif block_type == "heading_2":
                if not text:
                    continue
                
                if current_section is None:
                    current_section = {
                        "heading1": "",
                        "subsections": []
                    }
                    result["sections"].append(current_section)

                current_subsection = {
                    "heading2": text,
                    "content": []
                }
                current_content = None
                current_section["subsections"].append(current_subsection)

            # heading3 → 新しい小セクションを開始
            elif block_type == "heading_3":
                if not text:
                    continue
                
                if current_subsection is None:
                    continue

                current_content = {
                    "heading3": text,
                    "body": []
                }
                current_subsection["content"].append(current_content)

            # paragraph / bulleted_list_item / numbered_list_item → 本文
            elif block_type in ["paragraph", "bulleted_list_item", "numbered_list_item"]:
                if not text:
                    continue
                
                if current_content is None:
                    if current_subsection is None:
                        continue
                    current_content = {
                        "heading3": "",
                        "body": []
                    }
                    current_subsection["content"].append(current_content)

                current_content["body"].append(text)

            
            elif block_type == "image":
                image_url = self._extract_image_url(block)
                if not image_url:
                    continue
                if current_content is None:
                    if current_subsection is None:
                        continue
                    current_content = {
                        "heading3": "",
                        "body": []
                    }
                    current_subsection["content"].append(current_content)

                current_content["body"].append({
                    "type": "image",
                    "url": image_url
                })

        return result

    def _extract_text(self, block: dict) -> str:
        """
        ブロックからプレーンテキストを抽出する
        """
        block_type = block.get("type")
        if not block_type:
            return ""

        block_contents = block.get(block_type, {})
        text_array = block_contents.get("rich_text", [])

        return "".join(rt.get("plain_text", "") for rt in text_array)

    def _extract_image_url(self, block: dict) -> str:
        """
        画像ブロックからURLを抽出する
        """
        block_contents = block.get("image", {})
        image_type = block_contents.get("type")
        if not image_type:
            return ""

        return block_contents.get(image_type, {}).get("url", "")