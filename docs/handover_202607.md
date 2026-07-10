# handover_202607

## 2026-07-11 Album UX / canonical data migration / closeout commit

### 背景/目的
ユーザから、アルバム・index・album detail が「トップバーや重複テキストばかり目立って画像を見にくい」「キャラクターと通常日次が混ざっている」「画像だけを大きく見ながら前後移動したい」「同じ情報が何度も出ている」と継続的に指摘された。指摘は仮説として扱い、実際にHTML/JS/CSS/生成スクリプトを確認した結果、個別の表示文言だけでなく、ソースデータ、生成物、フィルタ軸、一覧/詳細の役割分担をまとめて直す必要があった。

今回の目的は、Chat Voyage を「画像を増やすだけの静的ギャラリー」から、「画像中心に閲覧し、日常と紫乃を分け、アルバム単位/画像単位でレビューできる静的プロダクト」にすること。

### 主要な構造変更
- `data/albums/**/*.json` をアルバム・画像メタデータの正本にした。
  - 通常日次: `data/albums/daily/YYYY/MM/YYYY-MM-DD-theme.json`
  - 紫乃: `data/albums/characters/shino/YYYY/MM/YYYY-MM-DD-theme.json`
- 表示画像は `assets/albums/...` 配下へ移行した。
  - 通常日次: `assets/albums/daily/YYYY/MM/YYYY-MM-DD-theme/`
  - 紫乃: `assets/albums/characters/shino/YYYY/MM/YYYY-MM-DD-theme/`
- 旧 `assets/daily/*` と直下 `notes/*.md` は削除扱いになっているが、これは新構成への移動・正規化の一部。生成資産なので、今後も追加整理する場合はAGENTSの「明示承認なしに originals を削除しない」を守る。
- `notes/albums/...` へメモを移した。トップ一覧ではメモリンクを目立たせず、詳細ページで確認する思想に寄せた。
- `scripts/build_album_catalog.py` は `index.html`、`albums.html`、`album.html`、`assets/album-data.js`、legacy redirect HTML を生成する中心スクリプトになった。
- `docs/album-json-contract.md` を追加し、必須フィールド、`summaryJa`、`locationDetail`、`preferredAspectRatio`、画像実測 `aspectRatio`、更新フローを記述した。

### UI実装メモ
`index.html`:
- 画像一覧として扱う。`すべて`、`日常`、`キャラクター` のフィルタを持つ。
- `すべて` 選択時は、日常/キャラクターを分けた見出しで並列表示しない。1つの `gallery-collection-all` に混在表示する。
- 並び順ドロップダウンを追加。`アルバム日付 新しい順`、`アルバム日付 古い順`、`画像タイトル`、`アルバムタイトル`。
- 画像サイズ `小/大` を追加。
- キャプションは重複を避けるため、`日付 / 都市 / 何枚目` と `カテゴリ / 具体ラベル / 絵柄` の2段にした。例: `2026-06-21 / Fictional Port City / 02`、`Home / lobby bag fish guide / Anime Editorial`。

`albums.html`:
- アルバムブラウザ。`画像一覧`への戻りリンク、`すべて`、`キャラクター`、`日常` のモードを持つ。
- `すべて` では `album-section-all` に全カードを集約し、`キャラクターアルバム` / `日常アルバム` 見出しで分断しない。
- `キャラクター` または `日常` 選択時だけ、それぞれのセクションを表示する。
- `日付`ビューのボタンは廃止し、並び順の `日付ごと` に統合した。`state.sort === "date-groups"` のとき `data-view="date"` になる。
- 画像サイズ `小/大` を追加。サムネイルは `object-fit: cover` に寄せ、空白が目立つ表示を避けた。
- モバイルでは操作列を詰め込みすぎないよう、検索欄を上段へ逃がすCSSにした。

`album.html`:
- 詳細ビュー。ユーザの「トップバーではなく画像を見たい」に合わせ、stage画像と右側パネル中心の構成へ寄せた。
- 左右キー・`<`/`>`ボタンで画像移動。クリックでライトボックス。
- フィードバックは `好き` / `それほどでもない` に簡素化し、`見送り`や`良い`の曖昧さをなくした。
- メモリンクは詳細画面側に残す。
- アルバムセレクト右に前後アルバム移動の `<` / `>` ボタンを追加。`assets/album-page.js` の `renderAlbumNeighbors()` が `albumIndex` から循環リンクを設定する。

