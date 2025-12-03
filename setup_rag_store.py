import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("APIキーが.envファイルにありません")

client = genai.Client(api_key=api_key)

# ✅ あなたが実際に list で確認できた “存在する” ストア名
FILE_SEARCH_STORE_NAME = "fileSearchStores/gas-documentation-rag-store-ftwf69nijziu"

doc_dirs = ["gas_docs_txt", "gemini_api_docs_txt"]

print("📁 既存の File Search Store にアップロードします")
print("  - store_name =", FILE_SEARCH_STORE_NAME)

# -----------------------------
# アップロード
# -----------------------------
for doc_directory in doc_dirs:
    print(f"\n📂 ディレクトリ '{doc_directory}' の処理開始...")

    for filename in os.listdir(doc_directory):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(doc_directory, filename)
        print(f"  - アップロード中: {filename}")

        # ✅ あなたのSDKで唯一通る正しい呼び方
        op = client.file_search_stores.upload_to_file_search_store(
            file_search_store_name=FILE_SEARCH_STORE_NAME,
            file=file_path,
        )

        # 完了待ち
        while True:
           current = client.operations.get(op)   # ← 文字列ではなくオブジェクト
           if current.done:
               break
           print("    - 処理中...")
           time.sleep(2)



print("\n✅ すべてのファイルをアップロードしました")

# -----------------------------
# ストア名を保存
# -----------------------------
with open("setup_rag_store_file_search_store_name.txt", "w", encoding="utf-8") as f:
    f.write(FILE_SEARCH_STORE_NAME)

print("\n🎉 RAGの準備が完了しました")
print("File Search Store Name:", FILE_SEARCH_STORE_NAME)







