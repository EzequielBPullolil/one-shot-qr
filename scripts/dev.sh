export DB_PATH="./databases/dev.db"
export URL_ENCRYPT_CODE="dev_code_1234561"
export SECRET_KEY='dev'
export SHORTCUT_ADDRESS="0.0.0.0:5000"

flask --app src/main.py run -h 0.0.0.0 --debug