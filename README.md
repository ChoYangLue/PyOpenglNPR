# PyOpenglNPR

## 概要
PyOpenglNPRはノンフォトリアリスティック(NRP)な表現ができる機能をpython3で実装したレンダラソフトである。
![screenshot](https://user-images.githubusercontent.com/31681741/30103796-ac60e8dc-932e-11e7-940e-c2d945f7c99c.png)
このソフトは３Dモデルを使用して漫画(アニメ)風の画像を作るソフトを作成することを目的としている。実装した主な機能は以下である。
* レンダリング機能
* ３Dモデルのみ込み
* ３Dモデルの操作
* レンダリング結果の保存
そのほかにも、使いやすさ、UIについても考えた設計をした。

## インストール
実行にはpythonのほか以下の追加ライブラリが必要。
* PyOpenGL
* Pygame
* PIL
* pymeshio

今回のソフトウェア開発には、プログラミング言語としてPythonを使用した。また、仕組みの理解と実装を重視するため、3D描画にはUnityやUnreal Engineを使うのではなく、OpenGLのPython版である、PyOpenGLを使った。PyOpenGLに付属しているGLUTは初期化ができないバグが存在するため、PygameのOpenGL描画機能を使っている。GUI部分には、Tkinterを使用している。これは標準ライブラリである。MMD形式のファイルはバイナリデータなのでそれを読むためにpymeshioというライブラリを使用している。

## プログラム構成
今回作成したソフトウェアは機能ごとにファイルを複数に分割して作成した。そのプログラム構成は以下である。

* index.py		メインのプログラム
* gui.py		GUIを構成するプログラム
* objloader.py	OBJファイルを読み込むプログラム
* mmdloader.py	MMD(pmd)ファイルを読み込むプログラム
* GLSL.py	プログラマブルシェーダ関連のプログラム
* GL2d.py		テキスト表示のプログラム

index.pyを実行することでソフトウェアを使用できる。このファイルで、シェーダーの管理やオブジェクトの操作の処理などをしている。また、Tkinterとpygameのウィンドウを一体化させる処理も行っている。
> os.environ['SDL_WINDOWID'] = str(canvas.winfo_id())
> os.environ['SDL_VIDEODRIVER'] = 'windib'
xwindowとの相性が悪いようで、Linux環境ではうまくウィンドウが統合されず、メイン画面とGUI画面が分離してしまう。gui.pyのファイルにはGUIを構成するためのプログラムが書かれており、主にボタン関連の処理を書いている。objloader.py、mmdloader.pyでは、主にファイルパーサーを記述している。GLSL.pyには各シェーダーをコンパイルする処理などが主に書かれている。詳しくは次章で解説。GL2d.pyは、文字列を画面に表示するためのビルボードを作成、表示するプログラムなどが書かれているが、本プログラムでは使用していない。セリフ機能で使用したかったが、座標値計算がうまくいかず、任意の場所に配置できないバグが存在するためである。

## 実行
1. index.pyを実行。
2. 右側のファイル選択ボタンから対応するファイルを読み込む。
3. 好みのレンダラに切り替える。
4. 保存ボタンでレンダリング結果を保存できる。

## その他
2017年前期作成
