from pysqlcipher3 import dbapi2 as sqlite
import hashlib


def decrypt(key):
    conn = sqlite.connect("EnMicroMsg.db")
    c = conn.cursor()
    c.execute("PRAGMA key = '" + key + "';")
    c.execute("PRAGMA cipher_use_hmac = OFF;")
    c.execute("PRAGMA cipher_page_size = 1024;")
    c.execute("PRAGMA kdf_iter = 4000;")
    c.execute("ATTACH DATABASE 'EnMicroMsg-decrypted.db' AS wechatdecrypted KEY '';")
    c.execute("SELECT sqlcipher_export( 'wechatdecrypted' );")
    c.execute("DETACH DATABASE wechatdecrypted;")
    c.close()


def generate_key():
    imei = "863640032818824"
    uin = "-1187121926"
    key = hashlib.md5(str(imei).encode("utf8") + str(uin).encode("utf8")).hexdigest()[0:7]
    return key


def main():
    key = generate_key()
    decrypt(key)


main()