### メタデータ/JSON実装メモ
- 旧 `category` は残すが、フィルタ・詳細表示では以下を追加使用する。
  - `occasion`: 場面
  - `venue`: 場所カテゴリ
  - `activity`: 行動
  - `outfit`: 服装カテゴリ
  - `locationDetail`: 具体的な場所。都市名だけや行動文ではなく、UI表示に耐える場所名にする。
- `summaryJa` はUI向け短文。日付は別表示されるので入れない。
- `preferredAspectRatio` はアルバム生成前に決める意図比率。画像ごとの `aspectRatio` は `scripts/enrich_album_source_metadata.py` で実測から入れる。
- `scripts/enrich_album_source_metadata.py --refresh-text` は、既存の人間編集した `summaryJa` / `locationDetail` を上書きし得るので、意図的な再生成時だけ使う。

### 重要ファイル
- `scripts/build_album_catalog.py`: catalog生成、UI shell生成、gallery/album card生成、legacy redirect生成。
- `scripts/enrich_album_source_metadata.py`: JSONへ画像実測サイズと比率を入れる。通常はrefresh-textなしで使う。
- `scripts/validate_gallery.py`: JSON、生成物、画像参照、locationDetail、寸法、album shellを検証する。
- `assets/album-browser.js` / `assets/album-browser.css`: `albums.html` のフィルタ、sort、view、size、date-groups。
- `assets/album-page.js` / `assets/album-page.css`: `album.html` の画像移動、lightbox、feedback、album select、前後アルバム移動。
- `docs/album-json-contract.md`: JSON契約。後続は最初に読む。
- `skills/daily-fashion-sketch/SKILL.md`: 通常日次生成。
- `skills/shino-album-generation/SKILL.md`: 紫乃固定キャラクター生成。

### Skill確認
`skill-creator` 標準手順を確認した。要点は concrete examples -> reusable contents -> init -> edit -> quick_validate -> forward-test。新規skillは、`SKILL.md` を簡潔にし、詳細は必要に応じて references/scripts へ分ける。

今回の判断:
- `daily-fashion-sketch`: 通常日次生成、WebP保存、canonical JSON、catalog rebuild、validation、PNG/original handling を既に扱える。更新は現状必須ではない。
- `shino-album-generation`: 紫乃固定キャラクターの生成、i2i参照、WebP、JSON、notes/log、validation を扱える。更新は現状必須ではない。
- 新規skill候補: `chat-voyage-album-ops`。今回のような album UX、JSON移行、Pages/iPhone実機確認、index/albums/album detailレビューを今後も繰り返すなら作る価値がある。ただし現時点では、まず `docs/album-json-contract.md` とこのhandoverで十分。次回同じレビュー作業が発生したらskill化を検討する。

### 検証済みコマンド
今回のcloseout直前に通したもの:

```sh
python3 scripts/validate_gallery.py
node --check assets/album-browser.js
node --check assets/album-page.js
python3 -m py_compile scripts/build_album_catalog.py
git diff --check
```

代表結果:
- `python3 scripts/validate_gallery.py`: `errors: 0`
- 2026-07-11時点の検証では `album_images: 302`、`album_source_files: 67`、`index_figures: 302`、`legacy_album_pages: 67`。

### 未完了/注意
- `localhost:8765` のブラウザ自動操作は、途中で環境側ポリシーにより拒否された回がある。そのため、最終確認は静的検証とHTML/CSS/JS確認が中心。GitHub Pages本番、Safari、iPhoneでの目視確認は残る。
- 大規模移行でファイル削除/追加が多い。commit後も、本当に旧パス参照が残っていないかは `python3 scripts/validate_gallery.py` を正とする。
- 実機で見ると、画像サイズ・余白・サムネイルの切り抜き・フィルタの密度はまだ改善余地が出る可能性が高い。
- アルバムUIレビューを今後も継続するなら、`chat-voyage-album-ops` skillを `skill-creator` 手順で作る。想定examplesは「albums.htmlをiPhone幅でレビューして」「indexキャプション重複を直して」「canonical JSONを増やしてcatalog再生成して」「GitHub Pages反映後に画像閲覧導線を確認して」。

