rm -rf /lambda2git/packages
rm lambda2git.zip

pip install --target /lambda2git/packages requests

zip -r lambda2git . \
    -x *.pyc* \
    -x *.git* \
    -x *packages/*.pyc* \
    -x *.swp* \
    -x .env
