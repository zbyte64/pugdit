import nacl from 'tweetnacl';

//create & store identity
function encode(x) {
  //string -> unit8 array
  return new TextEncoder().encode(x);
}

function decode(x) {
  //unit8 array -> hex
  return x.reduce(function(memo, i) {
    return memo + ('0' + i.toString(16)).slice(-2); //padd with leading 0 if <16
  }, '');
}

export function newIdentity(username) {
  let {publicKey, secretKey} = nacl.sign.keyPair();
  let localStorage = window.localStorage;
  //TODO password encrypt?
  localStorage.setItem('identity_public_key', publicKey);
  localStorage.setItem('identity_private_key', secretKey);
  let payload = encode(username);
  return {
    'signed_username': decode(nacl.sign(payload, secretKey)),
    'public_key': decode(publicKey),
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
  return decode(b);
}
