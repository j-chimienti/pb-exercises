'''
#code
>>> from io import BytesIO
>>> import helper, op, script, tx
>>> from ecc import PrivateKey, S256Point, Signature
>>> from helper import decode_base58, encode_base58_checksum, hash160, hash256, int_to_little_endian, SIGHASH_ALL
>>> from script import p2pkh_script, Script
>>> from tx import Tx, TxIn, TxOut

#endcode
#unittest
tx:TxTest:test_verify_p2pkh:
#endunittest
#code
>>> # Transaction Construction Example
>>> from ecc import PrivateKey
>>> from helper import decode_base58, SIGHASH_ALL
>>> from script import p2pkh_script, Script
>>> from tx import Tx, TxIn, TxOut
>>> # Step 1
>>> tx_ins = []
>>> prev_tx = bytes.fromhex('8be2f69037de71e3bc856a6627ed3e222a7a2d0ce81daeeb54a3aea8db274149')
>>> prev_index = 4
>>> tx_ins.append(TxIn(prev_tx, prev_index))
>>> # Step 2
>>> tx_outs = []
>>> h160 = decode_base58('mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2')
>>> tx_outs.append(TxOut(
...     amount=int(0.38*100000000),
...     script_pubkey=p2pkh_script(h160),
... ))
>>> h160 = decode_base58('mnrVtF8DWjMu839VW3rBfgYaAfKk8983Xf')
>>> tx_outs.append(TxOut(
...     amount=int(0.1*100000000),
...     script_pubkey=p2pkh_script(h160),
... ))
>>> tx_obj = Tx(1, tx_ins, tx_outs, 0, testnet=True)
>>> # Step 3
>>> z = tx_obj.sig_hash(0)
>>> pk = PrivateKey(secret=8675309)
>>> der = pk.sign(z).der()
>>> sig = der + SIGHASH_ALL.to_bytes(1, 'big')
>>> sec = pk.point.sec()
>>> tx_obj.tx_ins[0].script_sig = Script([sig, sec])
>>> print(tx_obj.serialize().hex())
0100000001494127dba8aea354ebae1de80c2d7a2a223eed27666a85bce371de3790f6e28b040000006b483045022100fa3032607b50e8cb05bedc9d43f986f19dedc22e61320b9765061c5cd9c66946022072d514ef637988515bfa59a660596206de68f0ed4090d0a398e70f4d81370dfb012103935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b67ffffffff0280d54302000000001976a914d52ad7ca9b3d096a38e752c2018e6fbc40cdf26f88ac80969800000000001976a914507b27411ccf7f16f10297de6cef3f291623eddf88ac00000000

#endcode
#unittest
tx:TxTest:test_sign_input:
#endunittest
#exercise
Send 0.04 TBTC to this address 

`mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv`

#### Go here to send your transaction: https://live.blockcypher.com/btc-testnet/pushtx/
---
>>> from tx import Tx, TxIn, TxOut
>>> from helper import hash256, little_endian_to_int
>>> prev_tx = bytes.fromhex('0c024b9d3aa2ae8faae96603b8d40c88df2fc6bf50b3f446295206f70f3cf6ad')  #/prev_tx = bytes.fromhex('<transaction id here>')  # CHANGE
>>> prev_index = 0  #/prev_index = -1  # CHANGE
>>> target_address = 'mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv'
>>> target_amount = 0.04
>>> fee = 50000
>>> passphrase = b'Jimmy Song'  #/passphrase = b'<your passphrase here>'  # CHANGE
>>> secret = little_endian_to_int(hash256(passphrase))
>>> private_key = PrivateKey(secret=secret)
>>> change_address = private_key.point.address(testnet=True)
>>> # initialize inputs
>>> tx_ins = []  #/
>>> # create a new tx input with prev_tx, prev_index
>>> tx_ins.append(TxIn(prev_tx, prev_index))  #/
>>> # initialize outputs
>>> tx_outs = []  #/
>>> # decode the hash160 from the target address
>>> h160 = decode_base58(target_address)  #/
>>> # convert hash160 to p2pkh script
>>> script_pubkey = p2pkh_script(h160)  #/
>>> # convert target amount to satoshis (multiply by 100 million)
>>> target_satoshis = int(target_amount*100000000)  #/
>>> # create a new tx output for target with amount and script_pubkey
>>> tx_outs.append(TxOut(target_satoshis, script_pubkey))  #/
>>> # decode the hash160 from the change address
>>> h160 = decode_base58(change_address)  #/
>>> # convert hash160 to p2pkh script
>>> script_pubkey = p2pkh_script(h160)  #/
>>> # get the value for the transaction input (remember testnet=True)
>>> prev_amount = tx_ins[0].value(testnet=True)  #/
>>> # calculate change_satoshis based on previous amount, target_satoshis & fee
>>> change_satoshis = prev_amount - target_satoshis - fee  #/
>>> # create a new tx output for target with amount and script_pubkey
>>> tx_outs.append(TxOut(change_satoshis, script_pubkey))  #/
>>> # create the transaction (name it tx_obj to not conflict)
>>> tx_obj = Tx(1, tx_ins, tx_outs, 0, testnet=True)  #/
>>> # now sign the 0th input with the private_key using sign_input
>>> tx_obj.sign_input(0, private_key)  #/
True
>>> # SANITY CHECK: change address corresponds to private key
>>> if private_key.point.address(testnet=True) != change_address:
...     raise RuntimeError('Private Key does not correspond to Change Address, check priv_key and change_address')
>>> # SANITY CHECK: output's script_pubkey is the same one as your address
>>> if tx_ins[0].script_pubkey(testnet=True).instructions[2] != decode_base58(change_address):
...     raise RuntimeError('Output is not something you can spend with this private key. Check that the prev_tx and prev_index are correct')
>>> # SANITY CHECK: fee is reasonable
>>> if tx_obj.fee() > 0.05*100000000 or tx_obj.fee() <= 0:
...     raise RuntimeError('Check that the change amount is reasonable. Fee is {}'.format(tx_obj.fee()))
>>> # serialize and hex()
>>> print(tx_obj.serialize().hex())  #/
0100000001adf63c0ff706522946f4b350bfc62fdf880cd4b80366e9aa8faea23a9d4b020c000000006a47304402201967ab281d8d2b47cd36ae62022cb360d973fa97832edb97888d6b136196f23d022008dd3d8231e28429b61c92866a3e4394b067854b5d5fbc7fe3fc9b978522a298012103dc585d46cfca73f3a75ba1ef0c5756a21c1924587480700c6eb64e3f75d22083ffffffff0200093d00000000001976a914ad346f8eb57dee9a37981716e498120ae80e44f788ac30ca5a00000000001976a914850af0029eb376691c3eef244c25eceb4e50c50388ac00000000

#endexercise
#exercise
#### Bonus Question. Only attempt if you've finished Exercise 3 and have time to try it.

Get some testnet coins and spend both outputs (one from your change address and one from the testnet faucet) to 

`mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv`

#### You can get some free testnet coins at: https://testnet.coinfaucet.eu/en/
---
>>> # Bonus
>>> prev_tx_1 = bytes.fromhex('0886537e27969a12478e0d33707bf6b9fe4fdaec8d5d471b5304453b04135e7e')  #/prev_tx_1 = bytes.fromhex('<tx id from last exercise>')  # CHANGE
>>> prev_index_1 = 1  #/prev_index_1 = -1  # CHANGE
>>> prev_tx_2 = bytes.fromhex('da9d75c119dfccac71c9eb8ebf3724f6066d4a84cfce4eaa1bcebd32276886c5')  #/prev_tx_2 = bytes.fromhex('<tx id from faucet>')  # CHANGE
>>> prev_index_2 = 1  #/prev_index_2 = -1  # CHANGE
>>> target_address = 'mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv'
>>> fee = 50000
>>> passphrase = b'Jimmy Song'  #/passphrase = b'<your passphrase here>'  # CHANGE
>>> secret = little_endian_to_int(hash256(passphrase))
>>> private_key = PrivateKey(secret=secret)
>>> # initialize inputs
>>> tx_ins = []  #/
>>> # create the first tx input with prev_tx_1, prev_index_1
>>> tx_ins.append(TxIn(prev_tx_1, prev_index_1))  #/
>>> # create the second tx input with prev_tx_2, prev_index_2
>>> tx_ins.append(TxIn(prev_tx_2, prev_index_2))  #/
>>> # initialize outputs
>>> tx_outs = []  #/
>>> # decode the hash160 from the target address
>>> h160 = decode_base58(target_address)  #/
>>> # convert hash160 to p2pkh script
>>> script_pubkey = p2pkh_script(h160)  #/
>>> # calculate target amount by adding the input values and subtracting the fee
>>> target_satoshis = tx_ins[0].value(True) + tx_ins[1].value(True) - fee  #/
>>> # create a single tx output for target with amount and script_pubkey
>>> tx_outs.append(TxOut(target_satoshis, script_pubkey))  #/
>>> # create the transaction
>>> tx_obj = Tx(1, tx_ins, tx_outs, 0, testnet=True)  #/
>>> # sign both inputs with the private key using sign_input
>>> tx_obj.sign_input(0, private_key)  #/
True
>>> tx_obj.sign_input(1, private_key)  #/
True
>>> # SANITY CHECK: output's script_pubkey is the same one as your address
>>> if tx_ins[0].script_pubkey(testnet=True).instructions[2] != decode_base58(private_key.point.address(testnet=True)):
...     raise RuntimeError('Output is not something you can spend with this private key. Check that the prev_tx and prev_index are correct')
>>> # SANITY CHECK: fee is reasonable
>>> if tx_obj.fee() > 0.05*100000000 or tx_obj.fee() <= 0:
...     raise RuntimeError('Check that the change amount is reasonable. Fee is {}'.format(tx_obj.fee()))
>>> # serialize and hex()
>>> print(tx_obj.serialize().hex())  #/
01000000027e5e13043b4504531b475d8decda4ffeb9f67b70330d8e47129a96277e538608010000006a473044022071ccd9179773e113f6d1d4c2ad5042c8a49fc47ee98ba4a9dae5e61db67cce7502206fd1043be9c9c97904663f4b1a51e3f9d256f1df5de990507dc78369c1b4030b012103dc585d46cfca73f3a75ba1ef0c5756a21c1924587480700c6eb64e3f75d22083ffffffffc586682732bdce1baa4ececf844a6d06f62437bf8eebc971acccdf19c1759dda010000006b483045022100970e49e00a15245c51db09303ef4769d1cfbd1b947c8d0340ea4176aa8cc9870022040f809aeaf40196afba1910e31926ed6f88e3dd73be04a1873191c202fbef8f6012103dc585d46cfca73f3a75ba1ef0c5756a21c1924587480700c6eb64e3f75d22083ffffffff0110d1b400000000001976a914ad346f8eb57dee9a37981716e498120ae80e44f788ac00000000

#endexercise
#code
>>> # op_checkmultisig
>>> def op_checkmultisig(stack, z):
...     if len(stack) < 1:
...         return False
...     n = decode_num(stack.pop())
...     if len(stack) < n + 1:
...         return False
...     sec_pubkeys = []
...     for _ in range(n):
...         sec_pubkeys.append(stack.pop())
...     m = decode_num(stack.pop())
...     if len(stack) < m + 1:
...         return False
...     der_signatures = []
...     for _ in range(m):
...         # signature is assumed to be using SIGHASH_ALL
...         der_signatures.append(stack.pop()[:-1])
...     # OP_CHECKMULTISIG bug
...     stack.pop()
...     try:
...         raise NotImplementedError
...     except (ValueError, SyntaxError):
...         return False
...     return True

#endcode
#unittest
op:OpTest:test_op_checkmultisig:
#endunittest
#exercise
Find the hash160 of the RedeemScript
```
5221022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb7152ae
```
---
>>> hex_redeem_script = '5221022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb7152ae'
>>> # bytes.fromhex script
>>> redeem_script = bytes.fromhex(hex_redeem_script)  #/
>>> # hash160 result
>>> h160 = hash160(redeem_script)  #/
>>> # hex() to display
>>> print(h160.hex())  #/
74d691da1574e6b3c192ecfb52cc8984ee7b6c56

#endexercise
#code
>>> # P2SH address construction example
>>> from helper import encode_base58_checksum
>>> print(encode_base58_checksum(b'\x05'+bytes.fromhex('74d691da1574e6b3c192ecfb52cc8984ee7b6c56')))
3CLoMMyuoDQTPRD3XYZtCvgvkadrAdvdXh

#endcode
#unittest
helper:HelperTest:test_p2pkh_address:
#endunittest
#unittest
helper:HelperTest:test_p2sh_address:
#endunittest
#unittest
script:ScriptTest:test_address:
#endunittest
#code
>>> # z for p2sh example
>>> from helper import hash256
>>> h256 = hash256(bytes.fromhex('0100000001868278ed6ddfb6c1ed3ad5f8181eb0c7a385aa0836f01d5e4789e6bd304d87221a000000475221022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb7152aeffffffff04d3b11400000000001976a914904a49878c0adfc3aa05de7afad2cc15f483a56a88ac7f400900000000001976a914418327e3f3dda4cf5b9089325a4b95abdfa0334088ac722c0c00000000001976a914ba35042cfe9fc66fd35ac2224eebdafd1028ad2788acdc4ace020000000017a91474d691da1574e6b3c192ecfb52cc8984ee7b6c56870000000001000000'))
>>> z = int.from_bytes(h256, 'big')
>>> print(hex(z))
0xe71bfa115715d6fd33796948126f40a8cdd39f187e4afb03896795189fe1423c

#endcode
#code
>>> # p2sh verification example
>>> from ecc import S256Point, Signature
>>> from helper import hash256
>>> h256 = hash256(bytes.fromhex('0100000001868278ed6ddfb6c1ed3ad5f8181eb0c7a385aa0836f01d5e4789e6bd304d87221a000000475221022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb7152aeffffffff04d3b11400000000001976a914904a49878c0adfc3aa05de7afad2cc15f483a56a88ac7f400900000000001976a914418327e3f3dda4cf5b9089325a4b95abdfa0334088ac722c0c00000000001976a914ba35042cfe9fc66fd35ac2224eebdafd1028ad2788acdc4ace020000000017a91474d691da1574e6b3c192ecfb52cc8984ee7b6c56870000000001000000'))
>>> z = int.from_bytes(h256, 'big')
>>> point = S256Point.parse(bytes.fromhex('022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb70'))
>>> sig = Signature.parse(bytes.fromhex('3045022100dc92655fe37036f47756db8102e0d7d5e28b3beb83a8fef4f5dc0559bddfb94e02205a36d4e4e6c7fcd16658c50783e00c341609977aed3ad00937bf4ee942a89937'))
>>> print(point.verify(z, sig))
True

#endcode
#exercise
Validate the second signature of the first input

```
0100000001868278ed6ddfb6c1ed3ad5f8181eb0c7a385aa0836f01d5e4789e6bd304d87221a000000db00483045022100dc92655fe37036f47756db8102e0d7d5e28b3beb83a8fef4f5dc0559bddfb94e02205a36d4e4e6c7fcd16658c50783e00c341609977aed3ad00937bf4ee942a8993701483045022100da6bee3c93766232079a01639d07fa869598749729ae323eab8eef53577d611b02207bef15429dcadce2121ea07f233115c6f09034c0be68db99980b9a6c5e75402201475221022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb7152aeffffffff04d3b11400000000001976a914904a49878c0adfc3aa05de7afad2cc15f483a56a88ac7f400900000000001976a914418327e3f3dda4cf5b9089325a4b95abdfa0334088ac722c0c00000000001976a914ba35042cfe9fc66fd35ac2224eebdafd1028ad2788acdc4ace020000000017a91474d691da1574e6b3c192ecfb52cc8984ee7b6c568700000000
```

The sec pubkey of the second signature is:
```
03b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb71
```

The der signature of the second signature is:
```
3045022100da6bee3c93766232079a01639d07fa869598749729ae323eab8eef53577d611b02207bef15429dcadce2121ea07f233115c6f09034c0be68db99980b9a6c5e75402201475221022
```

The redeemScript is:
```
475221022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb7152ae
```
---
>>> hex_sec = '03b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb71'
>>> hex_der = '3045022100da6bee3c93766232079a01639d07fa869598749729ae323eab8eef53577d611b02207bef15429dcadce2121ea07f233115c6f09034c0be68db99980b9a6c5e754022'
>>> hex_redeem_script = '475221022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb7152ae'
>>> sec = bytes.fromhex(hex_sec)
>>> der = bytes.fromhex(hex_der)
>>> redeem_script_stream = BytesIO(bytes.fromhex(hex_redeem_script))
>>> hex_tx = '0100000001868278ed6ddfb6c1ed3ad5f8181eb0c7a385aa0836f01d5e4789e6bd304d87221a000000db00483045022100dc92655fe37036f47756db8102e0d7d5e28b3beb83a8fef4f5dc0559bddfb94e02205a36d4e4e6c7fcd16658c50783e00c341609977aed3ad00937bf4ee942a8993701483045022100da6bee3c93766232079a01639d07fa869598749729ae323eab8eef53577d611b02207bef15429dcadce2121ea07f233115c6f09034c0be68db99980b9a6c5e75402201475221022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb7152aeffffffff04d3b11400000000001976a914904a49878c0adfc3aa05de7afad2cc15f483a56a88ac7f400900000000001976a914418327e3f3dda4cf5b9089325a4b95abdfa0334088ac722c0c00000000001976a914ba35042cfe9fc66fd35ac2224eebdafd1028ad2788acdc4ace020000000017a91474d691da1574e6b3c192ecfb52cc8984ee7b6c568700000000'
>>> stream = BytesIO(bytes.fromhex(hex_tx))
>>> # parse the S256Point and Signature
>>> point = S256Point.parse(sec)  #/
>>> sig = Signature.parse(der)  #/
>>> # parse the Tx
>>> t = Tx.parse(stream)  #/
>>> # change the first input's scriptSig to redeemScript
>>> # use Script.parse on the redeem_script_stream
>>> t.tx_ins[0].script_sig = Script.parse(redeem_script_stream)  #/
>>> # get the serialization
>>> ser = t.serialize()  #/
>>> # add the sighash (4 bytes, little-endian of SIGHASH_ALL)
>>> ser += int_to_little_endian(SIGHASH_ALL, 4)  #/
>>> # hash256 the result
>>> h256 = hash256(ser)  #/
>>> # this interpreted is a big-endian number is your z
>>> z = int.from_bytes(h256, 'big')  #/
>>> # now verify the signature using point.verify
>>> print(point.verify(z, sig))  #/
True

#endexercise
'''


