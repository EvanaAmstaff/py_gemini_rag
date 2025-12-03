import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("APIキーが.envにありません")

client = genai.Client(api_key=api_key)

# ✅ 今回あなたが作成した「唯一有効なストア」
FILE_SEARCH_STORE_NAME = "fileSearchStores/rvoklhg8fcem-bzuaggmyfr14"

doc_dirs = ["gas_docs_txt", "gemini_api_docs_txt"]

print("✅ 使用ストア:", FILE_SEARCH_STORE_NAME)

# -----------------------------
# ファイルアップロード
# -----------------------------
for doc_directory in doc_dirs:
    print(f"\n📂 ディレクトリ '{doc_directory}' の処理開始...")

    if not os.path.isdir(doc_directory):
        print("⚠ ディレクトリが存在しません:", doc_directory)
        continue

    for filename in os.listdir(doc_directory):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(doc_directory, filename)
        print(f"  - アップロード中: {filename}")

        # ✅ SDK完全互換形（dict禁止・keyword完全一致）
        op = client.file_search_stores.upload_to_file_search_store(
           file_search_store_name=FILE_SEARCH_STORE_NAME,
           file=file_path,
        )












