# taiyochhanel

## 起動前の準備
docker-compose.ymlをダウンロード
```
git clone https://github.com/k175jp/taiyochannel.git
cd taiyochannel
```

## .env file
docker-compose.ymlと同じディレクトリに配置
```
MYSQL_DATABASE=taiyochannel_database
MYSQL_USER=taiyochannel_user
MYSQL_PASSWORD=taiyochannel_password
MYSQL_ROOT_PASSWORD=taiyochannel_password
TZ=Asia/Tokyo
LANG=ja_JP.UTF-8
LANGUAGE=ja_JP:ja
DB_HOST=db
DB_PORT=3306
```

## 起動
```docker compose up -d```を実行して起動

## 停止
```docker compose down ```を実行して停止

