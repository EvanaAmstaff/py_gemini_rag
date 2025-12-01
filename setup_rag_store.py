# setup_rag_store.py（完全修正版）

import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("APIキーが.envファイルにありません")

client = genai.Client(api_key=api_key)
doc_dirs = ["gas_docs_txt", "gemini_api_docs_txt"]

# -----------------------------
# 1. File Search Store の作成
# -----------------------------
print("📁 ファイル検索ストアを作成しています...")
store = client.file_search_stores.create(
    config={"display_name": "GAS Documentation RAG Store (new SDK)"}
)

# store.name = "projects/xxx/locations/global/fileSearchStores/abcd1234"
store_id = store.name.split("/")[-1]
print("  - store_id =", store_id)

# -----------------------------
# 2. アップロード
# -----------------------------
for doc_directory in doc_dirs:
    print(f"\n📂 ディレクトリ '{doc_directory}' の処理開始...")

    for filename in os.listdir(doc_directory):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(doc_directory, filename)
        print(f"  - アップロード中: {filename}")

        # --- 正しい upload 呼び出し形式 ---
        op = client.file_search_stores.upload_to_file_search_store(
            file_search_store_id=store_id,
            display_name=filename,
            file={
                "path": file_path,
                "mime_type": "text/plain",
            },
        )

        # --- operation.name を使って進行監視 ---
        while True:
            current = client.operations.get(name=op.name)
            if current.done:
                break
            print("    - 処理中...")
            time.sleep(4)

print("\n✅ すべてのファイルをアップロードしました")

# -----------------------------
# 3. store_id をファイルに保存
# -----------------------------
with open("setup_rag_store_file_search_store_name.txt", "w", encoding="utf-8") as f:
    f.write(store_id)

print("\n🎉 RAGの準備が完了しました")
print("ストアID:", store_id)
