const CryptoJS=require("crypto-js")
function decryptByDES(ciphertext) {
    var keyHex = CryptoJS.enc.Utf8.parse("1qaz@wsx3e");
    var decrypted = CryptoJS.DES.decrypt({
            ciphertext: CryptoJS.enc.Base64.parse(ciphertext),
        },
        keyHex, {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7,
        }
    );
    return decrypted.toString(CryptoJS.enc.Utf8);
}

