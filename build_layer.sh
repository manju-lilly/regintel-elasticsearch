path="layers"
package="${1}"
layername="${2}"
mkdir -p $path
pip install "${package}" --target "${path}/python/lib/python3.7/site-packages/"
cd $path && 7z a -r ../lambdalayer.zip .

