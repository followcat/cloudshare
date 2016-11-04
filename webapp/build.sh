echo "Running Front-end Builder"

export WEBAPP_DIR=`pwd`
export APP_DIR=$WEBAPP_DIR/app
export STATIC_DIR=$WEBAPP_DIR/static

cd $APP_DIR
npm install --registry=https://registry.npm.taobao.org
echo "Running Webpack Builder"
npm run build:production


cd $STATIC_DIR
npm install --registry=https://registry.npm.taobao.org
echo "Running Gulp Builder"
npm run build