from io import BytesIO
from unittest import TestCase

import helper
import op


from ecc import (
    PrivateKey,
    S256Point,
    Signature,
)
from helper import (
    decode_base58,
    encode_base58_checksum,
    hash160,
    hash256,
    int_to_little_endian,
    SIGHASH_ALL,
)
from op import (
    decode_num,
    encode_num,
)
from script import (
    p2pkh_script,
    Script,
)
from tx import (
    Tx,
    TxIn,
    TxOut,
)


def verify_input(self, input_index):
    tx_in = self.tx_ins[input_index]
    z = self.sig_hash(input_index)
    combined_script = tx_in.script_sig + tx_in.script_pubkey(self.testnet)
    return combined_script.evaluate(z)


def sign_input(self, input_index, private_key):
    z = self.sig_hash(input_index)
    der = private_key.sign(z).der()
    sig = der + SIGHASH_ALL.to_bytes(1, 'big')
    sec = private_key.point.sec()
    script_sig = Script([sig, sec])
    self.tx_ins[input_index].script_sig = script_sig
    return self.verify_input(input_index)


def op_checkmultisig(stack, z):
    if len(stack) < 1:
        return False
    n = decode_num(stack.pop())
    if len(stack) < n + 1:
        return False
    sec_pubkeys = []
    for _ in range(n):
        sec_pubkeys.append(stack.pop())
    m = decode_num(stack.pop())
    if len(stack) < m + 1:
        return False
    der_signatures = []
    for _ in range(m):
        der_signatures.append(stack.pop()[:-1])
    stack.pop()
    try:
        points = [S256Point.parse(sec) for sec in sec_pubkeys]
        sigs = [Signature.parse(der) for der in der_signatures]
        for sig in sigs:
            if len(points) == 0:
                print("signatures no good or not in right order")
                return False
            while points:
                point = points.pop(0)
                if point.verify(z, sig):
                    break
        stack.append(encode_num(1))
    except (ValueError, SyntaxError):
        return False
    return True


