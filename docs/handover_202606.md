# handover_202606

## 2026-06-16 Notion gallery trial

### 背景/目的
ユーザから「今のアルバムにこだわりはない」「Notionでもよいのでは」と相談があり、Notionを閲覧用データベースとして試験投入した。

### 判断
- 粒度は画像1枚 = Notion 1レコード。
- 初回対象は最新10セット、合計40枚。
- Notion内の親ページ `Chat Voyage` に `mcp` connection を追加し、APIからDBを作成した。

### 変更内容
- `.gitignore` に `.notion.env` と `.tmp/` を追加。
- `.notion.env.example` を追加。
- `scripts/notion_upload_gallery.py` を追加。dry-run既定で、`--confirm-upload` のときだけNotionへ送信する。
- `docs/notion-gallery-import.md` を追加。設定手順、dry-run、upload手順、試験結果を記録。
- Notion DB表示をGalleryに変更し、カードプレビューで画像が見える状態を確認。
- ChatGPT案を現状DBに照合し、`Chat Voyage Images` を維持したまま、次回以降の投入スキーマに `Status` / `Batch ID` / `Variant` / `Theme` / `Scene` / `Prompt Short` / `Model` / `Aspect Ratio` / `File Size MB` / `Width` / `Height` を追加。
- 新規Notionページ本文は `Prompt` / `Scene` / `Review Notes` の軽量テンプレートにした。
- `docs/notion-gallery-import.md` に推奨ビュー、プロパティ一覧、命名規則、既存データソース同期手順を追記。
- Notion UIで誤ってダッシュボード/空テーブルデータソース面を開いたが、`Images Only` Gallery viewへ復旧した。
- `Images Only` は page cover card preview、medium cards、media fit on、popup page opening、`Date` desc + `Image No` asc の並びに設定済み。
- 既存DB同期用に `scripts/notion_upload_gallery.py` へ `--sync-existing`, `--data-source-id`, `--append-missing` を追加。既存行は `Source path` で照合する。

### 実行結果
- Notion parent page: `Chat Voyage`
- Notion database: `Chat Voyage Images`
- Database ID: `381ecca2-7ba4-81b5-b327-fc2e5a8a55ac`
- Image data source ID: `381ecca2-7ba4-8124-965d-000b2171071a`
- Empty table data source ID created during UI exploration: `381ecca2-7ba4-8047-a3d2-000bb4298c01`
- Uploaded rows: 40
- Uploaded image bytes: about 8.1 MB
- Source range: 2026-06-16 through 2026-06-09

### 検証
実施済み:

```sh
PYTHONPYCACHEPREFIX=.tmp/pycache python3 -m py_compile scripts/notion_upload_gallery.py
python3 scripts/notion_upload_gallery.py --limit 40
python3 scripts/notion_upload_gallery.py --limit 40 --confirm-upload
```

結果:
- dry-run は40件を選択し、合計約8.1MBと表示。
- upload は `done: uploaded 40 images to Notion database 'Chat Voyage Images'` で完了。
- in-app browser で `Chat Voyage Images` database を開き、行とプロパティが表示されることを確認。
- Gallery viewで画像カードが見えることを確認。
- スキーマ拡張後のdry-run `python3 scripts/notion_upload_gallery.py --limit 4` は成功。
- `PYTHONPYCACHEPREFIX=.tmp/pycache python3 -m py_compile scripts/notion_upload_gallery.py` は成功。
- `python3 scripts/validate_gallery.py`: `errors: 0`
- `git diff --check`: 問題なし。
- `python3 scripts/notion_upload_gallery.py --limit 40 --sync-existing --data-source-id 381ecca2-7ba4-8124-965d-000b2171071a`:
  matched 40, missing 0, append_requested false.

### 注意
- Notion token は `.notion.env` に保存し、gitignore済み。
- token はチャット上で共有されたため、継続運用する場合はNotion側で再発行/rotateするのが安全。
- dry-run時に、足りないdata sourceプロパティ定義だけがNotionへ追加される副作用が一度発生した。スクリプトは修正済みで、以降dry-runではプロパティ追加も行わない。
- 既存40件のNotionページへ追加プロパティ値を後付けする実更新は、外部SaaSへのメタデータ送信として承認が必要。`--confirm-upload` 付き実行はまだ未実施。

## 2026-06-16 Album preference feedback

### 背景/目的
ユーザから「アルバムにユーザの好みフィードバックを取ってはどうか」「好みは、絵柄、人、服装、とかかな」と提案があり、アルバムを閲覧だけでなく次回生成の判断材料を集める場所として拡張した。

### 判断
- サーバ保存は導入せず、静的サイトのまま `localStorage` に画像単位の好みを保存する。
- 画像ごとに全体評価 `Love` / `Good` / `Pass`、好み次元タグ、自由メモを保存する。
- 好み次元は `art-style`, `person`, `outfit` を主軸にし、`color`, `silhouette`, `pose`, `place`, `vibe` を補助軸にする。
- 将来の生成へ渡しやすいよう、アルバム全体のフィードバックを JSON export できるようにした。

