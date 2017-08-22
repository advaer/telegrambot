docker build -t amznlnx
docker run -i --name azl amznlnx
source awsenv/bin/activate

Then according manual:
http://chalice.readthedocs.io/en/latest/topics/packaging.html

docker cp azl:/tmp/package.whl /path/to/package.whl

docker start -i azl
unzip /path/to/zip -d /path/to/vendor