import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("APIキーが.envファイルにありません")

client = genai.Client(api_key=api_key)

# すでに存在する正しい store_id（あなたの環境で確認済み）
STORE_ID = "gas-documentation-rag-store-ftwf69nijziu"

# アップロードするフォルダ
doc_dirs = ["gas_docs_txt", "gemini_api_docs_txt"]

print("📁 既存の File Search Store を使用します:")
print("  - store_id =", STORE_ID)

# ----------------------------------------------------
# 1. アップロード
# ----------------------------------------------------
for doc_directory in doc_dirs:
    print(f"\n📂 ディレクトリ '{doc_directory}' の処理開始...")

    for filename in os.listdir(doc_directory):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(doc_directory, filename)
        print(f"  - アップロード中: {filename}")

        # 新SDKの正しい upload 呼び出し（display_name は存在しない）
        op = client.file_search_stores.upload_to_file_search_store(
            file_search_store_id=STORE_ID,
            file={
                "path": file_path,
                "mime_type": "text/plain",
            },
        )

        # アップロードの Operation 完了待ち
        while True:
            current = client.operations.get(name=op.name)
            if current.done:
                break
            print("    - 処理中...")
            time.sleep(3)

print("\n✅ すべてのファイルを正常にアップロードしました")

# ----------------------------------------------------
# 2. store_id をファイル保存
# ----------------------------------------------------
with open("setup_rag_store_file_search_store_name.txt", "w", encoding="utf-8") as f:
    f.write(STORE_ID)

print("\n🎉 RAGの準備が完了しました")
print("ストアID:", STORE_ID)





