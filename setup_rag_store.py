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
# 既存のストアを使用する
# -----------------------------
store_name = "fileSearchStores/gas-documentation-rag-store-ftwf69nijziu"
print("📁 既存ストアにアップロードします")
print("  - store_name =", store_name)

# -----------------------------
# ファイルアップロード
# -----------------------------
for doc_directory in doc_dirs:
    print(f"\n📂 ディレクトリ '{doc_directory}' の処理開始...")

    for filename in os.listdir(doc_directory):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(doc_directory, filename)
        print(f"  - アップロード中: {filename}")

        op = client.file_search_stores.upload_to_file_search_store(
            file_search_store_name=store_name,
            file=file_path,
            display_name=filename,
        )

        while True:
            current = client.operations.get(name=op.name)
            if current.done:
                break
            print("    - 処理中...")
            time.sleep(2)

print("\n✅ すべてのファイルを既存ストアにアップロードしました")



