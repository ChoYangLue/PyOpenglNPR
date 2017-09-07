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

## 実行
1. index.pyを実行。
2. 右側のファイル選択ボタンから対応するファイルを読み込む。
3. 好みのレンダラに切り替える。
4. 保存ボタンでレンダリング結果を保存できる。  

推奨実行環境はWindows  
Linuxでも実行は可能だが、UIが別ウィンドウとなる。Macは不明。

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

## シェーダー
![7-29-35-50](https://user-images.githubusercontent.com/31681741/30154385-b32cd70e-93f4-11e7-958f-028857c64d46.png)
![6-9-49-56](https://user-images.githubusercontent.com/31681741/30154428-ce64ae34-93f4-11e7-85db-d286a6a15ca4.png)

## その他
2017年前期作成

## 参考文献
http://qiita.com/edo_m18/items/71f6064f3355be7e4f45 shader+pyopengl
http://miffysora.wikidot.com/pyopengl-shader
https://showa-yojyo.github.io/notebook/python-pyopengl/shader.html
http://qiita.com/ar90n@github/items/934b1048b3173d2a3b04
https://github.com/hgomersall/Blog-Code/tree/master/opengl_utils

shader
http://www.arakin.dyndns.org/glsl_cartoon.php
http://gamescience.jp/2009/Paper/Matsuo_2009.pdf
https://www21.atwiki.jp/opengl/pages/318.html
http://marina.sys.wakayama-u.ac.jp/~tokoi/?date=20080218
http://python-opengl-examples.blogspot.jp/
https://wgld.org/d/webgl/w048.html
https://wgld.org/d/webgl/w077.html

GLSL
http://d.hatena.ne.jp/programer_hoshimi/20101027
https://wgld.org/d/glsl/g001.html
http://sssiii.seesaa.net/article/392425404.html
http://d.sonicjam.co.jp/post/130263392711

collada
http://miffysora.wikidot.com/dae
http://maverickproj.web.fc2.com/WebGL_15/collada.js
http://maverickproj.web.fc2.com/WebGL_15/WebGL_15.html
http://miffysora.wikidot.com/opengl-antialiasing

FXAA
http://www.geeks3d.com/20110405/fxaa-fast-approximate-anti-aliasing-demo-glsl-opengl-test-radeon-geforce/3/
https://gamedev.stackexchange.com/questions/119545/inverted-fxaa-shader
http://zerogram.info/?p=941#more-941
http://nullege.com/codes/show/src@b@l@blenderpython-HEAD@scripts@addons_extern@blender26-meshio@export_pmx.py/105/pymeshio.pmx.Bone
http://sssiii.seesaa.net/article/411486529.html