### 変更内容
- `album.html` の右ペインに Preference feedback UI を追加。
- `assets/album-page.js` に `chat-voyage-feedback-v1` localStorage 保存、サムネイル状態表示、JSON export を追加。
- `assets/album-page.css` にフィードバックUIとサムネイル状態表示のスタイルを追加。
- `scripts/build_album_catalog.py` を更新し、再生成してもフィードバックUIが残るようにした。
- `scripts/validate_gallery.py` でアルバムシェルのフィードバック機能マーカーを検証するようにした。
- `docs/daily-generation-workflow.md` と `skills/daily-fashion-sketch/SKILL.md` に、exported album preference feedback を日次生成前に確認する運用を追加した。
- installed skill copy `/Users/allegro/.codex/skills/daily-fashion-sketch/SKILL.md` は repo copy と同期済み。

### 検証
実施済み:

```sh
python3 scripts/build_album_catalog.py
node --check assets/album-page.js
python3 scripts/validate_gallery.py
git diff --check
```

結果:
- `build_album_catalog.py`: `albums: 34`, `changed: 1`
- `validate_gallery.py`: `daily_images: 139`, `index_figures: 139`, `legacy_album_pages: 34`, `errors: 0`
- repo copy と installed copy の `daily-fashion-sketch/SKILL.md` は `cmp` 一致

### 未実施
- in-app browser での `file://` 実表示確認。Browser policy が `file:///Users/allegro/Applications/ChatVoyage/album.html?...` への遷移をブロックしたため、迂回せず未実施とした。

## 2026-06-16 Album product rebuild

### 背景/目的
ユーザから「アルバムそのものがイマイチ」「33件のアルバムHTMLという構成そのものはいいのか」と指摘があり、個別HTMLテンプレート改善ではなくアルバムのプロダクト構成を見直した。

### 判断
- 33個の個別HTMLを主導線にする構成は不採用。静的サイトとしては動くが、正本が分散し、遷移がファイル設計都合に寄り、テンプレート更新時の差分も大きすぎる。
- 主導線は `album.html?set=...` の単一ビューアに統一。
- `assets/*-album.html` は削除せず、旧リンク互換のリダイレクトページとして残す。

### 変更内容
- `album.html` を追加。単一のアルバムビューア shell。
- `assets/album-data.js` を追加。33セット / 135画像の構造化データ。
- `assets/album-page.js` をデータ駆動ビューアとして作り直し。
- `assets/album-page.css` を単一ビューア用に更新。
- `albums.html` と `index.html` のアルバムリンクを `album.html?set=...` に統一。
- 既存 `assets/*-album.html` 33件は `../album.html?set=...` への legacy redirect に変更。
- `scripts/build_album_catalog.py` を追加。album shell / data JS / album browser / legacy redirect / index link をまとめて生成する正本。
- `scripts/build_album_index.py`, `scripts/rebuild_album_pages.py`, `scripts/backfill_missing_album_pages.py`, `scripts/normalize_album_pages.py` は新ビルダーへの互換ラッパーに変更。
- `scripts/validate_gallery.py` を単一ビューア構成の検証に更新。
- `docs/daily-generation-workflow.md` と `skills/daily-fashion-sketch/SKILL.md` を新しいアルバム運用へ更新。
- installed skill copy `/Users/allegro/.codex/skills/daily-fashion-sketch/SKILL.md` は repo copy と同期済み。

### 検証
実施済み:

```sh
python3 scripts/build_album_catalog.py
node --check assets/album-page.js
node --check assets/album-browser.js
python3 scripts/validate_gallery.py
git diff --check
```

結果:
- `build_album_catalog.py`: `albums: 33`, `changed: 0`
- album data: 33 albums / 135 images / 33 unique slugs / non-WebP data refs 0
- `validate_gallery.py`: `errors: 0`
- repo copy と installed copy の `daily-fashion-sketch/SKILL.md` は `cmp` 一致

### 未実施
- ローカルURLの実ブラウザ視覚確認。今回のセッションでは local `file://` / `127.0.0.1` 表示がツールポリシーで使えなかったため未実施。

## 2026-06-05 Chat Voyage gallery / metadata / daily workflow closeout

### 背景/目的
Chat Voyage は、日次のファッション画像生成を日付別セットとして保存し、後続の Codex や LLM が「都市、ファッションカテゴリ、画像スタイル、人物、ポーズ、場所、結果」を参照して別パターンを作れるようにする小規模創作アーカイブ。今回の主目的は、生成済み画像とホームギャラリーの不整合を解消し、Yokohama セットと Seoul セットを含む全画像を browseable にすること。

