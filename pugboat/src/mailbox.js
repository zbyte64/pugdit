import nacl from 'tweetnacl';


//string -> uint8 array
function byteArray(x) {
  return new TextEncoder().encode(x);
}

//unit8 array -> hex
function encodeHex(x) {
  return x.reduce(function(memo, i) {
    return memo + ('0' + i.toString(16)).slice(-2); //padd with leading 0 if <16
  }, '');
}

function encodeBase64(arr) {
  var i, s = [], len = arr.length;
  for (i = 0; i < len; i++) s.push(String.fromCharCode(arr[i]));
  return btoa(s.join(''));
}

function decodeBase64(s) {
  var i, d = atob(s), b = new Uint8Array(d.length);
  for (i = 0; i < d.length; i++) b[i] = d.charCodeAt(i);
  return b;
}

export function newIdentity(username) {
  let keyPair = getOrCreateKeyPair();
  let payload = byteArray(username);
  return {
    'signed_username': encodeBase64(nacl.sign(payload, keyPair.secretKey)),
    'public_key': encodeBase64(keyPair.publicKey),
  };
}

export function getOrCreateKeyPair() {
  let localStorage = window.localStorage;
  let keyPair = localStorage.getItem('identity_key_pair');
  try {
    if (keyPair) {
      keyPair = JSON.parse(keyPair);
      keyPair.secretKey = decodeBase64(keyPair.secretKey);
      keyPair.publicKey = decodeBase64(keyPair.publicKey);
    }
  } catch(e) {
    //pass
  }
  if (!keyPair || !keyPair.secretKey) {
    keyPair = nacl.sign.keyPair();
    localStorage.setItem('identity_key_pair', JSON.stringify({
      secretKey: encodeBase64(keyPair.secretKey),
      publicKey: encodeBase64(keyPair.publicKey),
    }));
  }
  return keyPair;
}

export function loadKey() {
  return getOrCreateKeyPair()['secretKey'];
}

export function sign(message) {
  let key = loadKey();
  let payload = byteArray(message);
  let b = nacl.sign(payload, key);
  return encodeBase64(b);
}
