# A virtualenv running Python3.6 on Amazon Linux/EC2 (approximately) simulates the Python 3.6 Docker container used by Lambda
# and can be used for developing/testing Python 3.6 Lambda functions
# This script installs Python 3.6 on an EC2 instance running Amazon Linux and creates a virtualenv running this version of Python
# This is required because Amazon Linux does not come with Python 3.6 pre-installed
# and several packages available in Amazon Linux are not available in the Lambda Python 3.6 runtime

# The script has been tested successfully on a t2.micro EC2 instance (Root device type: ebs; Virtualization type: hvm)
# running Amazon Linux AMI 2017.03.0 (HVM), SSD Volume Type - ami-c58c1dd3
# and was developed with the help of AWS Support

# The steps in this script are:
# - install pre-reqs
# - install Python 3.6
# - create virtualenv

# install pre-requisites
yum -y groupinstall development
yum -y install zlib-devel
yum -y install openssl-devel
yum -y install wget

# Installing openssl-devel alone seems to result in SSL errors in pip (see https://medium.com/@moreless/pip-complains-there-is-no-ssl-support-in-python-edbdce548852)
# Need to install OpenSSL also to avoid these errors
wget https://github.com/openssl/openssl/archive/OpenSSL_1_0_2l.tar.gz
tar -zxvf OpenSSL_1_0_2l.tar.gz
cd openssl-OpenSSL_1_0_2l/

./config shared
make
make install
export LD_LIBRARY_PATH=/usr/local/ssl/lib/

cd ..
rm OpenSSL_1_0_2l.tar.gz
rm -rf openssl-OpenSSL_1_0_2l/


# Install Python 3.6
wget https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tar.xz
tar xJf Python-3.6.2.tar.xz
cd Python-3.6.2

./configure
make
make install

cd ..
rm Python-3.6.2.tar.xz
rm -rf Python-3.6.2


# Create virtualenv running Python 3.6
pip3 install --upgrade virtualenv
virtualenv -p python3.6 awsenv
source awsenv/bin/activate

python --version
# Python 3.6.0