### 調査内容
- `assets/daily/` 配下を確認し、14 ディレクトリ、合計 59 PNG が存在することを確認した。
- `index.html` の `figure[data-style]` 数が以前は 47 で、`assets/daily/` の実画像より 12 枚少ない状態だった。
- 不足していたのは主に次の 3 セット。
  - `assets/daily/2026-05-27-yokohama-burgundy-theater-romance/` 4枚
  - `assets/daily/2026-05-31-yokohama-burgundy-theater-3d/` 4枚
  - `assets/daily/2026-06-05-seoul-indie-youth-culture/` 4枚
- 2026-05-27 Yokohama Romance は専用 notes が見当たらなかったため、既存 Yokohama 3D notes の方向性とファイル名から最低限の caption / style / place / category を推定した。
- 既存 skill `/Users/allegro/.codex/skills/daily-fashion-sketch/SKILL.md` を確認した。初期の realistic fashion sketch / fixed roles 寄りで、現在の Chat Voyage 運用との差分がある。

### 変更内容（API/SQL/ファイル）
- `/Users/allegro/Applications/ChatVoyage/index.html`
  - `visible-count` / `total-count` の初期表示を 59 に更新。
  - Place filter に `yokohama` を追加。
  - `2026-06-05 Seoul Indie Youth Culture` セクションを追加。
  - `2026-05-31 Yokohama Burgundy Theater 3D` セクションを追加。
  - `2026-05-27 Yokohama Burgundy Theater Romance` セクションを追加。メタデータは `anime-editorial` / `yokohama` を基本に、category は `street`, `mode`, `lounge`, `resort` とした。
- `/Users/allegro/Applications/ChatVoyage/assets/2026-05-31-yokohama-burgundy-theater-3d-album.html`
  - 4枚の 3D CG セット用アルバムを新規作成。
  - 各画像に category, style, place を明記。
- `/Users/allegro/Applications/ChatVoyage/docs/weeklyreport/weeklyreport_202606.md`
  - 今回の上位目的、成果、課題、失敗をエグゼクティブ向けに追記。
- `/Users/allegro/Applications/ChatVoyage/docs/handover_202606.md`
  - 後続 Codex 向けに調査内容、変更ファイル、検証手順、残課題を記録。
- `/Users/allegro/Applications/ChatVoyage/TODO.md`
  - ギャラリー整合、Yokohama 3D アルバム、Yokohama Romance メタデータ、skill 更新、検証スクリプト化、git 初期化を完了項目として記録。
- `/Users/allegro/Applications/ChatVoyage/skills/daily-fashion-sketch/`
  - Chat Voyage 用に更新した `daily-fashion-sketch` skill の project-tracked copy を追加。
  - installed copy は `/Users/allegro/.codex/skills/daily-fashion-sketch/` に同期済み。

API / SQL の変更はなし。

### 成果
- ホームギャラリーが `assets/daily/` の全画像 59 枚を反映する状態になった。
- Filter group の `style`, `place`, `category` について、index 内の data 値に対応するボタンがすべて存在する状態になった。
- 2026-05-31 Yokohama 3D は個別アルバムからも参照可能になった。
- 2026-05-27 Yokohama Romance は、暫定推定メタデータ付きでホーム閲覧可能になった。

### 課題
- Chat Voyage は当初 `.git` が存在しなかったため、プロジェクト root で作業する方針に切り替えた。以後は `/Users/allegro/Applications/ChatVoyage` を基準ディレクトリにする。
- `daily-fashion-sketch` skill は 2026-06-05 に現行運用へ更新済み。Chat Voyage repo 内の `skills/daily-fashion-sketch/` を追跡対象の正本とし、installed copy を `/Users/allegro/.codex/skills/daily-fashion-sketch/` に同期する。
- 2026-05-27 Yokohama Romance は専用 notes と album を追加済み。メタデータは推定なので、後から当時の生成プロンプトが見つかった場合は更新する。

### 検証手順
実施済み:

```sh
python3 - <<'PY'
from html.parser import HTMLParser
from pathlib import Path
root = Path('/Users/allegro/Applications/ChatVoyage')
# index.html の figure 数、daily PNG 数、local href/src、filter data 値を検証
PY
```

結果:
- `daily_images 59`
- `index_figures 59`
- `missing_refs []`
- `missing_filter_values {'style': [], 'place': [], 'category': []}`
- `album_refs 6`
- `album_missing []`

追加検証:

```sh
python3 scripts/validate_gallery.py
```

結果:
- `daily_images: 59`
- `index_figures: 59`
- `album_pages: 10`
- `errors: 0`

未実施項目:
- installed copy 側 `/Users/allegro/.codex/skills/daily-fashion-sketch/` の個別 git commit

理由:
- installed copy は git repository ではない。追跡可能な正本は Chat Voyage repo 内の `skills/daily-fashion-sketch/` に置いた。

代替確認:
- project-tracked copy と installed copy の内容を同期した。

次回実施条件:
- skill 更新時はまず Chat Voyage repo 内の `skills/daily-fashion-sketch/` を編集し、その後 installed copy に同期する。
