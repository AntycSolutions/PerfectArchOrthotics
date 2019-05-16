
platform=`python -c "import platform; print(platform.system())"`

file=`realpath ${BASH_SOURCE[0]}`
dir=`dirname $file`

if [[ "$platform" == 'Linux' ]]; then
    source $dir/../venv_perfect_arch/bin/activate
elif [[ "$platform" == 'Windows' ]]; then
    source $dir/../venv_perfect_arch/Scripts/activate
else
    echo "Unsupported platform: $platform"
fi
