import nacl from 'tweetnacl';
import SecureLS from 'secure-ls';
import _ from 'lodash';


class StorageLocker {
  constructor(username, secretKey) {
    this.username = username;
    this.ls = new SecureLS({
      encodingType: 'des',
      encryptionSecret: secretKey,
    });
    this.lsKey = 'locker/' + this.username;
  }

  sign(payload) {
    let kp = this.getKey();
    console.log('sign', payload, kp.secretKey);
    return nacl.sign(payload, decodeBase64(kp.secretKey));
  }

  getKey() {
    let kp = this.ls.get(this.lsKey);
    if (!_.isString(kp.secretKey) || !_.isString(kp.publicKey)) {
      kp = this.generateKey();
    }
    if (!kp) kp = this.generateKey();
    return kp;
  }

  generateKey() {
    let keyPair = nacl.sign.keyPair();
    return this.stashKey(keyPair);
  }

  stashKey(keyPair) {
    let message = {
      secretKey: encodeBase64(keyPair.secretKey),
      publicKey: encodeBase64(keyPair.publicKey),
    };
    this.ls.set(this.lsKey, message);
    return message;
  }

  signedUsername() {
    return encodeBase64(this.sign(byteArray(this.username)));
  }
}

export var LOCKER = null;

export function setLockerAuth(username, storageKey) {
  LOCKER = new StorageLocker(username, storageKey);
  return LOCKER;
}

//string -> uint8 array
function byteArray(x) {
  return new TextEncoder().encode(x);
}

function encodeBase64(arr) {
  var i, s = [], len = arr.length;
  for (i = 0; i < len; i++) s.push(String.fromCharCode(arr[i]));
  return btoa(s.join(''));
}

export function decodeBase64(s) {
  var i, d = atob(s), b = new Uint8Array(d.length);
  for (i = 0; i < d.length; i++) b[i] = d.charCodeAt(i);
  return b;
}

export function sign(message) {
  let payload = message; //byteArray(message);
  let b = LOCKER.sign(payload);
  return encodeBase64(b);
}

export function getGraphId(bytes) {
  return Buffer.from(bytes, 'base64').toString('ascii').split(':')[1];
}

export function buildRFC822(tuples, payload) {
  let msg = []
  for (let index in tuples) {
    let key = tuples[index][0]
    let value = tuples[index][1].replace('\r\n', '')
    msg.push(`${key}: ${value}`)
  }
  msg.push('\r\n')
  msg.push(payload)
  return msg.join('\r\n')
}