def h160_to_p2pkh_address(h160, testnet=False):
    if testnet:
        prefix = b'\x6f'
    else:
        prefix = b'\x00'
    return encode_base58_checksum(prefix + h160)


def h160_to_p2sh_address(h160, testnet=False):
    if testnet:
        prefix = b'\xc4'
    else:
        prefix = b'\x05'
    return encode_base58_checksum(prefix + h160)


def is_p2pkh_script_pubkey(self):
    return len(self.instructions) == 5 and self.instructions[0] == 0x76 \
        and self.instructions[1] == 0xa9 \
        and type(self.instructions[2]) == bytes and len(self.instructions[2]) == 20 \
        and self.instructions[3] == 0x88 and self.instructions[4] == 0xac


def is_p2sh_script_pubkey(self):
    return len(self.instructions) == 3 and self.instructions[0] == 0xa9 \
        and type(self.instructions[1]) == bytes and len(self.instructions[1]) == 20 \
        and self.instructions[2] == 0x87


def address(self, testnet=False):
    if self.is_p2pkh_script_pubkey():
        h160 = self.instructions[2]
        return h160_to_p2pkh_address(h160, testnet)
    elif self.is_p2sh_script_pubkey():
        h160 = self.instructions[1]
        return h160_to_p2sh_address(h160, testnet)
    raise ValueError('Unknown ScriptPubKey')


class SessionTest(TestCase):

    def test_apply(self):
        Tx.verify_input = verify_input
        Tx.sign_input = sign_input
        op.op_checkmultisig = op_checkmultisig
        op.OP_CODE_FUNCTIONS[0xae] = op_checkmultisig
        helper.h160_to_p2pkh_address = h160_to_p2pkh_address
        helper.h160_to_p2sh_address = h160_to_p2sh_address
        Script.is_p2pkh_script_pubkey = is_p2pkh_script_pubkey
        Script.is_p2sh_script_pubkey = is_p2sh_script_pubkey
        Script.address = address
