from cx_Freeze import setup, Executable

# Define the target executable
target = Executable(
    script="main.py",
    base="Win32GUI",  # Use "Console" for console applications
    target_name='Flac to Wav Converter.exe'
)

options = {
    'build_exe': {
        'include_files': ['E:/Project/PyCharm/FlacToWavConverter/venv/Lib/site-packages/tkdnd/tkdnd/win64/'],
    }
}


# Setup options
setup(
    name="Flac to Wav Converter",
    version="1.0",
    description="Batch convert Flac/Ape files into Wav with drag-and-drops.",
    executables=[target],
    options=options
)