## 2026-07-04 Shino fixed-character album closeout

### 背景/目的
ユーザは紫乃（Shino）の「日常アルバム」を継続制作したい。今回の一連のセッションでは、画像生成だけでなく、キャラクター設定、街設定、参照画像運用、i2i前提、WebP保存、album catalog登録、人物一貫性レビュー、次回への引き継ぎまでを整理した。

紫乃は25歳。海沿いの温暖な架空港町で一人暮らしをする、製品規格ラボのテストエンジニア。仕事はUL/TUV系の国際認証・規格試験ラボを連想するが、実在社名やロゴは出さない。街は南紀/伊勢の海と気候、ニュルンベルク風の旧市街、港、市場、路面電車、水族館、丘、古い城壁跡、モニュメント広場、小さなバーを混ぜた架空都市。水族館は仙台うみの杜水族館のような明るい地域水槽感を参照しつつ、短い水中トンネルやクラゲ/地味な魚/深海魚寄りの嗜好を持たせる。

### 調査内容
- 既存の project instruction は `AGENTS.md`。生成資産は project materials として扱い、明示依頼なしに originals を削除しない。daily fashion outputs は collage ではなく個別画像。
- 月次ドキュメント配置は既存実績から以下を使用した。
  - `docs/weeklyreport/weeklyreport_YYYYMM.md`
  - `docs/handover_YYYYMM.md`
  - `TODO.md`
- 既存 skill を確認した。
  - `skills/daily-fashion-sketch/SKILL.md`: Chat Voyage の4枚日次生成、WebP化、album catalog、gallery validationを対象。character album mode には触れているが、紫乃の長尺セットや参照昇格までは十分に専用化されていない。
  - `/Users/allegro/.codex/skills/shino-image-review/SKILL.md`: 紫乃画像レビュー、25歳への成長判定、scene fit、参照昇格判断に強い。生成前後の保存/catalog更新までは対象外。
  - `/Users/allegro/.codex/skills/.system/skill-creator/SKILL.md`: 新規 skill は concrete examples -> reusable contents -> `init_skill.py` -> SKILL.md/resources編集 -> `quick_validate.py` -> forward-test が標準。

### 変更内容（API/SQL/ファイル）
この closeout で直接追記したファイル:
- `docs/weeklyreport/weeklyreport_202607.md`
- `docs/handover_202607.md`
- `TODO.md`

今回の一連の紫乃制作で重要な既存/生成済みファイル:
- `assets/albums/characters/shino/2026/06/2026-06-06-13-shino-ise-weather-lab/`
- `assets/albums/characters/shino/2026/06/2026-06-14-18-shino-ise-weather-lab/`
- `assets/albums/characters/shino/2026/06/2026-06-19-shino-birthday-dj-night/`
- `assets/albums/characters/shino/2026/06/2026-06-21-shino-coastal-lab-aquarium/`
- `assets/albums/characters/shino/2026/06/2026-06-21-shino-weekend-port-town/`
- `notes/albums/characters/shino/2026/06/2026-06-06-13-shino-ise-weather-lab.md`
- `notes/albums/characters/shino/2026/06/2026-06-14-18-shino-ise-weather-lab.md`
- `notes/albums/characters/shino/2026/06/2026-06-19-shino-birthday-dj-night.md`
- `notes/albums/characters/shino/2026/06/2026-06-21-shino-coastal-lab-aquarium.md`
- `notes/albums/characters/shino/2026/06/2026-06-21-shino-weekend-port-town.md`
- `assets/album-data.js`
- `index.html`
- `albums.html`
- `logs/generation-2026-06.md`
- `prompts/character-shino.md`
- `prompts/character-album-policy.md`

API / SQL の変更はなし。

