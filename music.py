import os
import time
import requests
from mutagen.flac import FLAC, Picture
from mutagen.id3 import PictureType

def fetch_album_art_from_itunes(album_name, artist_name=""):
    """
    iTunes API (Apple Music) を使って、アジア圏の楽曲でも確実に高画質ジャケットを検索
    """
    # 検索キーワードを設定
    query = f"{artist_name} {album_name}".strip()
    url = "https://itunes.apple.com/search"
    params = {
        "term": query,
        "media": "music",
        "entity": "album",
        "limit": 1
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                # 100x100のURLを1000x1000（高画質）に置き換える
                img_url = results[0].get("artworkUrl100", "")
                if img_url:
                    high_res_url = img_url.replace("100x100bb.jpg", "1000x1000bb.jpg")
                    return high_res_url
    except Exception:
        pass
    return None

def perfect_cover_embedder(music_dir):
    print("🎵 起動中: iTunes高精度画像埋め込みシステム (タグ絶対保護版) 🎵")
    print("-" * 60)
    
    success_count = 0
    fail_count = 0

    for root, dirs, files in os.walk(music_dir):
        for file in files:
            if file.lower().endswith('.flac'):
                flac_path = os.path.join(root, file)
                
                try:
                    # FLACファイルを読み込み
                    audio = FLAC(flac_path)
                    
                    # 既存のテキストタグ（タイトル、アルバム、アーティスト等）を完全に退避（保存）
                    # これにより、Windowsが一時的に見失ってもデータ自体は100%保護されます
                    saved_tags = {k: v for k, v in audio.items() if not k.startswith('__')}
                    
                    # アルバム名とアーティスト名を取得
                    albums = audio.get('album')
                    artists = audio.get('artist')
                    
                    if not albums:
                        print(f"⚠️ 跳过：[{file}] 缺失‘专辑’（アルバム）标签。")
                        continue
                        
                    album_name = albums[0].strip()
                    artist_name = artists[0].strip() if artists else ""
                    
                    print(f"🔍 正在检索 ➡️ 【{artist_name} - {album_name}】的封面...")
                    img_url = fetch_album_art_from_itunes(album_name, artist_name)
                    
                    if img_url:
                        img_resp = requests.get(img_url, timeout=15)
                        if img_resp.status_code == 200:
                            # 画像データを作成
                            picture = Picture()
                            picture.data = img_resp.content
                            picture.type = PictureType.COVER_FRONT
                            picture.mime = "image/jpeg"
                            picture.description = "Front Cover"
                            
                            # 画像を追加（既存の画像がある場合は上書き）
                            audio.clear_pictures()
                            audio.add_picture(picture)
                            
                            # 退避していた元のテキストタグを確実に再代入
                            for k, v in saved_tags.items():
                                audio[k] = v
                                
                            # 保存
                            audio.save()
                            print(f"✨ 成功：已為 [{file}] 嵌入高画质封面。")
                            success_count += 1
                        else:
                            print(f"❌ 下载失败：【{album_name}】")
                            fail_count += 1
                    else:
                        print(f"❌ 未找到封面：【{album_name}】")
                        fail_count += 1
                        
                    time.sleep(0.5) # 連続アクセス防止の軽い休憩
                    
                except Exception as e:
                    print(f"💥 错误 [{file}]: {e}")
                    fail_count += 1

    print("-" * 60)
    print(f"🏁 処理完了！ 成功: {success_count} 首 | 失敗: {fail_count} 首")
    print("💡 提示: 如果Windowsエクスプローラーの表示が空白に見える場合は、フォルダを右クリックして『最新の情報に更新』を押すか、PCを一度再起動してください。データは安全です。")

if __name__ == "__main__":
    # あなたのFLACフォルダのパスを指定してください
    MY_MUSIC_FOLDER = "./my_songs" 
    perfect_cover_embedder(MY_MUSIC_FOLDER)
