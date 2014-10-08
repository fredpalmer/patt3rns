#!/usr/bin/env bash
set -eo pipefail

NODE_VERSION=0.8.12
NODE_BASENAME=node-v${NODE_VERSION}-linux-x64
NODE_ARCHIVE="http://nodejs.org/dist/v${NODE_VERSION}/${NODE_BASENAME}.tar.gz"

# make a temp directory
tempdir="$( mktemp -t node_XXXX )"
rm -rf $tempdir
mkdir -p $tempdir

pushd $tempdir
curl -s -L -o tmp-nodejs.tar.gz $NODE_ARCHIVE
tar -zxvf tmp-nodejs.tar.gz > /dev/null
rm tmp-nodejs.tar.gz
popd

mkdir -v -p $BUILD_DIR/.heroku/vendor
pushd $BUILD_DIR/.heroku/vendor
rm -rf node
mv $tempdir/$NODE_BASENAME node
popd

ln -s -f ../../vendor/node/bin/node .heroku/python/bin/node
ln -s -f ../../vendor/node/bin/node-waf .heroku/python/bin/node-waf
ln -s -f ../../vendor/node/bin/npm .heroku/python/bin/npm