### 成果
- 紫乃の基本設定をカテゴリ別に固めた。成人25歳、静かで観察力が高い、朝が弱い、魚/低音/古い建物/本に深く沈む、方向音痴、仲の良い同僚とは笑う、金曜夜と夏だけ大胆になる、という軸が有効。
- 自宅は港と旧市街の境目にある古い建物を改装した1DK。高い窓、白い壁、木の床、古い机、本棚、測定器小物、魚図鑑、DJフライヤー、黒いヘッドホン、折りたたみ自転車、1階ロビーがある。
- 参照画像は `/Users/allegro/Applications/ChatVoyageIntime/references/everyday_album_v2/` を通常 active set として使う。古い18-20歳相当の `character_core` は同一人物性の根拠であり、現在の25歳のターゲットではない。
- 6/14-18 セットの人物一貫性レビューでは、全体として同一人物性は高い。強い current Shino 候補は以下。
  - `assets/albums/characters/shino/2026/06/2026-06-14-18-shino-ise-weather-lab/03-0614-aquarium-tunnel-teal-wrap.webp`
  - `assets/albums/characters/shino/2026/06/2026-06-14-18-shino-ise-weather-lab/08-0617-emc-lab-pale-blue-orange.webp`
  - `assets/albums/characters/shino/2026/06/2026-06-14-18-shino-ise-weather-lab/09-0617-old-town-bar-burgundy-seagreen.webp`
- 6/19 金曜夜・誕生日DJセットは現在の作業ツリーでは完成済み。6枚の WebP、notes、album-data、index、generation log に存在する。古い引き継ぎメモに「保存していない」とあったが、それは現在状態と矛盾するため採用しない。
- 6/19 セットの plot は、ラボ退勤、同僚の小さな誕生日祝い、短いDJセット、フライヤー裏の夏旅行メモ、雨上がり旧市街で迷う、自室の低音余韻。全6枚とも notes 上では Adopt。

### 課題
- 6/2 Shino Mexico City など、一部セットには WebP 化後の PNG コピーが残っている。表示参照は WebP で、現時点の `scripts/validate_gallery.py` は通るが、AGENTS の「generated assets は project materials、明示依頼なしに originals を削除しない」に従い、削除や archive 移動はユーザ承認後に行う。
- `2026-06-02-shino-mexico-city-mamey-coral` は `index.html`、`assets/album-data.js`、`albums.html`、notes、ファイル実体に同期済み。残る問題は catalog 未同期ではなく、固定キャラクターを Chat Voyage 内で `character` collection として扱い続けるか、ChatVoyageIntime 側へ分けるかの設計判断。
- 紫乃は黒/ネイビー/チャコールに寄りやすい。`notes/albums/characters/shino/2026/06/2026-06-19-shino-birthday-dj-night.md` にも、47 Shino images の text-level scan で39件が暗色言及、28件が black 言及と記録されている。以後は淡い水色、ラベンダー、白、控えめな花柄、シーグラス、コーラル、セージなどを意識して回す。
- 「眠そうな目」は朝だけに寄せる。通常の紫乃は sleepy ではなく、quiet self-possession / observant / steady と書く方がよい。
- `daily-fashion-sketch` の step 12 は、Chat Voyage の AGENTS と今回の運用に合わせ、PNG/原本を明示承認なしに削除しない表現へ更新済み。
- 紫乃生成は repo 専用の `skills/shino-album-generation/` として分離した。`daily-fashion-sketch` は通常日次・一般テーマ用に残し、紫乃は人物継続、i2i参照、Shino active refs、黒/ネイビー偏重、WebP/catalog/log接続まで専用 skill で扱う。

### 検証手順
今回 closeout で確認済み:

```sh
rg --files | rg '(^|/)(weeklyreport_[0-9]{6}\.md|handover_[0-9]{6}\.md|TODO\.md|AGENTS\.md)$'
sed -n '1,220p' AGENTS.md
sed -n '1,260p' docs/weeklyreport/weeklyreport_202606.md
sed -n '1,260p' docs/handover_202606.md
sed -n '1,260p' TODO.md
sed -n '1,220p' skills/daily-fashion-sketch/SKILL.md
sed -n '1,240p' /Users/allegro/.codex/skills/shino-image-review/SKILL.md
find assets/albums/characters/shino/2026/06/2026-06-19-shino-birthday-dj-night -maxdepth 1 -type f -print | sort
sed -n '1,240p' notes/albums/characters/shino/2026/06/2026-06-19-shino-birthday-dj-night.md
```

今回 closeout 後に実行した検証:

```sh
git diff --check
python3 scripts/validate_gallery.py
```

