cd package
zip -r ../my-deployment-package.zip .
cd ..
zip -g my-deployment-package.zip fetch_news.py
aws lambda update-function-code --function-name fetch_news --zip-file fileb://my-deployment-package.zip