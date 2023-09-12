from cx_Freeze import setup, Executable

files = ["assets/", "backend/", "data/"]

setup(
    name="ControleRefugo",
    version="1.0",
    description="Faz a análise de produções",
    author="Rafael Bilhao",
    options={"build_exe": {"include_files": files}},
    executables=[Executable(script="./main.py", base="Win32GUI", icon="assets/icon.ico")]
)