結果:
- `git diff --check`: 問題なし。
- `python3 scripts/validate_gallery.py`: `errors: 0`
  - `daily_images: 250`
  - `daily_source_images: 250`
  - `index_figures: 250`
  - `legacy_album_pages: 55`

次回実施すべき検証:

```sh
python3 scripts/validate_gallery.py
git diff --check
```

現在の注意点:
- PNG コピーは残っているが、現時点の `validate_gallery.py` では error ではない。表示・catalog は WebP 参照で揃っている。
- PNG コピーを削除・移動・archive する場合は、AGENTS の generated assets 方針に従い、ユーザ承認を取る。
- `2026-06-02-shino-mexico-city-mamey-coral` の catalog 同期は済んでいる。残る論点は固定キャラクターを通常日次と分けて評価・閲覧する設計である。

### Skill化メモ
標準手順は `skill-creator` に従う。新規作成するなら、まず concrete examples を整理する。

想定 examples:
- 「6/14-6/18 の紫乃日常を、i2i参照を使って14枚生成して」
- 「人物一貫性をレビューして、current-growth 参照候補を選んで」
- 「金曜夜の紫乃を6枚。DJ nightだが派手なparty girlにしないで」
- 「WebP化して album catalog / index / notes / log に入れて」

Reusable contents:
- Shino active reference path list
- prompt guardrails for adult 25, black/navy drift, no school uniform feel, quiet self-possession
- generation output checklist
- WebP/catalog/log validation checklist
- PNG/original handling policy
- abnormal image_gen output stop rule

2026-07-05 に方針を更新し、紫乃の生成・保存・catalog 接続は repo 専用の `skills/shino-album-generation/` として分離した。既存の `shino-image-review` はレビュー面、`shino-album-generation` は生成から後処理までを担当する。

## 2026-07-04 Daily generation, album UI, Pages, and workflow closeout

### 背景/目的
この一連のセッションでは、Chat Voyage の日次ファッション画像生成とアルバム閲覧基盤をまとめて見直した。ユーザの主な問題意識は、生成画像が「見たことある」絵に戻ること、自然な服装が guardrail によって歪むこと、年齢帯や生活シーンの差分が弱いこと、アルバムがプロダクトとして十分でないこと、Notion/GitHub Pages のどちらを閲覧面にするか、固定キャラクター群が通常日次へ混ざることだった。

日次画像は、4枚のファッションボードというより「その都市の具体的な場所で、成人女性が生活し、その日の服装を選んでいるスナップ」として扱う方向に寄せた。露出の有無は主問題ではなく、気温、湿度、天気、時間帯、屋内外、移動、活動、本人の好み、場の規範に対して自然かを見る。

### 調査内容
- `AGENTS.md` を確認。生成資産は project materials なので、明示依頼なしに originals を削除しない。これは `daily-fashion-sketch` と `docs/daily-generation-workflow.md` の旧「PNG削除」記述と衝突していた。
- `docs/github-pages-workflow.md` を確認。Notion は主閲覧面ではなく、GitHub Pages で静的サイトを公開する方針になっている。
- `prompts/repetition-guardrails.md` を確認。最近の反復問題は、服単体ではなく、カテゴリ、構図、視線、場所、レッグウェア、実効画風、天気表現、フェリー/交通構図まで含めて見る方針に更新済み。
- `skills/daily-fashion-sketch/SKILL.md` を確認。現行 skill は日次4枚生成に加え、character day album、Shino profile、metadata axes、lifestyle snapshot、action-first pose、effective style、gaze mix まで相当程度取り込んでいる。新規 skill を即作るより、まず既存 skill の不整合を直すのが妥当。
- `skill-creator` の標準手順を確認。新規 skill は concrete examples -> reusable contents -> init -> edit -> quick_validate -> forward-test。紫乃は `daily-fashion-sketch` では一般的すぎるため、repo 専用 skill として `skills/shino-album-generation/` を作成した。

### 変更内容（API/SQL/ファイル）
この closeout で直接更新したファイル:
- `docs/weeklyreport/weeklyreport_202607.md`
- `docs/handover_202607.md`
- `TODO.md`
- `skills/daily-fashion-sketch/SKILL.md`
- `docs/daily-generation-workflow.md`

