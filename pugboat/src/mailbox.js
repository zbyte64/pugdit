import NodeRSA from 'node-rsa';

//create & store identity
export function newIdentity(username) {
  let key = new NodeRSA({b: 512});
  let public_key = key.exportKey('pkcs8-public-pem');
  let private_key = key.exportKey('pkcs8-private-pem');
  let localStorage = window.localStorage;
  //TODO password encrypt?
  localStorage.setItem('identity_public_key', public_key);
  localStorage.setItem('identity_private_key', private_key);
  return {
    'signed_username': key.sign(username),
    'public_key': public_key,
  };
}

export function loadKey() {
  let localStorage = window.localStorage;
  let private_key = localStorage.getItem('identity_private_key');
  if (!private_key) return null;
  let public_key = localStorage.getItem('identity_public_key');
  let key = new NodeRSA();
  key.importKey(private_key, 'pkcs8');
  return key;
}

export function sign(payload) {
  let key = loadKey();
  return key.sign(payload, 'utf8', 'hex');
}
