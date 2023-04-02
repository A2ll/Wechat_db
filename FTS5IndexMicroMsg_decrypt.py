from os.path import isfile
# 用pip install pysqlcipher3安装python的sqlcipher支持库再引用
from pysqlcipher3 import dbapi2 as sqlite
import hashlib
import sys
import time
import logging
import re

logging.basicConfig(filename='FTS5IndexMicroMsg_decrypt.log', format="%(asctime)s %(levelname)s: %(message)s",
                    datefmt="%d-%b-%Y %I:%M:%S %p", level=logging.DEBUG)


def decrypt(key):
    logging.info("连接数据库...")
    conn = sqlite.connect("FTS5IndexMicroMsg_encrypt.db")
    c = conn.cursor()
    c.execute("PRAGMA key = '" + key + "';")
    c.execute("PRAGMA cipher = 'aes-256-cbc';")
    c.execute("PRAGMA cipher_use_hmac = ON;")
    c.execute("PRAGMA cipher_page_size = 4096;")
    c.execute("PRAGMA kdf_iter = 64000;")
    try:
        logging.info("正在解密...")
        c.execute("ATTACH DATABASE 'FTS5IndexMicroMsg_decrypt.db' AS fts5indexdecrypt KEY '';")
        c.execute("SELECT sqlcipher_export( 'fts5indexdecrypt' );")
        c.execute("DETACH DATABASE fts5indexdecrypt;")
        logging.info("正在分离数据库...")
        c.close()
        status = 1
    except:
        c.close()
        status = 0
    return status


def generate_key():
    imei = "863640032818824"
    logging.info("IMEI: " + str(imei))
    uin_int = 3107845370  # 此处必须为正数才能运行
    if uin_int < 0:
        uin = str(uin_int + 4294967296)
    else:
        uin = str(uin_int)
    logging.info("UIN: " + str(uin))
    account = "wxid_g1wk7ir1u91j22"
    logging.info("account: " + str(account))
    logging.info("正在生成密钥...")
    key = hashlib.md5(str(uin).encode("utf8") + str(imei).encode("utf8") + str(account).encode("utf8")).hexdigest()[0:7]
    logging.info("密钥: " + key)
    return key


def db_hash():
    f = open('FTS5IndexMicroMsg_decrypt.db', 'rb').read()
    logging.info("正在生成哈希值...")
    if len(f) > 0:
        db_md5 = hashlib.md5(f).hexdigest()
        logging.info("FTS5IndexMicroMsg_decrypt.db MD5: " + db_md5)
        db_sha1 = hashlib.sha1(f).hexdigest()
        logging.info("FTS5IndexMicroMsg_decrypt.db SHA1: " + db_sha1)
        return


def main():
    if not (isfile("FTS5IndexMicroMsg_encrypt.db")):
        print("##########")
        print("'FTS5IndexMicroMsg_encrypt.db'不存在!")
        print("正在退出脚本...")
        print("##########")
        sys.exit()

    logging.info("脚本启动...")
    key = generate_key()
    status = decrypt(key)
    if status == 1:
        db_hash()
        print("##########")
        print("解密成功!")
        print("解密文件: FTS5IndexMicroMsg_decrypt.db")
        print("日志文件: FTS5IndexMicroMsg_decrypt.log")
        print("##########")
        logging.info("解密成功!")
        logging.info("解密文件: FTS5IndexMicroMsg_decrypt.db")
    else:
        print("##########")
        print("解密失败!")
        print("日志文件: FTS5IndexMicroMsg_decrypt.log")
        print("##########")
        logging.info("解密失败!")
    logging.info("正在退出脚本...")


main()