このセッション全体で重要な生成/運用対象:
- `album.html`
- `albums.html`
- `index.html`
- `assets/album-browser.css`
- `assets/album-browser.js`
- `assets/album-data.js`
- `assets/album-page.css`
- `assets/albums/daily/2026/06/2026-06-18-hong-kong-orchid-chrome-rev2/`
- `assets/albums/daily/2026/06/2026-06-19-osaka-orchid-friday-rev2/`
- `assets/albums/daily/2026/06/2026-06-20-kuala-lumpur-cempaka-saturday-snapshots/`
- `assets/albums/daily/2026/06/2026-06-21-sydney-wattle-winter-harbor/`
- `assets/albums/daily/2026/06/2026-06-22-copenhagen-rhubarb-solstice/`
- `assets/albums/daily/2026/06/2026-06-23-hanoi-lotus-rain-errands/`
- `assets/albums/daily/2026/06/2026-06-24-istanbul-sumac-bosphorus-gaze-mix/`
- `assets/albums/daily/2026/06/2026-06-25-madrid-azulejo-heat-life/`
- `assets/albums/daily/2026/06/2026-06-26-sao-paulo-jabuticaba-winter-motion/`
- `assets/albums/daily/2026/06/2026-06-27-buenos-aires-malbec-winter-culture/`
- `assets/albums/daily/2026/06/2026-06-28-vancouver-sea-glass-sunday/`
- `assets/albums/daily/2026/06/2026-06-29-lagos-adire-indigo-rain-monday/`
- `assets/albums/daily/2026/07/2026-07-03-mexico-city-tezontle-coral-style-study/`
- corresponding `notes/YYYY-MM-DD-*.md`
- `logs/generation-2026-06.md`
- `logs/generation-2026-07.md`
- `prompts/category-presets.md`
- `prompts/repetition-guardrails.md`
- `prompts/character-album-policy.md`
- `prompts/character-shino.md`
- `scripts/build_album_catalog.py`
- `scripts/gallery_metadata.py`
- `scripts/validate_gallery.py`

API / SQL の変更はなし。

Skill更新:
- `skills/daily-fashion-sketch/SKILL.md` の PNG 方針を修正する。WebPを表示正本にするが、`.codex` 原本や project に残った PNG は明示承認なしに削除しない。不要な project PNG は削除ではなく archive/move も含めてユーザ判断後に扱う。
- `docs/daily-generation-workflow.md` も同じ方針へ揃える。
- installed copy `/Users/allegro/.codex/skills/daily-fashion-sketch/SKILL.md` は、repo 内 copy を正本として同期済み。`agents/openai.yaml` も repo 内 copy と一致確認済み。

### 成果
- 日次生成の品質判断を、「露出がある/ない」ではなく「その人がその場所・天気・活動で自然に着る服か」へ整理した。
- 年齢帯ごとの違いを、色調だけではなくシルエット、生活シーン、素材、アクセサリ、態度、靴、レッグウェアで出す方針にした。
- `market/gallery/lounge/transit` 偏重を避け、`music-night`、`bar`、`disco`、`bookstore`、`theater`、`library`、`home`、`office`、`ceremony`、sports/activity space などをカテゴリ/場所軸へ拡張した。
- 実在の都市・場所は「風」ではなく具体名で扱う方針にした。例: Hanoi Social Club は Hanoi Social Club として扱う。ただし logos、readable marks、single-source copying は避ける。
- `data-category` が scene / place / clothing を兼ねすぎる問題に対し、`data-occasion`、`data-venue`、`data-activity`、`data-outfit` を追加し、閲覧・フィルタ・レビューの軸を分けた。
- アルバムUIは GitHub Pages で動く静的サイトとして見直した。Notion は一度試したが、主閲覧面から撤退。localStorage の好みフィードバックは個人レビュー用途として残す方向。
- 6/29 Lagos Adire Indigo Rain Monday を生成し、4枚の WebP、notes、log、index、album redirect に接続した。画像自体は概ね採用水準で、最終2枚目は靴の読める風マーク懸念で再生成したものを採用している。

