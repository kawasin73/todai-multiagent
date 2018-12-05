# totai-multiagent

東京大学工学部システム創成学科の「マルチエージェントシステム」の課題。

PSO（粒子群最適化）と ABC（人工蜂コロニー）アルゴリズムによって以下の関数の最適化を行います。

- Sphere 関数
- Rastrigin 関数
- Rosenbrock 関数
- Griewank 関数
- Alpine 関数
- 2n minima 関数

## Install

対象としているのは macOS です。

実行環境の構築に Pipenv を利用しています。

```bash
$ brew install pipenv
```

以下の手順でインストールしてください。

```bash
$ git clone https://github.com/kawasin73/todai-multiagent.git
$ cd todai-multiagent
$ pipenv install
```

macOS の場合、virtualenv を利用することで、以下のエラーが発生することがあります。

```
ImportError: Python is not installed as a framework. The Mac OS X backend will not be able to function correctly if Python is not installed as a framework. See the Python documentation for more information on installing Python as a framework on Mac OS X. Please either reinstall Python as a framework, or try one of the other backends. If you are using (Ana)Conda please install python.app and replace the use of 'python' with 'pythonw'. See 'Working with Matplotlib on OSX' in the Matplotlib FAQ for more information.
```

その場合は、以下の手順で修正してください。

1. Python のコンソール内で、以下のようにして `matplotlibrc` の場所を表示する
    ```
    $ python
    >>> import matplotlib
    >>> matplotlib.matplotlib_fname()
    '/Users/kawasin73/PycharmProjects/todai-multiagent/.venv/lib/python3.7/site-packages/matplotlib/mpl-data/matplotlibrc'
    ```
2. `matplotlibrc` の、`backend` の欄を修正する
    ```
    backend: TkAgg
    ```

参考：[Pipenv で起きる Matplotlib まわりのエラー](https://qiita.com/utahkaA/items/ad9aa825832c5909575a)

## 実行

以下のコマンドで実行できます。

```
python main.py
```

## LICENSE

MIT
