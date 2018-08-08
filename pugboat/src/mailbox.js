import nacl from 'tweetnacl';

//create & store identity
function encode(x) {
  //string -> uint8 array
  return new TextEncoder().encode(x);
}

function encodeHex(x) {
  //unit8 array -> hex
  return x.reduce(function(memo, i) {
    return memo + ('0' + i.toString(16)).slice(-2); //padd with leading 0 if <16
  }, '');
}

function encodeBase64(arr) {
  var i, s = [], len = arr.length;
  for (i = 0; i < len; i++) s.push(String.fromCharCode(arr[i]));
  return btoa(s.join(''));
}

export function newIdentity(username) {
  let {publicKey, secretKey} = nacl.sign.keyPair();
  let localStorage = window.localStorage;
  //TODO password encrypt?
  localStorage.setItem('identity_public_key', publicKey);
  localStorage.setItem('identity_private_key', secretKey);
  let payload = encode(username);
  return {
    'signed_username': encodeBase64(nacl.sign(payload, secretKey)),
    'public_key': encodeBase64(publicKey),
  };
}

export function loadKey() {
  let localStorage = window.localStorage;
  let private_key = localStorage.getItem('identity_private_key');
  if (!private_key) return null;
  //let public_key = localStorage.getItem('identity_public_key');
  return private_key;
}

export function sign(payload) {
  let key = loadKey();
  payload = encode(payload);
  let b = nacl.sign(payload, key);
  return encodeBase64(b);
}