### 課題
- `python3 scripts/validate_gallery.py` は現在 `errors: 0` で通る。6/2 Shino Mexico City の PNGコピーは残っているが、表示・catalog は WebP 参照で同期済み。
- `assets/albums/characters/shino/2026/06/2026-06-02-shino-mexico-city-mamey-coral/` は PNG と WebP が両方ある。AGENTS により明示承認なしに削除しない。
- `index.html`、`assets/album-data.js`、`albums.html` には `2026-06-02-shino-mexico-city-mamey-coral` が同期済み。固定キャラを Chat Voyage 内で続けるか、Chat Voyage 外へ移すかの判断は引き続き必要。
- 固定キャラクター群は通常日次の novelty 判定を歪める。Chat Voyage 内に残すなら `data-collection="character"` / `data-character="shino"` で明確に分け、通常 daily とは別プールでレビューする。
- GitHub Pages 本番反映とiPhone閲覧は、静的ページとして再度確認が必要。特にライトボックス下部テキスト被り、上部領域の大きさ、grid/list切替、フィルタ後の画像サイズ、前後送りは実ブラウザで確認する。
- `scripts/__pycache__/` が untracked に見える。コミット対象から外すか `.gitignore` を確認する。

### 検証手順
closeout 前に確認した状態:

```sh
git status --short --branch
```

結果:
- `## main...origin/main [ahead 1]`
- 多数の modified / untracked がある。既存変更を戻さないこと。

closeout 後に実行した検証:

```sh
python3 /Users/allegro/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/daily-fashion-sketch
python3.10 /Users/allegro/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/daily-fashion-sketch
cmp -s skills/daily-fashion-sketch/SKILL.md /Users/allegro/.codex/skills/daily-fashion-sketch/SKILL.md
cmp -s skills/daily-fashion-sketch/agents/openai.yaml /Users/allegro/.codex/skills/daily-fashion-sketch/agents/openai.yaml
git diff --check
python3 scripts/validate_gallery.py
```

結果:
- `python3 quick_validate.py`: PyYAML がなく `ModuleNotFoundError: No module named 'yaml'`。
- `python3.10 quick_validate.py`: `Skill is valid!`
- repo内 `daily-fashion-sketch` と installed copy の `SKILL.md` / `agents/openai.yaml`: `cmp -s` 一致。
- `git diff --check`: 問題なし。
- `python3 scripts/validate_gallery.py`: `errors: 0`
  - `daily_images: 250`
  - `daily_source_images: 250`
  - `index_figures: 250`
  - `legacy_album_pages: 55`

次に解消するなら、まず方針を決める:
- Chat Voyage 内に残す: `data-collection="character"` / `data-character="shino"` と通常日次のレビュー分離を維持する。
- ChatVoyageIntime に分ける: 画像・notes・album redirect・index/log参照を移す。削除ではなく移動/退避で扱い、ユーザ承認を取る。
- PNGコピーを整理する: 表示参照がWebPで揃っていることを確認済みだが、削除・移動・archive はユーザ承認後に行う。

### Skill化メモ
2026-07-05 時点で、紫乃の生成運用は repo 専用 skill として作成済み。

候補:
- `shino-album-generation`: 固定キャラ紫乃の生成、i2i参照、current-growth参照候補、黒/ネイビー偏重、街/水族館/ラボ/音楽/自宅の生活導線、WebP/catalog/log接続までを扱う。repo 内正本は `skills/shino-album-generation/`。
- `chat-voyage-album-review`: GitHub Pages/静的アルバムUIのブラウザレビュー、grid/list、lightbox、filters、mobile layout、localStorage feedback、Pages反映確認を扱う。

今回は `daily-fashion-sketch` の更新で足りる範囲:
- 通常日次4枚の生成。
- 具体的な都市/場所。
- natural clothing by climate/activity。
- lifestyle snapshot / action-first pose。
- age-band differentiation。
- metadata axes。
- character day album の基本分離。
- PNG/original handling policy。

新規 skill を作る判断条件:
- 紫乃の固定キャラ生成を今後も Chat Voyage/ChatVoyageIntime で継続し、毎回 i2i参照・参照昇格・人物一貫性レビュー・album catalog 接続まで行うなら専用化する。
- アルバムUIの本番Pagesレビューを今後も繰り返すなら、review skill 化よりまず `docs/github-pages-workflow.md` と既存 Playwright/Browser 手順を固める。
