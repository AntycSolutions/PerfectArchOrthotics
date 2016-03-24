
platform=`python -c "import platform; print(platform.system())"`

if [[ "$platform" == 'Linux' ]]; then
    source ../venv_perfect_arch/bin/activate
elif [[ "$platform" == 'Windows' ]]; then
    source ../venv_perfect_arch/Scripts/activate
else
    echo "Unsupported platform: $platform"
fi
